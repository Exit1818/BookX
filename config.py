CSRF_ENABLED = True
SECRET_KEY = 'com.buaa.exit'

import os
basedir = os.path.abspath(os.path.dirname(__file__))
 
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

BOOK_PER_PAGE = 5
UPLOAD_FOLDER = 'app/static/upload'
img_ext = ['.gif','.jpg','.jpeg','.png','.bmp']