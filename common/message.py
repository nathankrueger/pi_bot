# This file contains a messager 'interface' which can be used to create multiple implementations of debug, info, warning, and error messages

import datetime

class messager:
	def __init__(self):
		self.__raise()

	def warning(self, msg):
		self.__raise()
		
	def info(self, msg):
		self.__raise()
	
	def debug(self, msg):
		self.__raise()
	
	def error(self, msg):
		self.__raise()

	def __raise(self):
		raise Exception("Unimplemented abstract method")

class print_messager(messager):
	def __init__(self):
		pass

	def __print_message(self, msg, header):
		dt = datetime.datetime.today()
		print "{0}/{1}/{2} {3}:{4}:{5} {6}: {7}".format(dt.month, dt.day, dt.year, dt.hour, dt.minute, dt.second, header, msg)

	def warning(self, msg):
		self.__print_message(msg, "Warning")

	def info(self, msg):
		self.__print_message(msg, "Info")
	
	def debug(self, msg):
		self.__print_message(msg, "Debug")
	
	def error(self, msg):
		self.__print_message(msg, "Error")
