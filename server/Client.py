from ClientSocket import ClientSocket
import json

class Client(ClientSocket):
	def __init__(self, socket, adress, server):
		super(Client, self).__init__(socket, adress, server)
		self.isLogin = False
		self.type_user = None
		self.id_user = None
	
	def client_functions(self, msg_obj):
		if msg_obj['t'] == 0: #login
			msg_obj['c'] #game or chatroom logic here