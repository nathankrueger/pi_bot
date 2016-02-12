#!/usr/bin/python

# This file will contain the top-level code to run on the Raspberry Pi powered robot

import sys
import os
INSTALL_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
sys.path.append('{0}/socket'.format(INSTALL_DIR))
sys.path.append('{0}/common'.format(INSTALL_DIR))
sys.path.append('{0}/robot_control'.format(INSTALL_DIR))
sys.path.append('{0}/sensor'.format(INSTALL_DIR))

import time
import argparse
import curses

# pi_bot libraries
import motors
import server
import sensor
import commands
import message

DEFAULT_PORT=101112
messager = message.print_messager()
motor_man = motors.motor_manager(messager)

def getArgs():
	# Grab command-line arguments
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--port', type=int, help='Set the port to run the server on.')
	parser.add_argument('--interactive', action='store_true', help='Control robot interactively.')

	return parser.parse_args()

def interactive(stdscr):
	UP_KEY = 259
	DOWN_KEY = 258
	LEFT_KEY = 260
	RIGHT_KEY = 261
	try:
		while True:
			c = stdscr.getch()
			if c == UP_KEY:
				motor_man.get_motors().full_forward()
			elif c == DOWN_KEY:
				motor_man.get_motors().full_backward()
			elif c == LEFT_KEY:
				motor_man.get_motors().full_ccw()
			elif c == RIGHT_KEY:
				motor_man.get_motors().full_cw()
			else:
				motor_man.motors_off()

	except KeyboardInterrupt:
		pass

def main(stdscr):
	args = getArgs()
	server_port = DEFAULT_PORT

	print "Pi-Robot main!"

	if args.port:
		server_port = args.port

	if args.interactive:
		interactive(stdscr)

if __name__ == '__main__':
	curses.wrapper(main)
