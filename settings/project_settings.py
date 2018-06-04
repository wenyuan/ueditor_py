#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

BASE_DIR = reduce(lambda x, y: os.path.dirname(x), range(2), os.path.abspath(__file__))

DATA_PATH = os.path.join(BASE_DIR, 'data')
if not os.path.exists(DATA_PATH):
    os.makedirs(DATA_PATH)
DB_PATH = os.path.join(DATA_PATH, 'article.db')

UPLOAD_DIR = os.path.join(BASE_DIR, 'upload')
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

UPLOAD_IMG_DIR = os.path.join(UPLOAD_DIR, 'img')
if not os.path.exists(UPLOAD_IMG_DIR):
    os.makedirs(UPLOAD_IMG_DIR)
UPLOAD_IMG_URL = '/upload/img/'

UPLOAD_FILE_DIR = os.path.join(UPLOAD_DIR, 'file')
if not os.path.exists(UPLOAD_FILE_DIR):
    os.makedirs(UPLOAD_FILE_DIR)
UPLOAD_FILR_URL = '/upload/file/'
