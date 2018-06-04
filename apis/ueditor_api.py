#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import uuid
import urllib2
import os
import web

from settings.project_settings import UPLOAD_IMG_DIR, UPLOAD_FILE_DIR, UPLOAD_IMG_URL


# def listImage(rootDir, retlist):
#     for cfile in os.listdir(rootDir):
#         path = os.path.join(rootDir, cfile)
#         if os.path.isdir(path):
#             listImage(path, retlist)
#         else:
#             if cfile.endswith('.gif') or cfile.endswith('.png') or cfile.endswith('.jpg') or cfile.endswith('.bmp'):
#                 retlist.append('/static/upload/' + cfile)
#
#
# def saveUploadFile(fileName, content):
#     fileName = fileName.replace('\\', '/') # replaces the windows-style slashes with linux ones.
#     fout = open(UPLOAD_FILE_DIR + '/' + fileName, 'wb') # creates the file where the uploaded file should be stored
#     fout.write(content) # writes the uploaded file to the newly created file.
#     fout.close() # closes the file, upload complete.


def save_upload_img(img_path, content):
    with open(img_path, 'wb+') as destination:
        destination.write(content)


class UploadImage(object):

    def POST(self):
        post_data = web.input(upfile={}, pictitle="")
        file_obj = post_data.upfile
        pic_title = post_data.pictitle
        old_filename = file_obj.filename
        ext = '.' + old_filename.split('.')[-1]
        new_filename = str(uuid.uuid1()) + ext
        img_path = os.path.join(UPLOAD_IMG_DIR, new_filename)
        save_upload_img(img_path, file_obj.file.read())

        response = {
            "state": "SUCCESS",
            "url": UPLOAD_IMG_URL + new_filename,
            "title": pic_title,
            "fileType": ext,
            "original": old_filename
        }
        return response


class ListImage(object):

    def GET(self):
        req_data = web.input()
        start = req_data['start']
        size = req_data['size']
        # list_files = listImage(UPLOAD_IMG_DIR)

    def POST(self):
        reqData = web.input()
        if 'action' in reqData:
            if reqData.action == 'get':
                list_files = []
                # listImage(UPLOAD_FILE_DIR, retfiles)
                # htmlContent = "ue_separate_ue".join(retfiles)
                return htmlContent

class UploadFile(object):
    def GET(self):
        web.header("Content-Type", "text/html; charset=utf-8")
        return ""

    def POST(self):
        postData = web.input(upfile={})
        fileObj = postData.upfile
        fileName = postData.Filename
        ext = '.' + fileName.split('.')[-1]
        #web.py的static目录对中文文件名不支持，会404
        newFileName = str(uuid.uuid1()) + ext
        #fileNameFormat = postData.fileNameFormat
        # saveUploadFile(newFileName, fileObj.file.read())
        return "{'url':'" + UPLOAD_FILE_DIR + '/' + newFileName + "','fileType':'" + ext + "','original':'" + fileName + "','state':'" + "SUCCESS" + "'}"


class UploadScrawl(object):
    def GET(self):
        web.header("Content-Type", "text/html; charset=utf-8")
        return ""

    def POST(self):
        reqData = web.input(upfile={})
        if 'action' in reqData:
            if reqData.action == 'tmpImg':
                #上传背景
                fileObj = reqData.upfile
                fileName = fileObj.filename
                # saveUploadFile(fileName, fileObj.file.read())
                return "<script>parent.ue_callback(" + UPLOAD_FILE_DIR + '/' + fileName + "','" + "SUCCESS" + "')</script>"
        else:
            base64Content = reqData.content
            fileName = str(uuid.uuid1()) + '.png'
            # saveUploadFile(fileName, base64.decodestring(base64Content))
            return "{'url':'" + UPLOAD_FILE_DIR + '/' + fileName + "',state:'" + "SUCCESS" + "'}"


class GetRemoteImage(object):
    def GET(self):
        web.header("Content-Type", "text/html; charset=utf-8")
        return ""

    def POST(self):
        postData = web.input()
        urls = postData.upfile
        #urls = urls.replace('&amp','&')
        urllist = urls.split("ue_separate_ue")
        fileType = [".gif", ".png", ".jpg", ".jpeg", ".bmp"]
        outlist = []
        for fileurl in urllist:
            if not fileurl.startswith('http'):
                continue
            ext = "." + fileurl.split('.')[-1]
            web.debug(ext + "|" + fileurl)
            if ext in fileType:
                fileName = str(uuid.uuid1()) + ext
                # saveUploadFile(fileName, urllib2.urlopen(fileurl).read())
                outlist.append(UPLOAD_FILE_DIR + "/" + fileName)
        outlist = "ue_separate_ue".join(outlist)
        return "{'url':'" + outlist + "','tip':'远程图片抓取成功！','srcUrl':'" + urls + "'}"


class UploadVideo(object):
    def POST(self):
        reqData = web.input()
        skey = reqData.searchKey
        vtype = reqData.videoType
        surl = 'http://api.tudou.com/v3/gw?method=item.search&appKey=myKey&format=json&kw=' + skey + '&pageNo=1&pageSize=20&channelId=' + vtype + '&inDays=7&media=v&sort=s'
        htmlContent = urllib2.urlopen(surl).read()
        web.debug(htmlContent)
        return htmlContent


class ListFile(object):
    def POST(self):
        reqData = web.input()
        if 'action' in reqData:
            if reqData.action == 'get':
                retfiles = []
                # listImage(UPLOAD_FILE_DIR, retfiles)
                htmlContent = "ue_separate_ue".join(retfiles)
                return htmlContent
