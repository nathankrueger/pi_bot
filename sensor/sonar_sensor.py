# This file will contain the simple UART driver for the Maxbotix LV-EZ1 Sonar sensor

import sys
import os
INSTALL_DIR = os.path.dirname(os.path.realpath(sys.argv[0])) + '/../'
sys.path.append('{0}/common'.format(INSTALL_DIR))

import serial
import re

# pi_bot libraries
import message
import sensor

class sonar_sensor(sensor.sensor):
	def __init__(self, uart_path, name, sleep_period, messager):
		sensor.sensor.__init__(self, name, sleep_period, messager)
		self.serial_comm = serial.Serial()
		self.serial_comm.baudrate = 9600
		self.serial_comm.port = uart_path

	def initialize(self):
		sensor.sensor.initialize(self)
		if not self.serial_comm.isOpen():
			self.messager.info("Opening serial port for sonar_sensor with UART path: {0} @ baudrate: {1}".format(self.serial_comm.port, self.serial_comm.baudrate))
			self.serial_comm.open()
		else:
			self.messager.error("Failed to initialize sonar_sensor, serial port is already open.")

	def acquire(self):
		sensor.sensor.acquire(self)
		if self.serial_comm.isOpen():
			self.serial_comm.flush()
			serial_val = str(self.serial_comm.read(10)).strip()
			match = re.search(r'R(\d{3})', serial_val)

			if match:
				self.value = int(match.group(1))
			else:
				self.messager.error("sonar_sensor: {0} recieved garbage: {1}".format(self.name, serial_val))
		else:
			self.messager.error("Failed to acquire from sonar_sensor, serial port is not open.")

	def release(self):
		sensor.sensor.release(self)
		if self.serial_comm.isOpen():
			self.serial_comm.close()

