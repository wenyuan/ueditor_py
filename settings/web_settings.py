#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web
from models.article import Article


render = web.template.render('templates', base='base')
web.config.debug = True

config = web.storage(
    site_name='DEMO页面',
    datestr=Article.transform_datestr
)

web.template.Template.globals['config'] = config
web.template.Template.globals['render'] = render
