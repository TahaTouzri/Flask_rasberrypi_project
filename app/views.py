#from gevent.pywsgi import WSGIServer
from flask import Flask, json, Response, render_template,request,redirect,url_for
from flask_login import LoginManager,login_user,login_required,current_user,logout_user
from flask_wtf import validators,form
import sqlite3
import sys
from time import sleep
from jinja2 import Template
from forms import *
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
	query = "SELECT * FROM user WHERE id = "+id
	c.execute(query)
	data = c.fetchone()
	conn.close()
	id = data[0]
	name = data[1]
	is_authenticated = data[2]
	#is_active = data[3]
	is_active = 0
	if is_active == 1:
		is_active = True
	else:
		is_active = False
	if is_authenticated == 1:
		is_authenticated = True
	else:
		is_authenticated =False
	user= User(name,is_active,is_authenticated)
	return user
	
@app.route('/login.html', methods=['POST'])
def login():
	def clean_db(user):
		query ="DELETE FROM sse_connection WHERE user_id="+user.get_id()+";"
		print query
		conn = sqlite3.connect('users.db')
		c=conn.cursor()
		c.execute(query)
		conn.commit()
		conn.close()
	def next_is_valid(next):
		return False
	# Here we use a class of some kind to represent and validate our
	# client-side form data. For example, WTForms is a library that will
	# handle this for us, and we use a custom LoginForm to validate.
	#form = LoginForm()
	form = request.form
	print form
	"""
	if True:#form.validate_on_submit():
		# Login and validate the user.
		# user should be an instance of your `User` class
		#login_user(user)
		next = request.args.get('next')
		# next_is_valid should check if the user has valid
		# permission to access the `next` url
		if not next_is_valid(next):
			return flask.abort(400)
		print next
		print "redirect to after login"
	"""
	user_name = form["username"]
	password  = form["password"]
	print user_name
	print password
	#id        = get_user_id(user_name)
	user=User(user_name)
	if True:#user_name=="taha":
		user.set_authenticated(True)
		#login the user
		login_user(user)
		#clean database
		clean_db(user)
		print "user logged in successfully"
		return redirect('/welcome.html')
	print "redering login.html"
	return render_template('login.html', form=form)

@app.route('/')
@app.route('/login.html')
def first_login():
	return render_template("/login.html")	

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
	name = user.name
	user_name = "user name"
	#need to update class user and to get data same way as user_name
	phone_number  = "71 000 111"
	mobile_number = "94 387 918"
	email         = "touzritaha@gmail.com"
	date_of_birth = "04/08/1989"
	gender        = "Male"
	home_address  = "Fahs"
	#home_time     = "14/01/2011"
	home_time     = str(datetime.now().date())
	return render_template(rule[1:],user_name=user_name,name=name,phone_number=phone_number,
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
#@login_required
def stream(room=None):
	user_id = current_user.get_id()
	return Response(event(room,user_id), mimetype="text/event-stream")

#update time date
	

if __name__ == "__main__":
	app.debug = True
	app.run(threaded=True)