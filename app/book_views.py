#-*- coding:utf-8 -*- 
import os
from flask import request,render_template,g, flash, url_for, redirect, jsonify, make_response
from flask.ext.login import current_user,login_required
from werkzeug.utils import secure_filename
from app import app,db
from datetime import datetime
from models import Book,User,Give
from forms import BookForm
from config import UPLOAD_FOLDER, img_ext
from administrator_views import is_not_admin

@app.route('/book/add', methods = ['GET', 'POST'])
@login_required
def add():
    form = BookForm()
    print form.name.data
    if form.validate_on_submit():
        if b_img:
            b_img = form.imgname.data
        else:
            b_img = 'default.jpg'
        b_name = form.name.data
        b_category = form.category.data
        b_press = form.press.data
        b_author = form.author.data
        b_note = form.note.data
        b = Book(name = b_name,
                img = b_img,
                category = b_category,
                press = b_press,
                author = b_author,
                note = b_note,
                status = False,
                num = 0)
        db.session.add(b)
        db.session.commit()
        if is_not_admin():
            time = datetime.now()
            give = Give(author = g.user.id,
                        book_id = b.id,
                        time = time,
                        status = 0)  
            db.session.add(give)
            db.session.commit()
            flash("添加成功，等待管理员审核")
        return redirect(url_for('info',b_id=b.id))
    
    return render_template('book_add.html',
            g = g,
            form =form)
    

@app.route('/book/<int:b_id>/delete', methods = ['GET', 'POST'])
@login_required
def delete(b_id):
    if is_not_admin():
        return redirect(url_for('info',b_id=b_id))
    b = Book.query.get(b_id)
    if not b:
        return "ERROR!"
    for give in b.gives:
        db.session.delete(give)
    for get in b.gets:
        db.session.delete(get)
    db.session.delete(b)
    db.session.commit()
    flash("删除成功")
    return redirect(url_for('user'))

@app.route('/book/<int:b_id>/ban_book', methods = ['GET', 'POST'])
@login_required
def ban_book(b_id):
    if is_not_admin():
        return redirect(url_for('info',b_id=b_id))
    b = Book.query.get(b_id)
    if not b:
        return "ERROR!"
    b.status = False
    db.session.add(b)
    db.session.commit()
    flash("修改成功")
    return redirect(url_for('info', b_id=b.id))


@app.route('/book/<int:b_id>/info',methods = ['GET','POST'])
def info(b_id):
    b = Book.query.get(b_id)
    if not b:
        return "ERROR!"

    if not b.img:
        b.img = 'default.jpg'
    return render_template('book.html',
            g = g, 
            book = b)


@app.route('/book/<int:b_id>/modify', methods = ['GET', 'POST'])
@login_required
def modify(b_id):
    # if is_not_admin():
    #     return redirect(url_for('info',b_id=b_id))
    b = Book.query.get(b_id)
    if not b:
        return "ERROR!"
    if not b.img:
        b.img = 'default.jpg'
    form = BookForm()
    if form.validate_on_submit():
        b.img = form.imgname.data
        b.name = form.name.data
        b.category = form.category.data
        b.press = form.press.data
        b.author = form.author.data
        b.note = form.note.data
        db.session.add(b)
        db.session.commit()
        flash("修改成功")
        return redirect(url_for('info',b_id=b.id))
    
    return render_template('book_modify.html',
            g = g,
            book = b,
            form = form)


@app.route('/book/<int:b_id>/set', methods = ['GET', 'POST'])
@login_required
def set(b_id):
    if is_not_admin():
        return redirect(url_for('info',b_id=b_id))
    b = Book.query.get(b_id)
    if not b:
        return "ERROR!"
    num = request.args.get('num')
    print num
    b.num = num
    db.session.add(b)
    db.session.commit()
    flash("修改成功")
    return redirect(url_for('info',b_id=b.id))



@app.route('/book/upload', methods = ['POST'])
@login_required
def upload():
    f = request.files['fileList']
    filename = f.filename
    fileExt = os.path.splitext(filename)[1]
    print fileExt
    if fileExt not in img_ext:
        return jsonify(error = 0)
    new_name = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f") + fileExt

    f.save(os.path.join(UPLOAD_FOLDER, new_name))
    return new_name