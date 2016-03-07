# This file will contain the simple UART driver for the Maxbotix LV-EZ1 Sonar sensor

import sys
import os
INSTALL_DIR = os.path.dirname(os.path.realpath(sys.argv[0])) + '/../'
sys.path.append('{0}/common'.format(INSTALL_DIR))

import serial

# pi_bot libraries
import message
import sensor

class sonar_sensor(sensor.sensor):
	def __init__(self, uart_path, name, sleep_period, messager):
		sensor.sensor.__init__(self, name, sleep_period, messager)
		self.serial_comm = serial.Serial()
		self.serial_comm.baudrate = 9600
		self.serial_comm.port = uart_path

	def init(self):
		sensor.sensor.init()
		if not self.serial_comm.is_open:
			self.serial_comm.open()

	def acquire(self):
		sensor.sensor.acquire()
		if self.serial_comm.is_open:
			self.serial.flush()
			serial_val = self.serial.read(10)
			if len(serial_val) == 4:
				self.value = int(serial_val[1:])

	def release(self):
		sensor.sensor.release()
		if self.serial_comm.is_open:
			self.serial_comm.close()

