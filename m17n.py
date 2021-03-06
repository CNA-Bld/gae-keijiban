# -*- coding: utf-8 -*-

# Copyright 2014 CNA_Bld & AngelaTang @ SSHZ.ORG
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


MESSAGE_CATALOG = {
    'en': {'_lang': 'English',
           'Admin': 'Admin',
           'Name': 'Name',
           'Email': 'Email',
           'Title': 'Title',
           'Submit': 'Submit',
           'Emoticon': 'Emoticon',
           'None': 'None',
           'Content': 'Content',
           'Attachment': 'Attachment',
           'No Title': 'No Title',
           'Anonymous': 'Anonymous',
           'No Content': 'No Content',
           'Reply': 'Reply',
           'First Page': 'First Page',
           'Next Page': 'Next Page',
           'Last Page': 'Last Page',
           'Delete': 'Delete',
           'Execute': 'Execute',
           'Index': 'Index',
           'Ban IP': 'Ban IP',
           'Sage': 'Sage',
           'Force Sage': 'Force Sage',
           'UnSage': 'UnSage',
           'Forum Index': 'Forum Index',
           'Lock Forum': 'Lock Forum',
           'Unlock Forum': 'Unlock Forum',
           'Delete Forum': 'Delete Forum',
           'This post has been force SAGEd': 'This post has been force SAGE\'d',
           'This post has been locked': 'This post has been locked',
           'This forum has been locked': 'This forum has been locked',
           'There are %d replies not displaying. Please click Reply link to view all replies.': 'There are %d replies not displaying. Please click Reply link to view all replies.',
           'Display Admin ID': 'Display Admin ID',
           'Lock': 'Lock',
           'Unlock': 'Unlock',
           'Posting new thread on forum.': 'Posting new thread on forum.',
           'Replying to thread.': 'Replying to thread.',
           'Your IP is now banned.': 'Your IP is now banned.',
           },
    'zh': {'_lang': '中文',
           'Admin': '管理',
           'Name': '名稱',
           'Email': 'Email',
           'Title': '題名',
           'Submit': '送出',
           'Emoticon': '顏文字',
           'None': '無',
           'Content': '正文',
           'Attachment': '附加圖檔',
           'No Title': '無題',
           'Anonymous': '無名',
           'No Content': '無本文',
           'Reply': '回應',
           'First Page': '最前頁',
           'Next Page': '下一頁',
           'Last Page': '最後頁',
           'Delete': '刪除',
           'Execute': '執行',
           'Index': '首頁',
           'Ban IP': '封 IP',
           'Sage': 'Sage',
           'Force Sage': '強制 Sage',
           'UnSage': '解除 Sage',
           'Forum Index': '版塊首頁',
           'Lock Forum': '鎖定板塊',
           'Unlock Forum': '解鎖板塊',
           'Delete Forum': '刪除板塊',
           'This post has been force SAGEd': '該串已被強制 SAGE',
           'This post has been locked': '該串已被鎖定',
           'This forum has been locked': '該版已被鎖定',
           'There are %d replies not displaying. Please click Reply link to view all replies.': '回應有 %d 篇被省略。要閱讀所有回應請按下回應連結。',
           'Display Admin ID': '顯示管理員 ID（紅名）',
           'Lock': '鎖定',
           'Unlock': '解鎖',
           'Posting new thread on forum.': '正在發送新串。',
           'Replying to thread.': '正在發送回應。',
           'Your IP is now banned.': '你的 IP 已被封禁。'
           },
}


def create_m17n_func(lang):
    dct = MESSAGE_CATALOG.get(lang)
    if not dct:
        raise ValueError("%s: unknown lang." % lang)
    return dct.get


def create_lang_table():
    lang_table = [{'code': lang, 'name': MESSAGE_CATALOG[lang]['_lang']} for lang in MESSAGE_CATALOG]
    return lang_table
