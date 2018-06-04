#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web
import sqlite3
import datetime

from settings.project_settings import DB_PATH

db = web.database(dbn='sqlite', db=DB_PATH)


class Article(object):

    def __init__(self):
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        try:
            cur.execute(' CREATE TABLE IF NOT EXISTS articles (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, '
                        'content TEXT, posted_on DATETIME )')
            print('Create or open table named articles successfully')
        except Exception as e:
            print('Create table failed')
            print(e)
        finally:
            cur.close()
            con.close()

    @staticmethod
    def get_posts():
        return db.select('articles', order='id desc')

    @staticmethod
    def get_post(id):
        try:
            return db.select('articles', where='id=$id',
                             vars=locals())[0]
        except IndexError:
            return None

    @staticmethod
    def new_post(title, text):
        db.insert('articles', title=title, content=text,
                  posted_on=datetime.datetime.utcnow())

    @staticmethod
    def del_post(id):
        db.delete('articles', where='id=$id', vars=locals())

    @staticmethod
    def update_post(id, title, text):
        db.update('articles', where='id=$id', vars=locals(),
                  title=title, content=text)

    @staticmethod
    def transform_datestr(posted_on):
        datetime_obj = datetime.datetime.strptime(posted_on, '%Y-%m-%d %H:%M:%S.%f')
        return web.datestr(datetime_obj)
