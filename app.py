from flask import Flask, render_template, redirect, request, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
import os
from config import DevelopmentConfig
#database library
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

#app.config.from_object(os.environ['APP_SETTINGS'])
app.config.from_object(DevelopmentConfig())
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class userId1(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	userid = db.Column(db.String(50), unique=True)
	password = db.Column(db.String(50))
	#constructor to introduce values
	def __init__(self, userid, password):
		self.userid = userid
		self.password = password

class login_form(FlaskForm):
	userId = StringField('userId', validators = [DataRequired()], render_kw = {'autocomplete':'off'})
	password = PasswordField('password', validators = [DataRequired()])
	submit = SubmitField('Submit')

@app.route('/login', methods=['GET', 'POST'])
def user_login():
	form = login_form();
	if(request.method == 'POST'):
		#logic for database validation
		user_data = userId1(str(form.userId.data),str(form.password.data))
		db.session.add(user_data)
		db.session.commit()
		return render_template('user.html',name = form.userId.data)
	return render_template('login.html', form = form)
