# -*- coding: utf-8 -*-

# Copyright 2014 CNA_Bld & AngelaTang @ SSHZ.ORG
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from __future__ import with_statement

import sys
import os
import webapp2
import urllib
from google.appengine.ext import ndb
from google.appengine.api import users

import models
import m17n

is_dev = (os.environ.get("SERVER_SOFTWARE") or "").startswith("Devel")

sys.path.insert(0, "lib")
import tenjin

tenjin.set_template_encoding("utf-8")
from tenjin import *
from tenjin.helpers import *
from tenjin.helpers.html import *
import tenjin.gae

tenjin.gae.init()
import logging

logger = logging.getLogger()
if is_dev:
    logger.setLevel(logging.DEBUG)
tenjin.logger = logger

tenjin_config = {
    "path": ["templates"],
    "layout": "_layout.pyhtml",
    "preprocess": True
}

engines = {i: tenjin.Engine(lang=i, **tenjin_config) for i in m17n.MESSAGE_CATALOG}

import settings

site_settings = models.SiteSettings.get_site_settings()


def is_admin():
    return users.get_current_user() and users.is_current_user_admin()


def get_basic_context():
    return {"is_admin": is_admin(), "site_title": site_settings.site_title, "forums": models.Forum.get_forums(),
            "footer_info": site_settings.footer_info, "langs": m17n.create_lang_table(),
            "version_info": settings.VERSION_INFO + " / " + settings.FOOTER_ADDITIONAL_INFO}


def check_user_key(request, response):
    user_key = models.UserKey.validate(request.cookies.get('display_id'), request.cookies.get('private_key'))
    if request.cookies.get('display_id') != user_key.display_id:
        response.set_cookie('display_id', user_key.display_id, max_age=2147483647)
        response.set_cookie('private_key', user_key.private_key, max_age=2147483647)
    return user_key.display_id


def m17n_process(request, response):
    lang = request.get('lang') or request.cookies.get('lang') or site_settings.default_language
    if lang in m17n.MESSAGE_CATALOG:
        response.set_cookie('lang', lang, max_age=2147483647)
    else:
        lang = site_settings.default_language
    return lang


class HomeHandler(webapp2.RequestHandler):
    def get(self):
        user_key = check_user_key(self.request, self.response)

        context = get_basic_context()
        context["front_page"] = site_settings.front_page

        lang = m17n_process(self.request, self.response)
        context['_'] = m17n.create_m17n_func(lang)
        html = engines[lang].render("home.pyhtml", context)
        self.response.out.write(html)


class ForumHandler(webapp2.RequestHandler):
    def get(self):
        user_key = check_user_key(self.request, self.response)

        context = get_basic_context()

        if self.request.url.find('?') != -1:
            forum_name = urllib.unquote(self.request.url[self.request.url.rfind('/') + 1:self.request.url.rfind('?')])
        else:
            forum_name = urllib.unquote(self.request.url[self.request.url.rfind('/') + 1:])

        forum = models.Forum.get_forum_by_name(forum_name)

        if forum is None:
            self.response.out.write('Forum not found.')
            return  # TODO

        context['forum'] = forum.title
        context['forum_description'] = forum.forum_description
        context['forum_locked'] = forum.locked
        context['page_number'] = int(self.request.get('pn') or 1)
        context['max_page_number'] = (forum.posts_count - 1) / site_settings.default_page_size + 1
        context['is_banned'] = models.BannedIP.is_banned(self.request.remote_addr)

        context['posts'] = forum.query_posts(context['page_number'], site_settings.default_page_size)

        lang = m17n_process(self.request, self.response)
        context['_'] = m17n.create_m17n_func(lang)
        html = engines[lang].render("forum.pyhtml", context)
        self.response.out.write(html)


class ThreadHandler(webapp2.RequestHandler):
    def get(self):
        user_key = check_user_key(self.request, self.response)

        context = get_basic_context()

        if self.request.url.find('?') != -1:
            post_id = urllib.unquote(self.request.url[self.request.url.rfind('/') + 1:self.request.url.rfind('?')])
        else:
            post_id = urllib.unquote(self.request.url[self.request.url.rfind('/') + 1:])
        try:
            post_id = int(post_id)
        except ValueError:
            self.response.out.write('Invalid thread ID.')
            return  # TODO
        forum_name = urllib.unquote(self.request.url[self.request.url.find('/t/') + 3:self.request.url.rfind('/')])

        forum = models.Forum.get_forum_by_name(forum_name)
        if forum is None:
            self.response.out.write('Forum not found.')
            return  # TODO

        post = models.Post.get_by_id(post_id, parent=forum.key)
        if post is None:
            self.response.out.write('Thread not found.')
            return  # TODO

        context['forum'] = forum.title
        context['forum_description'] = forum.forum_description
        context['forum_locked'] = forum.locked
        context['page_number'] = int(self.request.get('pn') or 1)
        context['max_page_number'] = (post.replies_count - 1) / site_settings.default_page_size + 1
        context['is_banned'] = models.BannedIP.is_banned(self.request.remote_addr)

        context['post'] = post.to_dict_on_reply_page(context['page_number'], site_settings.default_page_size)

        lang = m17n_process(self.request, self.response)
        context['_'] = m17n.create_m17n_func(lang)
        html = engines[lang].render("thread.pyhtml", context)
        self.response.out.write(html)


