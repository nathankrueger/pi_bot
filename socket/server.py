# This file will contain the implementation of the pi_bot server which will listen to remote commands
import sys
import os
INSTALL_DIR = os.path.dirname(os.path.realpath(sys.argv[0])) + '/../'
sys.path.append('{0}/common'.format(INSTALL_DIR))

import socket
import threading

# pi_bot libraries
import message
