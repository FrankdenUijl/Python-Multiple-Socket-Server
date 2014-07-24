#!/bin/sh
from Client import Client
from ServerSocket import ServerSocket
from iniParser import init
from logClass import logClass
import socket

class MyServer(object):
	def __init__(self, adress):
		self.log = logClass("MY_SERVER")
		self.adress = adress
		self.client_socket = []
		self.server_socket = ServerSocket(self.adress)
		self._isAlive = False
		self.idClient = 0
				
	def _start(self):
		self.log.msg("START SERVER: "+str(self.adress[0])+":"+str(self.adress[1]), "INFO")
		self._isAlive = True
		self._run()
	
	def _run(self):
		while self._isAlive:
			clientsock, address = self.server_socket.getConnection()
			try:
				self.client_socket.append(Client(clientsock, address, self))
				self.idClient += 1
			except:
				self.log.msg("SERVER STOPPED", "INFO")

		self.log.msg("STOP SERVER: "+str(self.adress[0])+":"+str(self.adress[1]), "INFO")
		
	def _stop(self):
		self.server_socket.close()
		del self.server_socket
		del self.client_socket
		self._isAlive = False
		
		self.forceStop = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.forceStop.connect(self.adress)
	
	def _removeSocket(self, s):
		self.log.msg("REMOVE SOCKET ID:"+str(s.id)+" ADRESS: "+str(s.adress[0])+":"+str(s.adress[1]), "INFO")
		self.client_socket.remove(s)
	
	def _restart(self):
		self.server_socket = ServerSocket(self.adress)
		self.client_socket = []
		self._start()
	
	def sendToBroadcast(self, broadcast, msg, type, sender):
		self.log.msg("MESSAGE type: "+str(type)+" from "+str(sender)+" VIA BROADCAST:"+broadcast, "INFO")
		self.log.msg("MESSAGE BROADCAST DATA: "+msg, "DATA")
		for s in self.client_socket:
			if broadcast in s.broadcasts:
				if sender != s.id:
					self.log.msg("SEND MESSAGE BROADCAST TO "+str(s.id), "DATA")
					s.sendMessage(msg, type, sender)
	
if __name__ == "__main__":
	ini = init("settings.ini")
	host = ini.getSetting("Server","host")
	port = int(ini.getSetting("Server","port"))
	s = MyServer((host, port))
	s._start()
	