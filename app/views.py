from gevent.pywsgi import WSGIServer
from flask import Flask, json, Response, render_template,request,redirect
from flask_login import LoginManager,login_user
from flask_wtf import validators,form
import sqlite3
from random import randint
from time import sleep
from jinja2 import Template

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

#in the login branch

class ServerSentEvent(object):
	def __init__(self, data):
		self.data = data
		self.event = None
		self.id = None
		self.desc_map = {
			self.data : "data",
			self.event : "event",
			self.id : "id"
		}

	def encode(self):
		if not self.data:
			return ""
		lines = ["%s: %s" % (v, k) for k, v in self.desc_map.iteritems() if k]
		return "%s\n\n" % "\n".join(lines)

#The user class
class User():
	def __init__(self, id,name,is_active=False,is_authenticated=False):
		self.id = id
		self.name = name
		self.active = is_active
		self.authenticated = is_authenticated
	def is_active(self):
		# Here you should write whatever the code is
		# that checks the database if your user is active
		return self.active
	def is_anonymous(self):
		return False
	def is_authenticated(self):
		return self.authenticated
	def get_id(self):
		return self.id
	def set_authenticated(self,authentication):
		if authentication:
			query = "UPDATE user SET is_authenticated = 1 WHERE id= "+str(self.id)
			self.authenticated = True
		else:
			query = "UPDATE user SET is_authenticated = 0 WHERE id= "+str(self.id)
			self.authenticated = False
		conn = sqlite3.connect('users.db')
		c=conn.cursor()
		c.execute(query)
		conn.commit()
		conn.close()
	def set_active(self,active):
		if active:
			query = "UPDATE user SET is_active = 1 WHERE id= "+str(self.id)
			self.active = True
		else:
			query = "UPDATE user SET is_active = 0 WHERE id= "+str(self.id)
			self.active = False
		conn = sqlite3.connect('users.db')
		c=conn.cursor()
		c.execute(query)
		conn.commit()
		conn.close()	
#the user loader
@login_manager.user_loader
def load_user(id):
	conn = sqlite3.connect('users.db')
	c=conn.cursor()
	query = "SELECT * FROM user WHERE id = "+id
	c.execute(query)
	data = c.fetchone()
	conn.close()
	name = data[1]
	id   = data[0]
	print name
	user= User(name,id)
	return user
	
@app.route('/login.html', methods=['GET', 'POST'])
def login():
	def next_is_valid(next):
		return True
	# Here we use a class of some kind to represent and validate our
	# client-side form data. For example, WTForms is a library that will
	# handle this for us, and we use a custom LoginForm to validate.
	#form = LoginForm()
	print "in the login view"
	if True:#form.validate_on_submit():
		# Login and validate the user.
		# user should be an instance of your `User` class
		#login_user(user)
		print "before get next"
		print request
		print request.args
		next = request.args.get('next')
		print "-----------------"
		print next
		# next_is_valid should check if the user has valid
		# permission to access the `next` url
		if not next_is_valid(next):
			return flask.abort(400)
		print next
		print "redirect to after login"
	return redirect('/welcome.html')
	#return flask.render_template('login.html', form=form)

@app.route('/')
def first_login():
	return render_template("/login.html")	

#We need to add that it is authenticated decorator
@app.route('/home.html')
@app.route('/bathroom.html')
@app.route('/bedroom.html')
@app.route('/room1.html')
@app.route('/room2.html')
@app.route('/kitchen.html')
def room():
	room = str(request.url_rule)[1:]
	return render_template('room.html', room=room)

@app.route('/menu.html')
@app.route('/welcome.html')
def pages():
	rule = str(request.url_rule)
	return render_template(rule[1:])
	
# those methods are for SSE
def event():
	while(True):
		ev = ServerSentEvent(str(randint(0,45)))
		yield ev.encode()
		sleep(1)
@app.route('/stream/', methods=['GET', 'POST'])
def stream():
	return Response(event(), mimetype="text/event-stream")
	

if __name__ == "__main__":
	app.debug = True
	app.run(threaded=True)