#!/usr/bin/python

# This file will contain the top-level code to run on the Raspberry Pi powered robot

import sys
sys.path.append('./socket')
sys.path.append('./common')
sys.path.append('./robot_control')
sys.path.append('./sensor')
import time

# pi_bot libraries
import motors
import server
import sensors
import commands
import message

def main():
	print "Pi-Robot main!"

if __name__ == '__main__':
	main()
