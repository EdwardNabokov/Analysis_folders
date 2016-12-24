from ConnectionHandler import *
from CommandHandler import *
import curio
from curio import Queue
import pickle


class Client:
	"""
	Temp high level client
	get some operations create tasks and send them
	"""

	@classmethod
	async def start(cls, name, addr, tasks, client=None):
		self = Client()
		self.tasks = tasks

		self.send = Queue()
		self.recieve = Queue()

		self.connection = await curio.spawn(ConnectionHandler.runHandler(name, addr, 
			self.send, self.recieve, client))
		await self.do_something()

		return self

	def file_send(self, filename):
		d = {
			'command': 'write',
			# TEST STRING
			'name': 'sync/' + filename,
			'block': '',
			'package_number': 0
			}
		with open(filename, 'rb') as file:
			while True:
				d['block'] = file.read(15000)
				if d['block'] == b'':
					break
				d['package_number'] += 1
				yield pickle.dumps(d)


	def create_file(self, filename):
		d = {
			'command': 'create',
			# TEST STRING
			'name':  'sync/' + filename,
			'block': '',
			'package_number': 0
			}
		return pickle.dumps(d)


	async def do_something(self):
		for file in self.tasks:
			await self.send.put(self.create_file(file))
			for x in self.file_send(file):
				await self.send.put(x)




addr = ('127.0.0.1', 25012)
data = ['import/file.txt', 'import/file2.txt', 'import/clion.dmg']
curio.run(Client.start('127.0.0.1:25012', addr, data))
