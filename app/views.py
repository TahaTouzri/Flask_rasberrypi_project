#from gevent.pywsgi import WSGIServer
from flask import Flask, json, Response, render_template,request,redirect,url_for
from flask_login import LoginManager,login_user,login_required,current_user,logout_user
from flask_wtf import validators,form
import sqlite3
import sys
from time import sleep
from jinja2 import Template
from forms import *
from modules import *
from datetime import datetime
#Import the hardware management modules
from hardwareManagement.roomMonitoring import get_room_info_update

# Configure authentication
app = Flask(__name__)
app.secret_key = 'super secret key'
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app)

#the user loader
@login_manager.user_loader
def load_user(id):
	conn = sqlite3.connect('users.db')
	c=conn.cursor()
	# fetch user_name:
	query="SELECT user_name FROM user WHERE id = '"+id+"'"
	c.execute(query)
	user_name = c.fetchone()[0]
	# fetch is_authenticated:
	query="SELECT is_authenticated FROM user WHERE id = '"+id+"'"
	c.execute(query)
	is_authenticated = c.fetchone()[0]
	# fetch is_active:
	query="SELECT is_active FROM user WHERE id = '"+id+"'"
	c.execute(query)
	is_active = c.fetchone()[0]
	#close connection:
	conn.close()

	is_active = 0
	if is_active == 1:
		is_active = True
	else:
		is_active = False
	if is_authenticated == 1:
		is_authenticated = True
	else:
		is_authenticated =False
	user= User(user_name,is_active,is_authenticated)
	return user

@app.route('/login.html', methods=['POST'])
def login():
	def next_is_valid(next):
		#seems like we don't have specific permissions for specific users for now
		#this is why we just return True
		#this may changes in the future
		#looks like:since you are redirecting to hard codded urls, your app is not vulnurable to
		#the url redirect attack, but you need to be more sure about this!!, see the link bellow for more information:
		# https://www.owasp.org/index.php/Unvalidated_Redirects_and_Forwards_Cheat_Sheet
		return True
	# Here we use a class of some kind to represent and validate our
	# client-side form data. For example, WTForms is a library that will
	# handle this for us, and we use a custom LoginForm to validate.
	#form = LoginForm()
	form=loginForm(request.form)
	if request.method == 'POST' and form.validate():
		user_name = form.username.data
		password  = form.password.data
		if next_is_valid("next"):
			try:
				user=User(user_name)
			except:
				return render_template('login.html', form=form,error_message="invalid user name or password")
			if user.get_password()==password:
				user.set_authenticated(True)
				login_user(user)
			else:
				return render_template('login.html', form=form,error_message="invalid user name or password")
		else:
			return render_template('login.html', form=form,error_message="you have no permissions to access this page")
		return render_template('welcome.html', name=user.get_name())
	else:
		return render_template('login.html', form=form,error_message="check your user name or password ++")

@app.route('/')
@app.route('/login.html')
def first_login():
	return render_template("/login.html",error_message="")

#We need to add that it is authenticated decorator
@app.route('/home.html')
@app.route('/bathroom.html')
@app.route('/bedroom.html')
@app.route('/room1.html')
@app.route('/room2.html')
@app.route('/kitchen.html')
@login_required
def room():
	room = str(request.url_rule)[1:]
	return render_template('room.html', room=room)

@app.route('/menu.html')
@app.route('/welcome.html')
@app.route('/account.html')
@app.route('/security.html')
@app.route('/profile.html')
@login_required
def pages():
	rule = str(request.url_rule)
	user = current_user
	user_name = user.user_name
	name = user.get_name()#"name is not user_name"
	#need to update class user and to get data same way as user_name
	phone_number  = user.get_phone_number()#"71 000 111"
	mobile_number = user.get_mobile_number()#"94 387 918"
	email         = user.get_email()#"touzritaha@gmail.com"
	date_of_birth = user.get_date_of_birth()#"1989-08-05"
	gender        = user.get_gender()#"Male"
	home_address  = user.get_home_address()#"Fahs"
	#home_time     = "14/01/2011"
	home_time     = str(datetime.now().date())
	return render_template(rule[1:],user_name=user_name,name=name,phone_number=phone_number,
						   mobile_number=mobile_number,email=email,date_of_birth=date_of_birth,
						  gender=gender,home_address=home_address,home_time=home_time)


@app.route('/settings.html',methods=['GET','POST'])
@login_required
def settings():
	user = current_user
	if request.method == 'POST':
		form=settingsForm(request.form)
		settings = Settings(user.get_id(),form.data)
		#save new settings to database
		settings.update_all()
	else:
		#render the form
		form = settingsForm(request.form)
		#get the form values from the database
		settings=Settings(user.get_id())
	return render_template('settings.html',form=form,settings=settings)
@app.route('/edit_profile.html', methods=['GET','POST'])
@login_required
def edit_profile():
	user = current_user
	if request.method == 'POST':
		form = request.form
		print "-------------------------------------"
		print "-------------------------------------"
		user.update(form)
	#get new data from database if the user is update by a post request
	#otherways get old data
	user_name = user.user_name
	name = user.get_name()#"name is not user_name"
	#need to update class user and to get data same way as user_name
	phone_number  = user.get_phone_number()#"71 000 111"
	mobile_number = user.get_mobile_number()#"94 387 918"
	email         = user.get_email()#"touzritaha@gmail.com"
	date_of_birth = user.get_date_of_birth()#"1989-08-05"
	gender        = user.get_gender()#"Male"
	home_address  = user.get_home_address()#"Fahs"
	#home_time     = "14/01/2011"
	home_time     = str(datetime.now().date())
	return render_template('edit_profile.html',user_name=user_name,name=name,phone_number=phone_number,
						   mobile_number=mobile_number,email=email,date_of_birth=date_of_birth,
						  gender=gender,home_address=home_address,home_time=home_time)




@app.route("/logout.html", methods=['GET', 'POST'])
@login_required
def logout():
	print "in the logout view"
	user = current_user
	user.set_authenticated(False)
	logout_user()
	print "logged out user"
	return redirect('/login.html')

# those methods are for SSE

#update room status
def event(room,user_id):
	sse_connection = sseConnection(user_id)
	while(True):
		data = get_room_info_update(room)
		ev   = ServerSentEvent(data)
		yield ev.encode()

@app.route('/stream', methods=['GET', 'POST'])
@app.route('/stream/<room>', methods=['GET', 'POST'])
@login_required
def stream(room=None):
	user_id = current_user.get_id()
	return Response(event(room,user_id), mimetype="text/event-stream")

#update time date


if __name__ == "__main__":
	app.debug = True
	app.run(threaded=True)
