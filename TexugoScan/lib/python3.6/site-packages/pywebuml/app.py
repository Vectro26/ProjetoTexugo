# -*- coding: utf-8 -*-

"""
The main module that is used by the web application and by the command that
initilize the database.
"""

from flask import Flask
from flaskext.sqlalchemy import SQLAlchemy
from pywebuml.settings import DATABASE_URL, DEBUG, DEBUG_DATABASE

app = Flask('pywebuml')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_ECHO'] = DEBUG_DATABASE
app.debug = DEBUG    
db = SQLAlchemy(app)
