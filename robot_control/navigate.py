import sys
sys.path.append('../common')
sys.path.append('../sensor')

import time
import random

# pi_bot libraries
import message
import motors
import sensor

class basic_navigation:
	def __init__(self, motor_manager, sensor_manager):
		self.motor_manager = motor_manager
		self.sensor_manager = sensor_manager
		self.reset()

	def reset(self):
		self.motor_manager.cancel_outstanding()
		self.motor_manager.motors_off()

	def turn_random_direction(self, speed, time_ms):
		num = random.random()
		if random <= 0.5:
			self.motor_manager.cw(speed, time_ms)
		else:
			self.motor_manager.ccw(speed, time_ms)

	# Call this in a main loop, presumably in bot_main.py
	def basic_navigate(self):
		DEF_SPEED = 50
		DEF_RANGE = 12
		while self.sensors.no_obstacle_within(DEF_RANGE):
			if not self.motor_manager.is_running():
				self.motor_manager.forward(DEF_SPEED, 1000)
			else
				pass # Go check the sensors again to make sure we don't crash!!!
		
		self.motor_manager.motors_off()
		# Turn a random direction, then check the sensors again!
		self.turn_random_direction(DEF_SPEED, 500)

