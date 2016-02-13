# This file will contain the implementation of the client-side socket code

import sys
import os
INSTALL_DIR = os.path.dirname(os.path.realpath(sys.argv[0])) + '/../'
sys.path.append('{0}/common'.format(INSTALL_DIR))

import time
import Queue
import threading
import sockets

# pi_bot libraries
import message

class bot_client(threading.Thread):
	def __init__(self, messager, port, server_addr, max_recv_bytes=1024, rest_period=0.01):
		self.port = port
		self.MAX_RECV_BYTES = max_recv_bytes
		self.REST_PERIOD = rest_period
		self.messager = messager
		self.server_addr = server_addr
		self.client_socket = None
		self.send_q = Queue.Queue()
		self.stopped = threading.Event()

	# Connect the client socket to the specified port on the server
	def __connect_client_socket(self):
		self.client_socket = None
		try:
			self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.server_socket.connect((self.server_addr, self.port))
			self.messager.info("Successfully connected to server {0}:{1}".format(self.server_addr, self.port))
		except Exception as err:
			self.messager.error("Failed to connect to server {0}:{1}".format(self.server_addr, self.port))
			self.client_socket = None

	def __send_data_item(self):
		if not self.send_q.empty():
			send_data = self.send_q.get()
			try:
				self.client_socket.sendall(send_data)
			except socket.error as err_msg:
				self.messager.error("Failed to send data to server: {0}".format(err_msg))

	def __reset(self):
		self.disconnect_client()
		self.client_socket = None
		self.send_q.clear()
		self.stopped.clear()

	def has_connection(self):
		return self.client_socket is not None

	# Get the most recently recieved data from the client socket
	def get_data(self):
		read_data = None
		err_msg = None
		if self.has_connection():
			try:
				read_data = self.client_socket.recv(self.MAX_RECV_BYTES)
			except socket.timeout, e:
				read_data = None
				err = e.args[0]
				if not (err == 'timed out'):
					err_msg = err
			except: socket.error as err:
				err_msg = err
			
		if not err_msg is None:
			self.messager.error("Error reading from client socket: {0}".format(err_msg))
			#self.client_socket = None
		
		return read_data
	
	# Put data on the send q to be sent out a asynchronously by the internal thread
	def send_data(self, data):
		self.send_q.put(data)
		
	def disconnect_client(self):
		if self.has_connection():
			try:
				self.client_socket.close()
				self.client_socket = None
				self.messager.info("Closing connection to client socket")
			except socket.error as err_msg:
				self.client_socket = None
				self.messager.error("Failed to close client socket")	

	# Stop the internal thread
	def stop(self):
		self.stopped.set()

	def run(self):
		# Reset state and setup server socket
		self.__reset()

		# Process incoming commands
		while not self.stopped.is_set():
			time.sleep(self.REST_PERIOD)
			
			# Get a connection if we don't have one
			if not self.has_connection():
				self.__connect_client_socket()
			
			if self.has_connection():
				while not self.send_q.empty():
					self.__send_data_item()
		
		# Make sure everything is disconnected when the thread exits
		self.__reset()
