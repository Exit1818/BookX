#-*- coding:utf-8 -*- 

from flask import request,render_template, g, flash, url_for, redirect, jsonify 
from flask.ext.login import login_required
from app import app, db
from models import User, Book, Give, Get

def is_not_admin():
    user = g.user
    if not user or not user.is_admin:
        return True
    return False

@app.route('/administrator')
@login_required
def administrator():
    if is_not_admin():
        pass
    else:
        users = User.query.all()
        gives = Give.query.filter_by(status = 0).order_by(Give.time).all()
        new_gets = Get.query.filter_by(status = 0).order_by(Get.time).all()
        send_gets = Get.query.filter_by(status = 1).order_by(Get.time).all()

    return render_template('administrator.html',
        users = users,
        gives = gives,
        new_gets = new_gets,
        send_gets = send_gets
        )

@app.route('/administrator/ban_user/<int:userid>')
@login_required
def ban_user(userid):
    if is_not_admin():
        pass
    else:
        u = User.query.get(userid)
        if not u:
            flash("No such user",'error')
        elif u.is_ban:
            flash("The user has been banned",'error')
        else:
            u.is_ban = True
            db.session.add(u)
            db.session.commit()
            flash("Ban successfully")

    return redirect(url_for('administrator'))

@app.route('/administrator/unban_user/<int:userid>')
@login_required
def unban_user(userid):
    if is_not_admin():
        pass
    else:
        u = User.query.get(userid)
        if not u:
            flash("No such user",'error')
        elif not u.is_ban:
            flash("The user has been unbanned",'error')
        else:
            u.is_ban = False
            db.session.add(u)
            db.session.commit()
            flash("Unban successfully")

    return redirect(url_for('administrator'))


@app.route('/administrator/check_give/<int:g_id>')
@login_required
def check_give(g_id):
    if is_not_admin():
        pass
    else:
        give = Give.query.get(g_id)
        if not give:
            flash("No such give", 'error')
        elif not give.book:
            flash("No such book", 'error')
        else:
            act = request.args.get('act')
            if act == 'pass':
                give.status = 1
                db.session.add(give)
                db.session.commit()
                b = Book.query.get(give.book_id)
                b.status = True
                b.num = b.num + 1
                db.session.add(b)
                db.session.commit()
            elif act =='reject':
                give.status = 2
                db.session.add(give)
                db.session.commit()
                # b = Book.query.get(give.book_id)
                # if b.status == False:
                #     db.session.delete(b)
                #     db.session.commit()
            flash('Action successfully')
    return redirect(url_for('administrator'))

@app.route('/administrator/check_get/<int:g_id>')
@login_required
def check_get(g_id):
    if is_not_admin():
        pass
    else:
        get = Get.query.get(g_id)
        if not get:
            flash("No such get", 'error')
        elif not get.book:
            flash("No such book", 'error')
        else:
            act = request.args.get('act')
            if act == 'pass':
                get.status = 1
                db.session.add(get)
                db.session.commit()
            elif act =='reject':
                get.status = 3
                db.session.add(get)
                db.session.commit()
                b = Book.query.get(get.book_id)
                b.num = b.num + 1
                db.session.add(b)
                db.session.commit()
            flash('Action successfully')
    return redirect(url_for('administrator'))


@app.route('/administrator/confirm_get/<int:g_id>')
@login_required
def confirm_get(g_id):
    if is_not_admin():
        pass
    else:
        get = Get.query.get(g_id)
        if not get:
            flash("No such get", 'error')
        else:
            act = request.args.get('act')
            if act == 'confirm':
                get.status = 2
                db.session.add(get)
                db.session.commit()
            elif act =='cancel':
                get.status = 3
                db.session.add(get)
                db.session.commit()
                b = Book.query.get(get.book_id)
                b.num = b.num + 1
                db.session.add(b)
                db.session.commit()
            flash('Action successfully')
    return redirect(url_for('administrator'))

@app.route('/administrator/getinfo/<int:u_id>', methods = ['GET'])
@login_required
def getinfo(u_id):
    if is_not_admin():
        return jsonify(error=1,message='No root')
    user = User.query.get(u_id)
    if not user:
        return jsonify(error=1,message='No such user')
    userinfo = {'username':user.username, 'mail':user.mail, 'tel':user.tel, 'school':user.school, 'address':user.address}
    return jsonify(userinfo)
