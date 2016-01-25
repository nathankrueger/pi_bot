#!/usr/bin/python

# This file will contain the top-level code to run on the Raspberry Pi powered robot

import sys
sys.path.append('./socket')
sys.path.append('./common')
sys.path.append('./robot_control')
sys.path.append('./sensor')

import time
import argparse

# pi_bot libraries
import motors
import server
import sensors
import commands
import message

DEFAULT_PORT=101112

def getArgs():
	# Grab command-line arguments
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--port', type=int, help='Set the port to run the server on.')
	parser.add_argument('--interactive', type=str, help='Control robot interactively.')

	return parser.parse_args()

def interactive():
	pass

def main():
	args = getArgs()
	server_port = DEFAULT_PORT

	if args.port:
		server_port = args.port

	if args.interactive:
		interactive()

	print "Pi-Robot main!"

if __name__ == '__main__':
	main()
