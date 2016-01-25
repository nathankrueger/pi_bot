# This file will contain the implementation of the motor control logic
import sys
sys.path.append('../common')

import Adafruit_MotorHAT as af_mh
from Adafruit_MotorHAT import Adafruit_MotorHAT as hat
from Adafruit_MotorHAT import Adafruit_DCMotor as dc_motor
import atexit

# pi_bot libraries
import message

MAX_SPEED=255
I2C_ADDRESS=0x60
LEFT_MOTOR_NUM=2
RIGHT_MOTOR_NUM=1

class motors:
	def __init__(self):
		self.mh = hat(addr=I2C_ADDRESS)
		atexit.register(self.turn_off_motors)
		pass

	def get_right_motor(self):
		return self.mh.getmotor(RIGHT_MOTOR_NUM)

	def get_left_motor(self):
		return self.mh.getmotor(LEFT_MOTOR_NUM)

	def turn_off_motors(self):
		self.get_left_motor().run(af_mh.RELEASE)
		self.get_right_motor().run(af_mh.RELEASE)

	def full_forward(self):
		self.run_left_motor(100)
		self.run_right_motor(100)
	
	def full_backward(self):
		self.run_left_motor(-100)
		self.run_right_motor(-100)

	def full_cw(self):
		self.run_left_motor(100)
		self.run_right_motor(-100)

	def full_ccw(self):
		self.run_left_motor(-100)
		self.run_right_motor(100)
		
	def run_left_motor(self, percentage):
		# Scale 100 to 255
		run_speed = int(abs(percentage)*(MAX_SPEED/100.0))
		lm = self.get_left_motor()
		lm.setSpeed(run_speed)

		if percentage > 0:
			lm.run(af_mh.FORWARD)
		else:
			lm.run(af_mh.BACKWARD)

	def run_right_motor(self, percentage):
		# Scale 100 to 255
		run_speed = int(abs(percentage)*(MAX_SPEED/100.0))
		rm = self.get_right_motor()
		rm.setSpeed(run_speed)

		if percentage > 0:
			rm.run(af_mh.FORWARD)
		else:
			rm.run(af_mh.BACKWARD)

