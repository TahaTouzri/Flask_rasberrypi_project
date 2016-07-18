import sqlite3
import forms

class Settings():
	def __init__(self,settingsForm,user_id):
		self.data    = settingsForm.data
		self.user_id = user_id
	def insert_not_update(self):
		query = "SELECT user_id FROM configuration WHERE user_name = '"+str(self.user_id)+"'"
		conn = sqlite3.connect('users.db')
		c=conn.cursor()
		result = False
		try:
			c.execute(query)
		except:
			result = True
		conn.close()
		return result
	def set_new_login_enable_sms(self):
		if self.insert_not_update():
			print "insert not update"
			query =
		else:
			print "update existing config"
			query = 

	def set_new_login_enable_email(self):
		pass
	def set_temperature_exceed_enable_sms(self):
		pass
	def set_temperature_exceed_enable_email(self):
		pass
	def set_temperature_decrease_enable_sms(self):
		pass
	def set_temperature_decrease_enable_email(self):
		pass
	def set_door_opened_enable_sms(self):
		pass
	def set_door_opened_enable_email(self):
		pass
	def set_window_opened_enable_sms(self):
		pass
	def set_window_opened_enable_email(self):
		pass
	def update_all(self):
		print "---------------------------------"
		print self.user_id
		print self.data['new_login_enable_sms']
		print self.data['new_login_enable_email']
		print self.data['temperature_exceed_enable_sms']
		print self.data['temperature_exceed_enable_email']
		print self.data['temperature_decrease_enable_sms']
		print self.data['temperature_decrease_enable_email']
		print self.data['door_opened_enable_sms']
		print self.data['door_opened_enable_email']
		print self.data['window_opened_enable_sms']
		print self.data['window_opened_enable_email']
		self.set_new_login_enable_sms()
#The user class
class User():
	def __init__(self,user_name,is_active=False,is_authenticated=False):
		self.id = self.get_user_id(user_name)
		self.user_name = user_name
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
	def get_id(self):
		return self.id
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
	def get_user_id(self,user_name):
		print "------------------------------------"
		print user_name
		query = "SELECT id FROM user WHERE user_name = '"+user_name+"'"
		conn = sqlite3.connect('users.db')
		c=conn.cursor()
		c.execute(query)
		id = str(c.fetchone()[0])
		return id
	def get_name(self):
		query = "SELECT name FROM user WHERE user_name = '"+self.user_name+"'"
		conn = sqlite3.connect('users.db')
		c=conn.cursor()
		c.execute(query)
		name = str(c.fetchone()[0])
		return name
	def get_phone_number(self):
		query = "SELECT phone_number FROM user WHERE user_name = '"+self.user_name+"'"
		conn = sqlite3.connect('users.db')
		c=conn.cursor()
		c.execute(query)
		phone_number = str(c.fetchone()[0])
		return phone_number
	def get_mobile_number(self):
		query = "SELECT mobile_number FROM user WHERE user_name = '"+self.user_name+"'"
		conn = sqlite3.connect('users.db')
		c=conn.cursor()
		c.execute(query)
		mobile_number = str(c.fetchone()[0])
		return mobile_number
	def get_name(self):
		query = "SELECT name FROM user WHERE user_name = '"+self.user_name+"'"
		conn = sqlite3.connect('users.db')
		c=conn.cursor()
		c.execute(query)
		name = str(c.fetchone()[0])
		return name
	def get_date_of_birth(self):
		query = "SELECT date_of_birth FROM user WHERE user_name = '"+self.user_name+"'"
		conn = sqlite3.connect('users.db')
		c=conn.cursor()
		c.execute(query)
		date_of_birth = str(c.fetchone()[0])
		return date_of_birth
	def get_gender(self):
		query = "SELECT gender FROM user WHERE user_name = '"+self.user_name+"'"
		conn = sqlite3.connect('users.db')
		c=conn.cursor()
		c.execute(query)
		gender = str(c.fetchone()[0])
		return gender
	def get_home_address(self):
		query = "SELECT home_address FROM user WHERE user_name = '"+self.user_name+"'"
		conn = sqlite3.connect('users.db')
		c=conn.cursor()
		c.execute(query)
		home_address = str(c.fetchone()[0])
		return home_address
	def get_email(self):
		query = "SELECT email FROM user WHERE user_name = '"+self.user_name+"'"
		conn = sqlite3.connect('users.db')
		c=conn.cursor()
		c.execute(query)
		email = str(c.fetchone()[0])
		return email
	def get_password(self):
		query = "SELECT password FROM user WHERE user_name = '"+self.user_name+"'"
		conn = sqlite3.connect('users.db')
		c=conn.cursor()
		c.execute(query)
		password = str(c.fetchone()[0])
		return password
	def update(self,form):
		user_name 	  = form["user_name"]
		name      	  = form["name"]
		phone_number  = form["phone_number"]
		mobile_number = form["mobile_number"]
		email         = form["email"]
		date_of_birth = form["date_of_birth"]
		#gender        = form["gender"]
		home_address  = form["home_address"]
		print form
#server sent event class
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
#sseConnection class
class sseConnection():
	def __init__(self,user_id):
		self.user_id = user_id
		query        = "INSERT INTO sse_connection (user_id) VALUES ("+ str(user_id)+");"
		conn         = sqlite3.connect('users.db')
		c            =conn.cursor()
		c.execute(query)
		conn.commit()
		query        = "SELECT MAX(connection_id) FROM sse_connection WHERE user_id = "+str(self.user_id)+";"
		c.execute(query)
		self.connection_id = str(c.fetchone()[0])
		conn.close()
	def is_active(self):
		query = "SELECT MAX(connection_id) FROM sse_connection WHERE user_id = "+str(self.user_id)+";"
		conn = sqlite3.connect('users.db')
		c=conn.cursor()
		c.execute(query)
		active_connection_id = str(c.fetchone()[0])
		if active_connection_id == self.connection_id:
			return True
		else:
			self.delete_connection()
			return False
	def delete_connection(self):
		query ="DELETE FROM sse_connection WHERE connection_id="+self.connection_id+";"
		print query
		conn = sqlite3.connect('users.db')
		c=conn.cursor()
		c.execute(query)
		conn.commit()
		conn.close()
