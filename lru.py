#!/usr/bin/env python

class LRU_Entry():
	def __init__(self, key, value, parent_queue=None, previous_refrence=None, next_refrence=None,):
		self.key = key
		self.value = value
		self.parent_queue = parent_queue
		self.next_refrence = next_refrence
		self.previous_refrence = previous_refrence
		# could probably also calculate data size here as well so we could maintain a queue/entry data size
		# So we could implement queue memory limits instead of just max_entries
	def set(self, value):
		self.value = value
		# If we later implement memory sizes we would update the sizes here
		# and possibly the parents total size here or do that within the parent IDK which is better
	def get(self):
		return self.value


class LRU_Cache():
	'''
	Class that defines a Least Recently Used Cache
	Methods:
		- set(key, value) - set a key/value pair in the cache
		- get(key) - get a value for a key from the cache	

	Properties:
		- max_entries - Maximum number of entries allowed to exist within the queue
		- start_cursor - The next item to be bumped from the queue if max_entries is exceeded
		- end_cursor - the last item in the queue (used to add new entries after)
		- queue - Dict containing LRU queue entries
		- queue_entry_count - current count of items in the queue
	'''
	def __init__(self, max_entries=3):
		self.max_entries = max_entries
		self.start_cursor = None
		self.end_cursor = None
		self.queue = {}
		self.queue_entry_count = 0
	def get(self, key, detailed=False, update=True):
		'''
		Get a value for a given key from the cache
		'''
		entry = self.queue.get(key)
		if entry:
			if update:
				self.__update_entry_refrences__(entry)
			if detailed:
				return {'name': entry.key, 'value': entry.value, 'next_refrence': entry.next_refrence, 'previous_refrence': entry.previous_refrence}
			return entry.value
		else:
			return None
	def set(self, key, value):
		entry = self.queue.get(key)
		if entry == None:
			# Create new entry and add it to the queue
			entry = LRU_Entry(key, value, parent_queue=self, previous_refrence=self.end_cursor)
			#entry.previous_refrence.next_refrence = entry
			self.queue[key] = entry
			# increment queue_entry_count
			self.queue_entry_count += 1
		else:
			entry.set(value)
		self.__update_entry_refrences__(entry)
		# if max_entries is exceeded remove entry
		# NOTE: This should only happen on additions to the queue but we want it to happen after updating refrences
		if self.queue_entry_count > self.max_entries:
			self.__remove_lru__()
	def keys(self):
		keys = []
		cursor = self.start_cursor
		while cursor != None:
			key = cursor.key
			keys.append(key)
			cursor = cursor.next_refrence
		return keys
	def values(self):
		values = []
		cursor = self.start_cursor
		while cursor != None:
			value = cursor.value
			values.append(value)
			cursor = cursor.next_refrence
		return values
	def items(self):
		items = []
		cursor = self.start_cursor
		while cursor != None:
			item = (cursor.key, cursor.value)
			items.append(item)
			cursor = cursor.next_refrence
		return items
	def __remove_lru__(self):
		'''
		Removes the most lru entry from the queue and updates refrences
		'''
		self.start_cursor.next_refrence.previous_refrence = None
		del self.queue[self.start_cursor.key]
		self.queue_entry_count -= 1
		self.start_cursor = self.start_cursor.next_refrence
	def __update_entry_refrences__(self, entry):
		'''
		Updates surrounding entry refrences in the queue
		'''
		# short circut updates if we havn't been passed an actual entry object
		if entry == None:
			return
		# If we don't have a previous entry we are getting the first item in queue so we need to update start_cursor
		if entry.previous_refrence == None:
			self.start_cursor = entry.next_refrence
			# and the next refrence for the next refrence if a next refrence exists
			if entry.next_refrence:
				entry.next_refrence.previous_refrence = None
		# If we have a previous entry
		if entry.previous_refrence:
			# if we have a next entry (not new) set the previous entries next entry to our next entry
			if entry.next_refrence:
				entry.previous_refrence.next_refrence = entry.next_refrence
		# if we have a next entry
		if entry.next_refrence:
			# if we have a previous entry (not first entry in queue)
			if entry.previous_refrence:
				# set the next entries previous refrence to our previous refrence
				entry.next_refrence.previous_refrence = entry.previous_refrence
		# if we were not already the end cursor set the end cursors next refrence to us
		if entry != self.end_cursor and self.end_cursor != None:
			self.end_cursor.next_refrence = entry
		# set our previous refrence to the current end cursor
		entry.previous_refrence = self.end_cursor
		# Set the end cursor to be us
		self.end_cursor = entry
		# Nuke any next_refrence on the end_cursor as it should always be None
		self.end_cursor.next_refrence = None
		# If we don't have a start cursor we are a new first item and need to update the cursor
		if self.start_cursor == None:
			self.start_cursor = entry




# Create a new LRU_Cache

lru = LRU_Cache(max_entries=3)


# Add entry to cache

lru.set('a', '1')

# Test getting our entry

lru.get('a')

# From here on out going to use items() to test where things are at in the cache/queue

lru.items()
lru.set('b', '2')
lru.items()
lru.set('c', '3')
lru.items()
lru.set('d', '4')

# We should see 'a' fall off here as we just added a 4th item

lru.items()

# we should see b become the last entry in the list because we get it making it MRU

lru.get('b')
lru.items()

# we should see 'c' get updated and become MRU here

lru.get('c', detailed=True, update=False)
lru.set('c', 'winning')
lru.get('c', detailed=True, update=False)
lru.items()


