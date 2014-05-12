# -*- coding: utf-8 -*-

# Copyright 2014 CNA_Bld @ SSHZ.ORG
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from google.appengine.ext import ndb
from google.appengine.api import memcache
import datetime
import sys

sys.path.insert(0, "lib")
from tenjin.html import text2html

import utils
import settings

class SiteSettings(ndb.Model):
    site_title = ndb.StringProperty(indexed=False)
    description = ndb.StringProperty(indexed=False)
    front_page = ndb.StringProperty(indexed=False)
    footer_info = ndb.StringProperty(indexed=False)
    cookie_expiry_days = ndb.IntegerProperty(indexed=False)
    default_page_size = ndb.IntegerProperty(indexed=False)
    default_language = ndb.StringProperty(indexed=False)

    @classmethod
    def get_site_settings(cls):
        settings = cls.query().get()
        if not settings:
            settings = SiteSettings(site_title="GAE Keijiban", description="A lightweight Keijiban running on GAE",
                                    front_page="", footer_info="Copyright 2014 CNA_Bld @ SSHZ.ORG", cookie_expiry_days=30,
                                    default_page_size=10, default_language="en")
            settings.put()
        return settings


class ForumCategory(ndb.Model):
    name = ndb.StringProperty()
    order = ndb.IntegerProperty()

    @classmethod
    def get_categories(cls):
        return cls.query().order(ForumCategory.order)


class Forum(ndb.Model):  # Ancestor: ForumCategory
    title = ndb.StringProperty()
    forum_description = ndb.StringProperty(indexed=False)
    order = ndb.IntegerProperty()
    locked = ndb.BooleanProperty()
    posts_count = ndb.IntegerProperty(indexed=False)

    def can_post(self):
        return not self.locked

    def modify_posts_count(self, delta):
        self.posts_count += delta
        self.put()

    def query_posts(self, page, page_size):
        posts = Post.query_posts_by_page(self.key, page, page_size)
        result = []
        for post in posts:
            post_dict = post.to_dict()
            post_dict['replies'] = []
            replies = post.query_replies(old_to_new=False)
            if replies.count() > 0:
                if replies.count() > 5:
                    post_dict['hidden_replies'] = replies.count() - 5
                else:
                    post_dict['hidden_replies'] = 0

                for reply in reversed(list(replies.fetch(5))):
                    post_dict['replies'].append(reply.to_dict())
            else:
                post_dict['hidden_replies'] = 0
            result.append(post_dict)
        return result

    @classmethod
    def get_forums(cls):
        forums = []
        forum_categories = ForumCategory.get_categories()
        for forum_category in forum_categories:
            category = {'name': forum_category.name, 'forums': []}
            for forum in cls.query(ancestor=forum_category.key).order(Forum.order):
                category['forums'].append(forum.title)
            forums.append(category)
        return forums

    @classmethod
    def get_forum_by_name(cls, name):
        try:
            forum = cls.query(cls.title == name).get()
            return forum
        except IndexError:
            raise IndexError()  # TODO: this should be a 404


class Post(ndb.Model):  # Ancestor: Forum (Po) or Post (Reply)
    title = ndb.StringProperty(indexed=False)
    content = ndb.StringProperty(indexed=False)
    po_name = ndb.StringProperty()
    po_id = ndb.StringProperty()  # This should be auto generated
    po_email = ndb.StringProperty()  # No check on format, maybe SAGE
    po_ip = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now=True)
    force_saged = ndb.BooleanProperty()
    locked = ndb.BooleanProperty()
    attached_img = ndb.BlobKeyProperty()
    display_date = ndb.DateTimeProperty(auto_now_add=True)
    replies_count = ndb.IntegerProperty(indexed=False)
    is_reply = ndb.BooleanProperty()
    is_admin = ndb.BooleanProperty()

    def can_post(self):
        return (not self.locked) and (self.key.parent().get().can_post())

    def check_and_put(self):
        if self.can_post():
            self.content = text2html(self.content)
            self.put()
            if self.is_reply:
                self.key.parent().get().update_post(1, reply_saged=(self.po_email.lower() == 'sage'))
            else:
                self.key.parent().get().modify_posts_count(1)
            return True
        else:
            return  # TODO

    def update_post(self, delta, reply_saged=False):
        if not self.is_reply:
            self.replies_count += delta
            if not (delta <= 0 or self.force_saged or reply_saged):
                self.display_date = datetime.datetime.now()
            self.put()

    def query_replies(self, old_to_new=False):
        if self.is_reply:
            raise TypeError()
        else:
            query = Post.query(ancestor=self.key).filter(Post.is_reply == True)
            if old_to_new:
                query = query.order(Post.date)
            else:
                query = query.order(-Post.date)
            return query

    def query_replies_by_page(self, page=1, page_size=10):
        query = self.query_replies(old_to_new=True)
        return list(query.fetch(limit=page_size, offset=(page - 1) * page_size))

    def to_dict_on_reply_page(self, page=1, page_size=10):
        post_dict = self.to_dict()
        post_dict['hidden_replies'] = 0
        post_dict['replies'] = []
        replies = self.query_replies_by_page(page, page_size)
        for reply in replies:
            post_dict['replies'].append(reply.to_dict())
        return post_dict

    def to_dict(self):
        return {'attached_img': None, 'title': self.title, 'po_name': self.po_name, 'date': str(self.date),
                'po_id': self.po_id, 'id': str(self.key.id()), 'force_saged': self.force_saged, 'locked': self.locked,
                'content': self.content, 'po_ip': self.po_ip, 'is_admin': self.is_admin}

    @classmethod
    def query_posts_by_page(cls, ancestor_key, page=1, page_size=10):
        query = cls.query_post(ancestor_key).filter(Post.is_reply == False)
        return list(query.fetch(limit=page_size, offset=(page - 1) * page_size))

    @classmethod
    def query_post(cls, ancestor_key):
        return cls.query(ancestor=ancestor_key).order(-cls.display_date)


class UserKey(ndb.Model):
    display_id = ndb.StringProperty()
    private_key = ndb.StringProperty()
    is_admin = ndb.BooleanProperty(default=False)
    expiry_date = ndb.DateTimeProperty()

    @classmethod
    def get_expiry_date(cls):
        return datetime.datetime.now() + datetime.timedelta(
            days=int(SiteSettings.get_site_settings().cookie_expiry_days))

    @classmethod
    def generate_new(cls):
        user_key = UserKey()
        while True:
            user_key.display_id = utils.random_str(8)
            if cls.query(cls.display_id == user_key.display_id).count() == 0:
                break
        user_key.private_key = utils.random_str(128)
        user_key.expiry_date = cls.get_expiry_date()
        user_key.put()
        return user_key

    @classmethod
    def validate(cls, display_id, private_key):
        if display_id and private_key:
            private_key_in_cache = memcache.get('ukey_'+display_id)
            if private_key_in_cache is not None:
                if private_key == private_key_in_cache:
                    return UserKey(display_id=display_id, private_key=private_key)
            qry = cls.query(cls.display_id == display_id, cls.private_key == private_key)
            if qry.count() > 0 and qry.get().expiry_date > datetime.datetime.now():
                memcache.add('ukey_'+display_id, private_key, time=settings.MEMCACHE_EXPIRY)
                user_key = qry.get()
                user_key.expiry_date = cls.get_expiry_date()
                user_key.put()
                return user_key
        return cls.generate_new()


class BannedIP(ndb.Model):
    ip = ndb.StringProperty()
    end_date = ndb.DateTimeProperty()