class NewPostHandler(webapp2.RequestHandler):
    def post(self):
        user_key = check_user_key(self.request, self.response)

        if models.BannedIP.is_banned(self.request.remote_addr):
            self.response.write("Banned.")  # TODO
            return

        display_admin = is_admin() and self.request.get('display_admin') != ''

        try:
            forum = models.Forum.get_forum_by_name(self.request.get('forum')).key
        except (AttributeError, IndexError):
            logging.info("AttributeError: Possible Attack")
            self.response.write("No such forum found.")  # TODO
            return

        new_post = models.Post(parent=forum,
                               title=self.request.get('title'), content=self.request.get('content'),
                               po_name=self.request.get('name'),
                               po_id=(display_admin and models.AdminID.get_id(users.get_current_user())) or user_key,
                               po_email=self.request.get('email'), po_ip=self.request.remote_addr, force_saged=False,
                               locked=False, attached_img=None, is_reply=False, replies_count=0, is_admin=display_admin)
        if new_post.check_and_put():
            self.redirect('/f/' + urllib.quote(self.request.get('forum').encode('utf8')))
        else:
            logging.info("Not allowed to post: Possible Attack")  # TODO
            self.response.write("Not allowed to post.")


class NewReplyHandler(webapp2.RequestHandler):
    def post(self):
        user_key = check_user_key(self.request, self.response)

        if models.BannedIP.is_banned(self.request.remote_addr):
            self.response.write("Banned.")  # TODO
            return

        display_admin = is_admin() and self.request.get('display_admin') != ''

        try:
            thread = models.Post.get_by_id(int(self.request.get('id')),
                                           parent=models.Forum.get_forum_by_name(self.request.get('forum')).key).key
        except ValueError:
            self.response.write("Invalid thread ID.")
            return  # TODO
        except (AttributeError, IndexError):
            logging.info("AttributeError: Possible Attack")  # TODO
            self.response.write("No such forum/thread found.")
            return

        new_post = models.Post(parent=thread, title=self.request.get('title'), content=self.request.get('content'),
                               po_name=self.request.get('name'),
                               po_id=(display_admin and models.AdminID.get_id(users.get_current_user())) or user_key,
                               po_email=self.request.get('email'), po_ip=self.request.remote_addr, force_saged=False,
                               locked=False, attached_img=None, is_reply=True, replies_count=0, is_admin=display_admin)

        if new_post.check_and_put():
            self.redirect('/t/' + urllib.quote(self.request.get('forum').encode('utf8')) + '/' + self.request.get('id'))
        else:
            logging.info("Not allowed to post: Possible Attack")  # TODO
            self.response.write("Not allowed to post.")


class FrontendAdminHandler(webapp2.RequestHandler):
    def get(self):
        assert is_admin()

        get_object_funcs = {'thread': models.Post.get_thread_by_key, 'post': models.Post.get_post_by_key,
                            'forum': models.Forum.get_forum_by_name, 'ip': None}

        if self.request.get('type') not in get_object_funcs:
            self.response.write("Unrecognized object.")
            return

        try:
            obj = get_object_funcs[self.request.get('type')](self.request.get('key'))
        except TypeError:
            self.response.write('Illegal action.')
            return
        except IndexError:
            self.response.write('Object not found.')
            return

        actions = obj.get_actions()
        if self.request.get('do') not in actions:
            self.response.write('Illegal action.')
            return

        self.response.write(actions[self.request.get('do')]())

        self.response.write("<script>history.go(-1);</script>")


class AdminHandler(webapp2.RequestHandler):
    def get(self):
        assert is_admin()

        user_key = check_user_key(self.request, self.response)

        context = get_basic_context()
        context["categories"] = models.ForumCategory.get_categories()
        context["display_id"] = models.AdminID.get_id(users.get_current_user())
        context["ban_ip"] = self.request.get("ban_ip")

        lang = m17n_process(self.request, self.response)
        context['_'] = m17n.create_m17n_func(lang)
        html = engines[lang].render("admin.pyhtml", context)
        self.response.out.write(html)

    def post(self):
        assert is_admin()

        if self.request.get('do') == 'create_category':
            category = models.ForumCategory(name=self.request.get('name'), order=int(self.request.get('order')))
            category.put()
        elif self.request.get('do') == 'create_forum':
            forum = models.Forum(parent=ndb.Key(urlsafe=self.request.get('category')), title=self.request.get('title'),
                                 order=int(self.request.get('order')), locked=False, posts_count=0)
            forum.put()
        elif self.request.get('do') == 'set_display_name':
            models.AdminID.update_id(users.get_current_user(), self.request.get('name'))
        elif self.request.get('do') == 'ban_ip':
            if self.request.get('action_type') == '0':
                models.BannedIP.unban(self.request.get('ip'))
            elif self.request.get('action_type') == '1':
                models.BannedIP.ban(self.request.get('ip'), int(self.request.get('duration')))
        self.redirect('/admin/')


app = webapp2.WSGIApplication([
                                  ("/", HomeHandler),
                                  ("/f/.*", ForumHandler),
                                  ("/t/.*", ThreadHandler),
                                  ("/post/.*", NewPostHandler),
                                  ("/reply/.*", NewReplyHandler),
                                  ("/admin/frontend/.*", FrontendAdminHandler),
                                  ("/admin/.*", AdminHandler),
                              ], debug=is_dev)
