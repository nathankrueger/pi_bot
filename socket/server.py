# This file will contain the implementation of the pi_bot server which will listen to remote commands
import sys
import os
INSTALL_DIR = os.path.dirname(os.path.realpath(sys.argv[0])) + '/../'
sys.path.append('{0}/common'.format(INSTALL_DIR))

import time
import socket
import threading
import Queue

# pi_bot libraries
import message

class bot_server(threading.Thread):
	def __init__(self, messager, port, max_recv_bytes=1024, rest_period=0.01):
		super(bot_server, self).__init__()
		self.port = port
		self.MAX_RECV_BYTES = max_recv_bytes
		self.REST_PERIOD = rest_period
		self.messager = messager
		self.hostname = ''
		self.server_socket = None
		self.client_socket = None
		self.recv_q = Queue.Queue()
		self.stopped = threading.Event()
		
	# Accept incoming socket connections
	def __accept_connection(self):
		try:
			self.server_socket.listen(1)
			conn, addr = self.server_socket.accept()
			self.messager.info("Accepted client socket connection: {0}".format(addr))
			self.client_socket = conn
			self.client_socket.setttimeout(1)
		except socket.error, err_msg:
			self.messager.error("Failed to accept connection: {0}".format(err_msg))
			self.client_socket = None
	
	# Bind the server socket to the specified port
	def __bind_server_socket(self):
		self.server_sock = None
		try:
			self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.server_socket.setblocking(0)
			self.server_socket.bind((self.hostname, self.port))
			self.messager.info("Successfully bound server socket to port: {0}".format(self.port))
		except Exception as err:
			self.messager.error("Failed to bind server socket to port: {0}".format(self.port))
			self.server_socket = None

	# Read data from the client socket
	def __read_client_socket(self):
		read_data = None
		err_msg = None
		if not self.client_socket is None:
			try:
				read_data = self.client_socket.recv(self.MAX_RECV_BYTES)
			except socket.timeout, e:
				read_data = None
				err = e.args[0]
				if not (err == 'timed out'):
					err_msg = err
			except socket.error as err:
				err_msg = err
			
		if not err_msg is None:
			self.messager.error("Error reading from client socket: {0}".format(err_msg))
			#self.client_socket = None
			
		return read_data

	def __reset(self):
		self.messager.info("Reseting server...")
		self.disconnect_client()
		self.disconnect_server()
		self.server_socket = None
		self.client_socket = None
		with self.recv_q.mutex:
			self.recv_q.queue.clear()
		self.stopped.clear()

	def has_connection(self):
		return self.client_socket is not None

	# Get the most recently recieved data from the client socket
	def get_data(self):
		if not self.recv_q.empty():
			return self.recv_q.get()
		else:
			return None

	# Send data to the client socket if possible
	def send_data(self, data):
		if self.has_connection():
			try:
				self.client_socket.send(data)
			except socket.error, err_msg:
				self.messager.error("Failed to send data to client socket: {0}".format(err_msg))

	def disconnect_client(self):
		if self.has_connection():
			try:
				self.client_socket.close()
				self.client_socket = None
				self.messager.info("Closing connection to client socket")
			except socket.error, err_msg:
				self.client_socket = None
				self.messager.error("Failed to close client socket")

	def disconnect_server(self):
		if not self.server_socket is None:
			try:
				self.server_socket.close()
				self.server_socket = None
				self.messager.info("Closing connection to server socket")
			except socket.error, err_msg:
				self.server_socket = None
				self.messager.error("Failed to close server socket")	

	# Stop the internal thread
	def stop(self):
		self.stopped.set()

	def run(self):
		# Reset state and setup server socket
		self.__reset()
		self.__bind_server_socket()

		# Process incoming commands
		while not self.stopped.is_set():
			time.sleep(self.REST_PERIOD)
			
			# Get a connection if we don't have one
			if not self.has_connection():
				self.__accept_connection()
			
			read_data = self.__read_client_socket()
			if not read_data is None:	
				self.recv_q.put(read_data)
		
		# Make sure everything is disconnected when the thread exits
		self.__reset()
