import sqlite3
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

#The user class
class User():
	def __init__(self,name,is_active=False,is_authenticated=False):
		self.id = self.get_user_id(name)
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
	def get_user_id(self,user_name):
		query = "SELECT id FROM user WHERE name = '"+user_name+"'"
		print query
		conn = sqlite3.connect('users.db')
		c=conn.cursor()
		c.execute(query)
		id = str(c.fetchone()[0])
		print id
		return id
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
			return False