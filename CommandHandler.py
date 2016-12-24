import pickle
import os
import curio
  
class CommandHandler:

	def __init__(self, data):
		self.data = pickle.loads(data)

	def perform_operation(self):
		if self.data['command'] == 'create':
			self.create_file()
		if self.data['command'] == 'write':
			self.write_to_file()

	def write_to_file(self):
		with open(self.data['name'], 'ab') as file:
			file.write(self.data['block'])

	def create_file(self):
		with open(self.data['name'], 'wb') as file:
			pass