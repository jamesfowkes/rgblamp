import shelve

import logging

def get_logger():
	return logging.getLogger(__name__)

class PersistentConfig:

	def __init__(self, filename):
		self.__dict__["filename"] = filename

	def get(self, key):
		with shelve.open(self.filename) as shelf:
			try:
				v = shelf[key]
				get_logger().info("Getting {}={}:".format(key, v))
				return v
			except:
				return None
				
	def __getitem__(self, key):
		return self.get(key)
	
	def __getattr__(self, attr):

		if attr == "filename":
			return self.__dict__["filename"]

		try:
			return self.get(attr)
		except KeyError:
			raise AttributeError
	
	def __setattr__(self, name, value):
		if name == "filename":
			self.__dict__["filename"] = value
			return

		with shelve.open(self.filename) as shelf:
			get_logger().info("Setting {}={}".format(name, value))
			shelf[name] = value

	def set(self, **kwargs):
		with shelve.open(self.filename) as shelf:
			get_logger().info("Setting {} values:".format(len(kwargs)))
			for k, v in kwargs.items():
				self.__setattr__(k, v)

	def set_defaults(self, **kwargs):
		for k, v in kwargs.items():
			if self.get(k) is None:
				self.__setattr__(k, v)
