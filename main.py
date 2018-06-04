#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import web

from models.article import Article
from settings.web_settings import render
from apis.ueditor_api import UploadImage, UploadFile, UploadScrawl, GetRemoteImage, UploadVideo, ListImage, ListFile

if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

API_PORT = 12345
urls = (
    '/', 'Index',
    '/view/(\d+)', 'View',
    '/new', 'New',
    '/delete/(\d+)', 'Delete',
    '/edit/(\d+)', 'Edit',
    # '/imgs/(.*)', 'Imgs',
    '/ue_uploadimage', UploadImage,
    '/ue_uploadfile', UploadFile,
    '/ue_uploadscrawl', UploadScrawl,
    '/ue_getremoteimage', GetRemoteImage,
    '/ue_uploadvideo', UploadVideo,
    '/ue_listimage', ListImage,
    '/ue_listfile', ListFile,
    '/upload/(.*)', 'Download'
)


def start_api_server():
    sys.argv.append('0.0.0.0:%s' % API_PORT)
    app = web.application(urls, globals())
    app.run()


class Index(object):

    def GET(self):
        posts = Article.get_posts()
        return render.index(posts)


class View(object):
    def GET(self, id):
        post = Article.get_post(int(id))
        return render.view(post)


class New(object):
    form = web.form.Form(
        web.form.Textbox('title', web.form.notnull,
                         size=30,
                         description=u'文章标题'),
        web.form.Textarea('article_content', web.form.notnull,
                          rows=30, cols=80,
                          description=u'文章内容'),
        web.form.Button(u'提交')
    )

    def GET(self):
        form = self.form()
        return render.new(form)

    def POST(self):
        form = self.form()
        if not form.validates():
            return render.new(form)
        Article.new_post(form.d.title, form.d.article_content)
        raise web.seeother('/')


class Delete(object):
    def POST(self, id):
        Article.del_post(int(id))
        raise web.seeother('/')


class Edit(object):
    def GET(self, id):
        post = Article.get_post(int(id))
        form = New.form()
        form.fill(post)
        return render.edit(post, form)

    def POST(self, id):
        form = New.form()
        post = Article.get_post(int(id))
        if not form.validates():
            return render.edit(post, form)
        Article.update_post(int(id), form.d.title, form.d.content)
        raise web.seeother('/')


class Imgs(object):
    def GET(self, name):
        ext = name.split(".")[-1]
        cType = {
            "png": "images/png",
            "jpg": "images/jpeg",
            "gif": "images/gif",
            "ico": "images/x-icon"
        }
        if name in os.listdir('imgs'):
            web.header("Content-Type", cType[ext])
            return open('imgs/%s' % name, "rb").read()
        else:
            raise web.notfound()


# 访问/upload/这个静态目录
# 这种写法仅测试用,会存在任意文件读取漏洞,详见http://drops.xmd5.com/static/drops/papers-5040.html
class Download(object):

    def GET(self, filepath):
        try:
            with open("./upload/%s" % filepath, "rb") as f:
                content = f.read()
            return content
        except:
            return web.notfound("Sorry, the file you were looking for was not found.")


if __name__ == '__main__':
    article = Article()
    start_api_server()
