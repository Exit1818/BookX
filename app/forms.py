#coding=utf-8
from flask.ext.wtf import Form
from wtforms import TextField
from wtforms import PasswordField
from wtforms import FloatField
from wtforms import BooleanField
from wtforms.validators import Required

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class LoginForm(Form):
	username = TextField('用户名', validators = [Required()])
	password = PasswordField('密码', validators = [Required()])

class RegisterForm(Form):
	username = TextField('用户名', validators = [Required()])
	password = PasswordField('密码', validators = [Required()])
	password_again = PasswordField('确认密码', validators = [Required()])
	mail = TextField('邮箱', validators = [Required()])
	tel = TextField('手机', validators = [Required()])
	school = TextField('学校', validators = [Required()])
	address = TextField('地址', validators = [Required()])

class BookForm(Form):
	imgname = TextField('imgname')
	name = TextField('书籍名称', validators = [Required()])
	author = TextField('作者', validators = [Required()])
	category = TextField('书籍类别', validators = [Required()])
	press = TextField('出版社', validators = [Required()])
	note = TextField('是否有批注/笔记')