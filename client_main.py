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

def main():
	print "Client main!"

if __name__ = '__main__':
	main()
