#-*- coding:utf-8 -*- 

from flask import request,render_template,g, flash, url_for, redirect
from flask.ext.login import current_user,login_required
from app import app,db
from models import Book,User
from forms import BookForm
from config import BOOK_PER_PAGE
from administrator_views import is_not_admin


@app.route('/booklist',methods = ['GET','POST'])
@app.route('/booklist/<int:page>',methods = ['GET','POST'])
def booklist(page=1):
    search_category = request.args.get('category')
    if is_not_admin():
        #search_author = request.args.get('author')
        if search_category:
            books = Book.query.filter_by(category = search_category, status = True).paginate(page,BOOK_PER_PAGE,True)
        else:
            books = Book.query.filter_by(status = True).paginate(page,BOOK_PER_PAGE,True)
        return render_template('booklist.html',
                g = g, 
                books = books)
    else:
    	if search_category:
            books = Book.query.filter_by(category = search_category).paginate(page,BOOK_PER_PAGE,True)
        else:
            books = Book.query.paginate(page,BOOK_PER_PAGE,True)
        return render_template('booklist.html',
                g = g, 
                books = books)