import threading
import thread
from logClass import logClass
from iniParser import init
import json
import ast

class ClientSocket(object):
	def __init__(self, socket, adress, server):
		self.id = server.idClient
		self.log = logClass(str(adress[0])+":"+str(adress[1])+" id:"+str(self.id))
		self.socket = socket
		self.admin_rights = False
		self.accept = False
		self.adress = adress
		self.server = server
		self.BUFSIZ = 1024
		self.ini = init("settings.ini")
		self.history = []
		self.broadcasts = ["MAIN"]
		
		thread.start_new_thread(self._run, (self.socket, self.adress))
	
	def _run(self, clientsock, adress):
		while 1:
			data = clientsock.recv(self.BUFSIZ)
			if not data:
				break
			dataArray = data.split('@end');
			for d in dataArray:
				self.log.msg("RAW DATA: "+d, "DATA")
				if d != '\x00':
					self._handleMessage(d)
		self._disconnect()
	
	def _handleMessage(self, data):
		data = data.replace('\x00', '').encode("utf-8")
		self.log.msg("RECIEVED: "+data, "DATA")
		
		try:
			obj_msg = ast.literal_eval(data)
			obj_msg["t"]
		except:
			try:
				obj_msg = ast.literal_eval(json.loads(data.replace('\x00', '')))
			except:
				obj_msg = ast.literal_eval(json.loads(data))
		
		if obj_msg["t"] == 0:
			hsid = self.ini.getSetting("Server", "handshakeid")
			if obj_msg["c"]["hsid"] == hsid:
				self.log.msg("CONNECTION ACCEPTED!", "INFO")
				self.accept = True
				c = {}
				c['s'] = 1
				self.sendMessage( json.dumps(c), 0, self.id)
				
			else:
				self.log.msg("CONNECTION REFUSED!", "INFO")
				c = {}
				c['s'] = 0
				self.sendMessage( json.dumps(c), 0, self.id)
				self._disconnect()
				
		if self.accept:
			if obj_msg["t"] == 1:
				aid = self.ini.getSetting("Server", "adminid")
				if obj_msg["c"]["aid"] == aid:
					self.admin_rights = True
					self.log.msg("AS ADMIN LOGGED IN!", "INFO")
					c = {}
					c['s'] = 1
					self.sendMessage( json.dumps(c), 1, self.id)
				else:
					self.log.msg("ADMIN REFUSED!", "INFO")
					c = {}
					c['s'] = 0
					self.sendMessage( json.dumps(c), 1, self.id)
					self._disconnect()
			elif obj_msg["t"] >= 10 and obj_msg["t"] < 20:
				self._adminFunctions(obj_msg)
			elif obj_msg["t"] == 100:
				self.client_functions(obj_msg["c"])
				
		else:
			c = {}
			self.sendMessage( json.dumps(c), 30, self.id)
			self.log.msg("CONNECTION NEED APPROVAL", "INFO")
		
			
	def _adminFunctions(self, obj_msg):
		if self.admin_rights:
			if obj_msg["t"] == 10:
				if obj_msg["c"]["t"] == 0:
					self.log.msg("GET USERS", "INFO")
					c = {}
					c['s'] = 1
					c['t'] = 0
					c['u'] = []
					for s in self.server.client_socket:
						t = {}
						t['id'] = s.id
						t['a'] = s.adress[0]+":"+str(s.adress[1])
						c['u'].append(t)
						
					self.sendMessage( json.dumps(c), 10, self.id)
				if obj_msg["c"]["t"] == 1:
					self.log.msg("GET ADMINS", "INFO")
					c = {}
					c['s'] = 1
					c['t'] = 1
					c['u'] = []
					for s in self.server.client_socket:
						if s.admin_rights:
							t = {}
							t['id'] = s.id
							t['a'] = s.adress[0]+":"+str(s.adress[1])
							c['u'].append(t)
						
					self.sendMessage( json.dumps(c), 10, self.id)
				
				if obj_msg["c"]["t"] == 2:
					self.log.msg("GET HISTORY", "INFO")
					c = {}
					c['s'] = 1
					c['t'] = 2

					t = {}
					t['id'] = self.server.client_socket[int(obj_msg["c"]["id"])].id
					t['h'] = []
					for h in self.server.client_socket[int(obj_msg["c"]["id"])].history[int(obj_msg["c"]["a"]):]:
						x = {}
						x['t'] = h['type']
						x['s'] = h['sender']
						x['r'] = h['reciever']
						t['h'].append(x)
						
					c['u'] = t
						
					self.sendMessage( json.dumps(c), 10, self.id)
				
				if obj_msg["c"]["t"] == 3:
					self.log.msg("GET USER", "INFO")
					c = {}
					c['s'] = 1
					c['t'] = 3
				
					t = {}
					t['id'] = self.server.client_socket[int(obj_msg["c"]["id"])].id
					t['a'] = self.server.client_socket[int(obj_msg["c"]["id"])].adress[0]+":"+str(self.server.client_socket[int(obj_msg["c"]["id"])].adress[1])
					c['u'] = t
						
					self.sendMessage( json.dumps(c), 10, self.id)
					
			elif obj_msg["t"] == 11:
				if obj_msg["c"]["t"] == 0:
					self.log.msg("SET ADMIN", "INFO")
					try:
						self.server.client_socket[int(obj_msg["c"]["id"])].admin_rights = True
						c = {}
						c['t'] = 0
						c['s'] = 1
						self.sendMessage( json.dumps(c), 11, self.id)
					except:
						c = {}
						c['t'] = 0
						c['s'] = 0
						self.sendMessage( json.dumps(c), 11, self.id)
				if obj_msg["c"]["t"] == 1:
					self.log.msg("SET ACCEPT", "INFO")
					try:
						self.server.client_socket[int(obj_msg["c"]["id"])].accept = True
						c = {}
						c['s'] = 1
						c['s'] = 1
						self.sendMessage( json.dumps(c), 11, self.id)
					except:
						c = {}
						c['t'] = 1
						c['s'] = 0
						self.sendMessage( json.dumps(c), 11, self.id)
				if obj_msg["c"]["t"] == 2:
					#{"t" : 2, "is" : 1, "bc" : "MAIN"}
					#{"t" : 2, "is" : 0, "bc" : "MAIN"}
					self.log.msg("SET BROADCAST", "INFO")
					if obj_msg["c"]["is"] == 1:
						if obj_msg["c"]["bc"] in self.broadcasts:
							c = {}
							c['t'] = 2
							c['s'] = 0
							self.sendMessage( json.dumps(c), 11, self.id)
						else:
							self.broadcasts.append(obj_msg["c"]["bc"])
							c = {}
							c['t'] = 2
							c['s'] = 1
							self.sendMessage( json.dumps(c), 11, self.id)
					else:
						if obj_msg["c"]["bc"] in self.broadcasts:
							self.broadcasts.remove(obj_msg["c"]["bc"])
							c = {}
							c['t'] = 2
							c['s'] = 1
							self.sendMessage( json.dumps(c), 11, self.id)
						else:
							c = {}
							c['t'] = 2
							c['s'] = 0
							self.sendMessage( json.dumps(c), 11, self.id)
					
			elif obj_msg["t"] == 12:
				self.log.msg("STOP THE SERVER", "INFO")
				c = {}
				c['s'] = 1
				self.sendMessage( json.dumps(c), 12, self.id)
				self.server._stop()
			elif obj_msg["t"] == 13:
				self.log.msg("KICK PLAYER "+str(obj_msg["c"]["id"])+" Reason: "+obj_msg["c"]["m"], "INFO")
				self.server.client_socket[int(obj_msg["c"]["id"])].sendMessage(obj_msg["c"]["m"], 32, self.id)	
				self.server.client_socket[int(obj_msg["c"]["id"])]._disconnect()
				c = {}
				c['s'] = 1
				self.sendMessage( json.dumps(c), 13, self.id)
			elif obj_msg["t"] == 14:
				self.log.msg("BAN PLAYER "+str(obj_msg["c"]["id"])+" Reason: "+obj_msg["c"]["m"], "INFO")
				self.server.client_socket[int(obj_msg["c"]["id"])].sendMessage(obj_msg["c"]["m"], 32, self.id)	
				self.server.client_socket[int(obj_msg["c"]["id"])]._disconnect()
				c = {}
				c['s'] = 1
				self.sendMessage( json.dumps(c), 14, self.id)
				#ban function
			elif obj_msg["t"] == 15:
				self.log.msg("KICK ALL", "INFO")
				c = {}
				c['s'] = 1
				c['u'] = []
				for s in self.server.client_socket:
					if s.id != self.id:
						t = {}
						t['id'] = s.id
						c['u'].append(t)
						s._disconnect()					
				self.sendMessage( json.dumps(c), 15, self.id)
			elif obj_msg["t"] == 16:
				self.log.msg("RESTART NOT WORKING", "INFO")
				c = {}
				c['s'] = 1
				self.sendMessage( json.dumps(c), 31, self.id)
			elif obj_msg["t"] == 17:
				self.log.msg("MESSAGE ALL: "+obj_msg["c"]["m"]+"NOT WRKING", "INFO")
				c = {}
				c['s'] = 1
				c['u'] = []
				for s in self.server.client_socket:
					if s.id != self.id:
						t = {}
						t['id'] = s.id
						c['u'].append(t)
						s.sendMessage(obj_msg["c"]["m"])				
				self.sendMessage( json.dumps(c), 17, self.id)
			elif obj_msg["t"] == 18:
				self.log.msg("MESSAGE CLIENT "+ str(obj_msg["c"]["id"]) +" : "+obj_msg["c"]["m"]+" NOT WORKING", "INFO")
				c = {}
				c['s'] = 1
				self.server.client_socket[int(obj_msg["c"]["id"])].sendMessage(obj_msg["c"]["m"], 32, self.id)					
				self.sendMessage( json.dumps(c), 18, self.id)
		else:
			c = {}
			self.sendMessage( json.dumps(c), 30, self.id)
			self.log.msg("ADMIN RIGHTS NEEDED", "INFO")
			
	def sendMessage(self, msg, type, sender):
		h = {}
		h['type'] = type
		h['sender'] = sender
		h['reciever'] = self.id
		self.history.append(h)
		
		self.log.msg("SEND MESSAGE type: "+str(type)+" from "+str(sender), "INFO")
		self.log.msg("SEND MESSAGE DATA: "+msg+" to from "+str(sender), "DATA")
		try:
			self.socket.send('{ "t" : '+str(type)+', "s" : '+str(sender)+' , "c" : '+msg+'}\x00') #pipe error
		except:
			self._disconnect()
		
	def _disconnect(self):
		self.socket.close()
		self.log.msg("DISCONNECTED", "INFO")
		self.server._removeSocket(self)