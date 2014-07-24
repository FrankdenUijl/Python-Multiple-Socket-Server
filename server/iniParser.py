import ConfigParser
import logClass

class init:
	def __init__(self, path):
		self.log = logClass.logClass(path)

		self.config = ConfigParser.ConfigParser()
		try:
			self.config.read(path)
		except:
			self.log.msg("COULD NOT READ: "+path, "ERROR")

	def ConfigSectionMap(self, section):
		dict1 = {}
		Config = ConfigParser.ConfigParser()
		
		Config.read("settings.ini")
		options = Config.options(section)
		for option in options:
			try:
				dict1[option] = Config.get(section, option)
				if dict1[option] == -1:
					self.log.msg("skip: %s" % option, "ERROR")
			except:
				self.log.msg("exception on %s!" % option, "ERROR")
				dict1[option] = None
		return dict1
	
	def getSetting(self, option, index):
		return self.ConfigSectionMap(option)[index]