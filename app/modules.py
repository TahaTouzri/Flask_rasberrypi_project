import sqlite3
import forms

def execute_insert_query(query):
	conn = sqlite3.connect('users.db')
	c=conn.cursor()
	c.execute(query)
	conn.commit()
	conn.close()
def execute_select_query(query):
	conn = sqlite3.connect('users.db')
	c=conn.cursor()
	c.execute(query)
	result = str(c.fetchone()[0])
	print "+++++++++++++++++++++++++++++"
	print query
	print result
	if result =="True":
		return True
	elif result =="False":
		return False
	else:
		return str(result)

class Settings():
	def __init__(self,user_id,data=None):
		self.data    = data
		self.user_id = user_id
	def insert_not_update(self):
		query = "SELECT user_id FROM configuration WHERE user_id = '"+str(self.user_id)+"'"
		conn = sqlite3.connect('users.db')
		c=conn.cursor()
		print query
		result = False
		try:
			c.execute(query)
			print str(c.fetchone()[0])
		except:
			result = True
		conn.close()
		return result
	def update_column(self,column):
		query = "UPDATE configuration SET "+column+" = '"+str(self.data[column])+"' WHERE user_id= '"+str(self.user_id)+"';"
		print query
		execute_insert_query(query)
	def insert_into_column(self,column):
		query = "INSERT INTO configuration (user_id,"+column+") VALUES ("+ str(self.user_id)+",'"+str(self.data[column])+"');"
		print query
		execute_insert_query(query)
	def insert_or_update(self,column):
		if self.insert_not_update():
			print "insert new configuration"
			self.insert_into_column(column)
		else:
			print "update existing config"
			self.update_column(column)
	def set_new_login_enable_sms(self):
		self.insert_or_update('new_login_enable_sms')
	def set_new_login_enable_email(self):
		self.insert_or_update('new_login_enable_email')
	def set_temperature_exceed_enable_sms(self):
		self.insert_or_update('temperature_exceed_enable_sms')
	def set_temperature_exceed_enable_email(self):
		self.insert_or_update('temperature_exceed_enable_email')
	def set_temperature_decrease_enable_sms(self):
		self.insert_or_update('temperature_decrease_enable_sms')
	def set_temperature_decrease_enable_email(self):
		self.insert_or_update('temperature_decrease_enable_email')
	def set_door_opened_enable_sms(self):
		self.insert_or_update('door_opened_enable_sms')
	def set_door_opened_enable_email(self):
		self.insert_or_update('door_opened_enable_email')
	def set_window_opened_enable_sms(self):
		self.insert_or_update('window_opened_enable_sms')
	def set_window_opened_enable_email(self):
		self.insert_or_update('window_opened_enable_email')
	def set_temperature_max_val(self):
		self.insert_or_update('temperature_max_val')
	def set_temperature_min_val(self):
		self.insert_or_update('temperature_min_val')
	def update_all(self):
		self.set_new_login_enable_sms()
		self.set_new_login_enable_email()
		self.set_temperature_decrease_enable_sms()
		self.set_temperature_decrease_enable_email()
		self.set_temperature_exceed_enable_sms()
		self.set_temperature_exceed_enable_email()
		self.set_door_opened_enable_sms()
		self.set_door_opened_enable_email()
		self.set_window_opened_enable_sms()
		self.set_window_opened_enable_email()
		self.set_temperature_max_val()
		self.set_temperature_min_val()
	#get methods
	def get_new_login_enable_sms(self):
		query = "SELECT new_login_enable_sms FROM configuration WHERE user_id= '"+ str(self.user_id) + "';"
		return execute_select_query(query)
	def get_new_login_enable_email(self):
		query = "SELECT new_login_enable_email FROM configuration WHERE user_id= '"+ str(self.user_id) + "';"
		return execute_select_query(query)
	def get_temperature_exceed_enable_sms(self):
		query = "SELECT temperature_exceed_enable_sms FROM configuration WHERE user_id= '"+ str(self.user_id) + "';"
		return execute_select_query(query)
	def get_temperature_exceed_enable_email(self):
		query = "SELECT temperature_exceed_enable_email FROM configuration WHERE user_id= '"+ str(self.user_id) + "';"
		return execute_select_query(query)
	def get_temperature_decrease_enable_sms(self):
		query = "SELECT temperature_decrease_enable_sms FROM configuration WHERE user_id= '"+ str(self.user_id) + "';"
		return execute_select_query(query)
	def get_temperature_decrease_enable_email(self):
		query = "SELECT temperature_decrease_enable_email FROM configuration WHERE user_id= '"+ str(self.user_id) + "';"
		return execute_select_query(query)
	def get_door_opened_enable_sms(self):
		query = "SELECT door_opened_enable_sms FROM configuration WHERE user_id= '"+ str(self.user_id) + "';"
		return execute_select_query(query)
	def get_door_opened_enable_email(self):
		query = "SELECT door_opened_enable_email FROM configuration WHERE user_id= '"+ str(self.user_id) + "';"
		return execute_select_query(query)
	def get_window_opened_enable_sms(self):
		query = "SELECT window_opened_enable_sms FROM configuration WHERE user_id= '"+ str(self.user_id) + "';"
		return execute_select_query(query)
	def get_window_opened_enable_email(self):
		query = "SELECT window_opened_enable_email FROM configuration WHERE user_id= '"+ str(self.user_id) + "';"
		return execute_select_query(query)
	def get_window_opened_enable_email(self):
		query = "SELECT window_opened_enable_email FROM configuration WHERE user_id= '"+ str(self.user_id) + "';"
		return execute_select_query(query)
	def get_temperature_max_val(self):
		query = "SELECT temperature_max_val FROM configuration WHERE user_id= '"+ str(self.user_id) + "';"
		return execute_select_query(query)
	def get_temperature_min_val(self):
		query = "SELECT temperature_min_val FROM configuration WHERE user_id= '"+ str(self.user_id) + "';"
		a=execute_select_query(query)
		return execute_select_query(query)
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
