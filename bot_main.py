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

DEFAULT_PORT=12987
messager = message.print_messager()
motor_man = motors.motor_manager(messager)

def interactive_local(stdscr):
	UP_KEY = 259
	DOWN_KEY = 258
	LEFT_KEY = 260
	RIGHT_KEY = 261
	SPEED = 50
	try:
		while True:
			c = stdscr.getch()
			if c == UP_KEY:
				motor_man.get_motors().forward(SPEED)
			elif c == DOWN_KEY:
				motor_man.get_motors().backward(SPEED)
			elif c == LEFT_KEY:
				motor_man.get_motors().ccw(SPEED)
			elif c == RIGHT_KEY:
				motor_man.get_motors().cw(SPEED)
			else:
				motor_man.motors_off()

	except KeyboardInterrupt:
		pass

def listen(conn):
	pass

def getArgs():
	# Grab command-line arguments
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--port', type=int, help='Set the port to run the server on.')
	parser.add_argument('--interactive', action='store_true', help='Control robot interactively.')
	parser.add_argument('--listen', action='store_true', help='Listen for commands from the client.')

	return parser.parse_args()

def main(stdscr):
	args = getArgs()
	server_port = DEFAULT_PORT

	print "Pi-Robot main!"

	if args.port:
		server_port = args.port

	server_conn = server.bot_server(messager, server_port)
	server_conn.start()

	if args.interactive:
		interactive_local(stdscr)

	elif args.listen:
		listen(server_conn)
	
	server_conn.stop()

if __name__ == '__main__':
	curses.wrapper(main)
