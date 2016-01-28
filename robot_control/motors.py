# This file will contain the implementation of the motor control logic
import sys
sys.path.append('../common')

import threading
import time

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

# Main class for moving the motors
class motors:
	def __init__(self, mhat_addr):
		self.mh = hat(addr=mhat_addr)
		atexit.register(self.cleanup_motors)

	def get_right_motor(self):
		return self.mh.getmotor(RIGHT_MOTOR_NUM)

	def get_left_motor(self):
		return self.mh.getmotor(LEFT_MOTOR_NUM)

	# Ensure the motors stop running at program exit
	def cleanup_motors(self):
		self.get_left_motor().run(af_mh.RELEASE)
		self.get_right_motor().run(af_mh.RELEASE)

	# Set the motor speed to 0
	def motors_off(self):
		self.run_left_motor(0)
		self.run_right_motor(0)

	def full_forward(self):
		self.run_left_motor(100)
		self.run_right_motor(100)
	
	def full_backward(self):
		self.run_left_motor(-100)
		self.run_right_motor(-100)

	def forward(self, percentage):
		self.run_left_motor(percentage)
		self.run_right_motor(percentage)

	def reverse(self, percentage):
		self.run_left_motor(percentage*-1)
		self.run_right_motor(percentage*-1)

	def full_cw(self):
		self.run_left_motor(100)
		self.run_right_motor(-100)

	def full_ccw(self):
		self.run_left_motor(-100)
		self.run_right_motor(100)
	
	def cw(self, percentage):
		self.run_left_motor(percentage*-1)
		self.run_right_motor(percentage)

	def ccw(self, percentage):
		self.run_left_motor(percentage)
		self.run_right_motor(percentage*-1)

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

# Since motor movement is initiated by one-time I2C calls to the motor hat, there is no need to add the call to
# initiate the PWM to a seperate thread.  There is a need to request motor movement for a given period of time,
# followed by returning to idle, while conducting other tasks.  This thread handles waiting for a specified period
# of time, then shutting the motors back off.
class motor_off_timer(threading.Thread):
	def __init__(self, wait_time, callback, motors, messager):
		self.wait_time = wait_time
		self.callback = callback
		self.motors = motors
		self.cancel_event = threading.Event()
		self.running = False

	def start(self):
		try:
			super(motor_off_timer, self).start()
		except:
			self.messager.error("Unable to start motor_off_timer thread.")

	# Prevent the eventual motors_off call when changing modes.
	def cancel(self):
		self.cancel_event.set() # I'm worried about the order of this line and the next...
		self.running = False
	
	def is_running(self):
		return self.running

	def run(self):
		self.running = True
		time.sleep(self.wait_time)
		if not self.cancel_event.is_set():
			self.motors.motors_off()
			if self.callback:
				self.callback()

		self.running = False

# The top-level class that will likely be used by the pi_bot's main()
class motor_manager:
	def __init__(self, motors, messager, callback=None):
		self.motors = motors(I2C_ADDRESS)
		self.messager = messager
		self.last_motor_thread = None
		self.callback = callback

	def is_running(self):
		result = False
		if self.last_motor_thread:
			result = self.last.motor_thread.is_running()

		return result

	def set_callback(callback):
		self.callback = callback

	def cancel_outstanding(self):
		if self.is_running():
			self.last_motor_thread.cancel()

	def __start_timer(time_ms):
		time_s = float(time_ms)/1000.0
		self.last_motor_thread = motor_off_timer(time_s, self.callback, self.motors, self.messager)
		self.last_motor_thread.start()

	def motors_off(self):
		self.motors.motors_off()

	def cleanup_motors(self):
		self.motors.cleanup_motors()

	def full_forward(self, time_ms):
		self.cancel_outstanding()
		self.motors.full_forward()
		self.__start_timer(time_ms)

	def full_backward(self, time_ms):
		self.cancel_outstanding()
		self.motors.full_backward()
		self.__start_timer(time_ms)

	def forward(self, percentage, time_ms):
		self.cancel_outstanding()
		self.motors.forward(percentage)
		self.__start_timer(time_ms)

	def reverse(self, percentage, time_ms):
		self.cancel_outstanding()
		self.motors.reverse(percentage)
		self.__start_timer(time_ms)

	def full_cw(self, time_ms):
		self.cancel_outstanding()
		self.motors.full_cw()
		self.__start_timer(time_ms)

	def full_ccw(self, time_ms):
		self.cancel_outstanding()
		self.motors.full_ccw()
		self.__start_timer(time_ms)
	
	def cw(self, percentage, time_ms):
		self.cancel_outstanding()
		self.motors.cw(percentage)
		self.__start_timer(time_ms)

	def ccw(self, percentage, time_ms):
		self.cancel_outstanding()
		self.motors.ccw(percentage)
		self.__start_timer(time_ms)

	def run_left_motor(self, percentage, time_ms):
		self.cancel_outstanding()
		self.motors.run_left_motor(percentage)
		self.__start_timer(time_ms)

	def run_right_motor(self, percentage, time_ms):
		self.cancel_outstanding()
		self.motors.run_right_motor(percentage)
		self.__start_timer(time_ms)

