# This file will contain the sensor abstract class

import sys
import os
INSTALL_DIR = os.path.dirname(os.path.realpath(sys.argv[0])) + '/../'
sys.path.append('{0}/common'.format(INSTALL_DIR))

import threading
import time

# pi_bot libraries
import message

class sensor(threading.Thread):
	def __init__(self, name, sleep_period, messager):
		threading.Thread.__init__(self)
		self.name = name
		self.running = False
		self.sleep_period = sleep_period
		self.setDaemon(True) # When main terminates this thread will be automatically killed.
		self.stopped = threading.Event()
		self.value = None
		self.messager = messager

	def __del__(self):
		self.messager.debug("Destructing sensor: {0}".format(self.name))
		if self.running:
			self.stop()

	def __str__(self):
		return "Sensor\n\tname: {0}\n\trunning: {1}\n\tvalue: {2}".format(self.name, self.running, self.value)

	def start(self):
		try:
			super(sensor, self).start()
		except:
			self.messager.error("Unable to start sensor: {0}".format(self.name))

	def stop(self):
		self.messager.info("Stop requested of sensor: {0}".format(self.name))
		if not self.running:
			self.messager.warning("Sensor: {0} is not running, 'stop()' will have no effect".format(self.name))
		else:
			self.stopped.set()
			self.running = False
			
	def run(self):
		self.messager.info("Thread for sensor: {0} is now running".format(self.name))
		while not self.stopped.is_set():
			self.running = True
			self.acquire()
			time.sleep(self.sleep_period)
	
		self.running = False

	# To be overriden
	def acquire(self):
		self.messager.info("Sensor: {0} is acquiring a new value")

	# To be overriden
	def init(self):
		self.messager.info("Initializing sensor: {0}".format(self.name))
		
	def getValue(self):
		return self.value
	
	def isRunning(self):
		return self.running
