import socket
import iniParser
from logClass import logClass
import json
import ast

class MyAdmin(object):
	def __init__(self, adress, handshakeId, adminId):
		self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.log = logClass("ADMIN")
		
		try:
			self.clientsocket.connect(adress)	
			self.log.msg("CONNECTED", "INFO")
			
			msg = {}
			msg['hsid'] = hsid
			self.sendMessage(msg, 0)
			
			loop = True
		except:
			self.log.msg("COULD NOT CONNECT TO "+str(adress[0])+":"+str(adress[1]), "WARNING")
			loop = False
				
		while loop:
			action = raw_input('ADMIN > ')
			
			waitForServer = True
			
			if action == 'handshake':
				msg = {}
				msg['hsid'] = hsid
				self.sendMessage(msg, 0)
			elif action == 'admin':
				msg = {}
				msg['aid'] = aid
				self.sendMessage(msg, 1)
			elif action == 'get':
				secondAction = raw_input('Get what? > ')
				if secondAction == "users":
					msg = {}
					msg["t"] = 0
					self.sendMessage(msg, 10)
				if secondAction == "admins":
					msg = {}
					msg["t"] = 1
					self.sendMessage(msg, 10)
				if secondAction == "history":
					thirdAction = raw_input('ID? > ')
					fourthAction = raw_input('amount (negative)? > ')
					msg = {}
					msg["t"] = 2
					msg["id"] = thirdAction
					msg["a"] = fourthAction
					self.sendMessage(msg, 10)
				if secondAction == "user":
					thirdAction = raw_input('ID? > ')
					msg = {}
					msg["t"] = 3
					msg["id"] = thirdAction
					self.sendMessage(msg, 10)
			elif action == 'set':
				secondAction = raw_input('Set what? > ')
				if secondAction == "admin":
					thirdAction = raw_input('ID? > ')
					msg = {}
					msg["t"] = 0
					msg["id"] = thirdAction
					self.sendMessage(msg, 11)
				if secondAction == "accept":
					thirdAction = raw_input('ID? > ')
					msg = {}
					msg["t"] = 1
					msg["id"] = thirdAction
					self.sendMessage(msg, 11)
			elif action == 'stop':
				msg = {}
				self.sendMessage(msg, 12)
				loop = False
			elif action == 'kick':
				secondAction = raw_input('ID? > ')
				thirdAction = raw_input('REASON? > ')
				msg = {}
				msg['id'] = secondAction
				msg['m'] = thirdAction
				self.sendMessage(msg, 13)
			elif action == 'ban':
				secondAction = raw_input('ID? > ')
				thirdAction = raw_input('REASON? > ')
				msg = {}
				msg['id'] = secondAction
				msg['m'] = thirdAction
				self.sendMessage(msg, 14)
			elif action == 'kickall':
				thirdAction = raw_input('REASON? > ')
				msg = {}
				msg['m'] = thirdAction
				self.sendMessage(msg, 15)
			elif action == 'restart':
				thirdAction = raw_input('REASON? > ')
				msg = {}
				msg['m'] = thirdAction
				self.sendMessage(msg, 16)
			elif action == 'messageAll':
				thirdAction = raw_input('MESSAGE? > ')
				msg = {}
				msg['m'] = thirdAction
				self.sendMessage(msg, 17)
			elif action == 'messageClient':
				secondAction = raw_input('ID? > ')
				thirdAction = raw_input('MESSAGE? > ')
				msg = {}
				msg['m'] = thirdAction
				msg['id'] = secondAction
				self.sendMessage(msg, 18)
			elif action == 'messageServer':
				print("WARNING!! IS DANGEROUS")
				secondAction = raw_input('type > ')
				thirdAction = raw_input('obj_message > ')
				fourthAction = raw_input('waitForServer true or false? > ')
				waitForServer = True if fourthAction == "true" else False
				try:
					self.clientsocket.send('{ "t" : '+str(secondAction)+', "c" : '+thirdAction+' }\x00')
				except:
					self.log.msg("CONNECTION CLOSED!", "INFO")
			else:
				waitForServer = False
				print("handshake = handshake\nadmin = admin rights\nget = get something\nset = set something\nstop = stop the server\nkick = kick someone\nban = ban someone\nkickall = kick everybody\nrestart = restart\nmessageall = message everybody\nmessageclient = message client\n")
			
			if waitForServer:
				data = self.clientsocket.recv(4096)
				self.log.msg("RECIEVED: "+data, "DATA")
				
				try:
					data = data.replace('\x00', '').encode("utf-8")
					obj_msg = ast.literal_eval(data)
				except:
					obj_msg = ast.literal_eval(json.loads(data.replace('\x00', '')))
					
				if obj_msg['t'] == 1:
					if obj_msg['c']['s'] == 1:
						self.log.msg("ADMIN RIGHTS GRANDED", "INFO")
					else:
						self.log.msg("ADMIN RIGHTS NOT GRANDED", "INFO")
				elif obj_msg['t'] == 10:
					if obj_msg['c']['s'] == 1:
						if obj_msg['c']['t'] == 0:
							self.log.msg("GET USERS SUCCESS", "INFO")
							for u in obj_msg['c']['u']:
								print "ID:" + str(u['id'])
								print "ADRESS:" + str(u['a'])+"\n"
						elif obj_msg['c']['t'] == 1:
							self.log.msg("GET ADMINS SUCCESS", "INFO")
							for u in obj_msg['c']['u']:
								print "ID:" + str(u['id'])
								print "ADRESS:" + str(u['a'])+"\n"
						elif obj_msg['c']['t'] == 2:
							self.log.msg("GET HISTORY SUCCESS", "INFO")
							print "ID:" + str(obj_msg['c']['u']['id'])
							for h in obj_msg['c']['u']['h']:
								print "TYPE:" + str(h['t'])
								print "SENDER:" + str(h['s'])
								print "RECIEVER:" + str(h['r'])+"\n"
						elif obj_msg['c']['t'] == 3:
							self.log.msg("GET USER SUCCESS", "INFO")
							print "ID:" + str(obj_msg['c']['u']['id'])
							print "ADRESS:" + str(obj_msg['c']['u']['a'])	
					else:
						self.log.msg("GET NOT SUCCESSFULL", "INFO")
				elif obj_msg['t'] == 11:
					if obj_msg['c']['t'] == 0:
						if obj_msg['c']['s'] == 1:
							self.log.msg("SET ADMIN SUCCESS", "INFO")
						else:
							self.log.msg("SET ADMIN NOT SUCCESS", "INFO")
					if obj_msg['c']['t'] == 1:
						if obj_msg['c']['s'] == 1:
							self.log.msg("SET ACCEPT SUCCESS", "INFO")
						else:
							self.log.msg("SET ACCEPT NOT SUCCESS", "INFO")
				elif obj_msg['t'] == 12:
					if obj_msg['c']['s'] == 1:
							self.log.msg("STOP SUCCESS", "INFO")
				elif obj_msg['t'] == 13:
					if obj_msg['c']['s'] == 1:
							self.log.msg("KICK SUCCESS", "INFO")
				elif obj_msg['t'] == 14:
					if obj_msg['c']['s'] == 1:
							self.log.msg("BAN SUCCESS", "INFO")
				elif obj_msg['t'] == 15:
					if obj_msg['c']['s'] == 1:
							self.log.msg("KICKALL SUCCESS", "INFO")
							for u in obj_msg['c']['u']:
								print "KICKED ID:" + str(u['id'])
				elif obj_msg['t'] == 16:
					if obj_msg['c']['s'] == 1:
							self.log.msg("RESTART SUCCES", "INFO")
				elif obj_msg['t'] == 17:
					if obj_msg['c']['s'] == 1:
							self.log.msg("MESSAGE ALL SUCCESS", "INFO")
							for u in obj_msg['c']['u']:
								print "MESSAGE TO ID:" + str(u['id'])
				elif obj_msg['t'] == 18:
					if obj_msg['c']['s'] == 1:
							self.log.msg("MESSAGE SUCCESS", "INFO")

				elif obj_msg['t'] == 30:
					self.log.msg("ADMIN RIGHTS NEEDED", "INFO")
				elif obj_msg['t'] == 31:
					self.log.msg("ERROR", "INFO")
			
		self.clientsocket.close()
	
	def sendMessage(self, msg_obj, type):
		self.log.msg("SEND TYPE:"+str(type), "INFO")
		msg = json.dumps(msg_obj)
		self.log.msg("SEND DATA:"+msg, "DATA")
		try:
			self.clientsocket.send('{ "t" : '+str(type)+', "c" : '+msg+' }\x00')
		except:
			self.log.msg("CONNECTION CLOSED!", "INFO")
		
if __name__=='__main__':
	ini = iniParser.init("settings.ini")
	host = 'localhost'
	port = int(ini.getSetting("Server","port"))
	hsid = ini.getSetting("Server","handshakeid")
	aid = ini.getSetting("Server", "adminid")
	
	admin = MyAdmin((host, port), hsid, aid)

