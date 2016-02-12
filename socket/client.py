# This file will contain the implementation of the client-side socket code

import sys
import os
INSTALL_DIR = os.path.dirname(os.path.realpath(sys.argv[0])) + '/../'
sys.path.append('{0}/common'.format(INSTALL_DIR))

import sockets

# pi_bot libraries
import message
