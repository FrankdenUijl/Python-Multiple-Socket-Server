from logClass import logClass
from socket import *

class ServerSocket(object):
	def __init__(self, adress):
		self.log = logClass("SERVER_SOCKET")
		
		self.adress = adress
		self.socket = socket(AF_INET, SOCK_STREAM)
		self._isAlive = True
		self._bind()
		
	def getConnection(self):
		self.log.msg("WAITING FOR CONNECTIONS", "INFO")
		return self.socket.accept()
		
	def _bind(self):
		self.socket.bind(self.adress)
		self.socket.listen(2)
		
	def close(self):
		self.socket.close()