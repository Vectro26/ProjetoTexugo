# -*- coding: utf-8 -*-

'''
Has the different settings.
'''

import os

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))


DEBUG = True
DEBUG_DATABASE = False
DATABASE_URL = "sqlite:///%s/database.db" % CURRENT_DIR
