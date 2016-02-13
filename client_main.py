#!/usr/bin/python

# This file will contain the implementation of the top-level client-side code

import sys
import os
INSTALL_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
sys.path.append('{0}/socket'.format(INSTALL_DIR))
sys.path.append('{0}/common'.format(INSTALL_DIR))

# pi_bot libraries
import client
import commands
import message
import argparse

# Constants
DEFAULT_PORT = 12987
DEFAULT_SERVER_ADDR = '192.168.1.164'

# Globals
 messager = message.print_messager()

def drive(conn):
	pass

def interactive(conn):
	pass

def getArgs():
	parser = argparse.ArgumentParser(description='Control a remote pi_bot.')
	parser.add_argument('--interactive', action='store_true', help='Control robot interactively.')
	parser.add_argument('--drive', action='store_true', help='Drive the robot with the arrow keys.')
	parser.add_argument('--port', type=int, help='Specify a custom port.')
	parser.add_argument('--host', type=str, help='Specify a custom hostname where the pi_bot server is running.')

	return parser.parse_args()

def main():
	print "Client main!"
	port = DEFAULT_PORT
	host = DEFAULT_SERVER_ADDR
	args = getArgs()

	if args.port:
		port = args.port
	
	if args.host:
		host = args.host

	client_connn = client.bot_client(messager, port, host)
	client_conn.start()

	if args.drive:
		drive(client_conn)
	elif args.interactive:
		interactive(client_conn)

	client_conn.stop()

if __name__ = '__main__':
	main()
