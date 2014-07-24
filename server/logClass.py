import datetime
import logging

class logClass:
	def __init__(self, base):
		self.ignore = {}
		self.ignoreAll = False
		self.onlyType = ""
		self.base = base
		logging.basicConfig(filename='server.log',level=logging.DEBUG)
		logging.debug(self.base+" CREATED")
	
	def msg(self, msg, type):
		i = datetime.datetime.now()
		if self.onlyType == "":
			if self.ignoreAll == False:
				if not type in self.ignore:
					print(str(i)+"\n "+self.base+">\n  "+type+">\n   "+msg+"\n")
					logging.info(str(i)+"\n "+self.base+">\n  "+type+">\n   "+msg+"\n")
				else:
					logging.debug(str(i)+"\n "+self.base+">\n  "+type+">\n   "+msg+"\n")
		
		elif self.onlyType == type: 
			print(str(i)+"\n "+self.base+">\n  "+type+">\n   "+msg+"\n")
			logging.info(str(i)+"\n "+self.base+">\n  "+type+">\n   "+msg+"\n")
		else:
			logging.debug(str(i)+"\n "+self.base+">\n  "+type+">\n   "+msg+"\n")
	
	def iqnoreType(self, type):
		self.ignore[type] = True
	
	def ignoreAll(self, bool):
		self.ignoreAll = bool
		
	def ignoreAllExcept(self, type):
		self.ignoreAll = false
		self.onlyType = type