from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

import os
from flask.ext.login import LoginManager

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

from app import user_auth_views, user_views, book_views, book_list_views, administrator_views, models, forms