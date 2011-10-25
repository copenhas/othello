
class NDNode:

	def __init__(self, id, value):
		self.id = id
		self.value = value
		self.adjacents = {}

	def __str__(self):
		return "< NDNode: %s - %s >" % str(self.id), str(self.value)

#TODO: seriously need to make this just inherit from dict or something
class Graph:

	def __init__(self):
		self.nodes = {}

	def has_key(self, key):
		return self.nodes.has_key(key)

	def __getitem__(self, key):
		return self.nodes[key]
	
	def __setitem__(self, key, value):
		self.nodes[key] = value

	def __iter__(self):
		return self.nodes.itervalues()
