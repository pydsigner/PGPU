'''A set of dict()-like classes with differing features.
AUTHORS:
v0.4.5		--> pydsigner'''
from pgpu.compatibility import range

import pgpu.tkinter2x as tk
from pgpu.tkinter2x.constants import *
from pgpu.tkinter2x.simpledialog import askstring

class SortedDict(object):
	'''A sorted dictionary that is implemented as a merger of a dict() and a 
	list(). It exposes more of the dict() style via overloading but the list() 
	style is also accessible via named methods. When in doubt about which 
	"side" a method accesses, look at the signature; if one of the arguments is 
	@key, then it would access the dict() side. A method with @index as an 
	argument would access the list() side.
	
	AUTHORS:
	v0.4.5+		--> pydsigner
	'''
	def __init__(self, *args):
		'''
		SortedDict([(key_0, value_0), (key_1, value_1)..., (key_n, value_n)])
		SortedDict([key_0, key_1..., key_n], [value_0, value_1..., value_n])
		SortedDict([key_0, key_1..., key_n], default)
		SortedDict((key_0, value_0), (key_1, value_1)..., (key_n, value_n))
		'''
		self.data = []
		self.keydict = {}
		if len(args) == 1:
			for key, value in args[0]:
				self._add(key, value)
		elif len(args) == 2:
			if hasattr(args[1], '__len__') and len(args[1]) == len(args[0]):
				for i in range(len(args[0])):
					self._add(args[0][i], args[1][i])
			else:
				for key in args[0]:
					self._add(key, args[1])
		else:
			for key, value in args:
				self._add(key, value)
	
	def __delitem__(self, key):
		'Delete item @key from the dictionary.'
		del self.keydict[key]
	def __iter__(self):
		'Returns an iterator over the dictionary\'s keys.'
		return iter(self.keys())
	def __str__(self):
		prs = [str(pair) for pair in self.items()]
		return 'SortedDict(%s)' % ', '.join(prs)
	
	def get(self, key, *arg):
		'''get(key, [default])
		Get the value for @key from the dictionary. If @key is not in the 
		dictionary and @default is supplied, return @default.
		'''
		if len(arg) > 1:
			raise TypeError('Expected at most 2 arguments, got %s' % (len(arg) + 1))
		elif len(arg) == 1:
			ret = self.keydict.get(key, None)
			return self.data[ret] if ret != None else arg[0]
		else:
			return self.data[self.keydict.get(key)]
	__getitem__ = get
	
	def set(self, key, value):
		'Sets the value for @key to @value.'
		k = self.keydict.get(key)
		if k == None:
			self._add(key, value)
		else:
			self.data[k] = value
	__setitem__ = set
	
	def get_at(self, index):
		'''Get the value at @index. Probably quite slow, as the list() side of 
		the dictionary is not favored.'''
		return self.data[self.keydict[self.keys()[index]]]
	def set_at(self, index, value):
		'''Set the value at @index to @value. Probably quite slow, as the 
		list() side of the dictionary is not favored.'''
		self.data[self.keydict[self.keys()[index]]] = value
	def delete_at(self, index):
		'''Delete the value at index.Probably quite slow, as the list() side 
		of the dictionary is not favored.'''
		for p in self.keydict.items():
			if p[1] == index:
				the_pair = p
				break
		del self.keydict[the_pair[0]]
	
	def keys(self):
		kys = self.keydict.keys()
		return sorted(kys, key = self._sorter)
	def values(self):
		return [self.data[self.keydict[k]] for k in self.keys()]
	def items(self):
		return zip(self.keys(), self.values())
	
	def rebuild(self):
		'Remove zombie data from the data store to free up memory.'
		vals = self.keydict.values()
		slen = len(self.data)
		for i, v in enumerate(self.data):
			if not v in vals:
				del self.data[i]
		# Check to see if any changes were made before rebuilding
		if slen != len(self.data):
			self.__init__(vals, self.data)
	
	def _sorter(self, key):
		return self.keydict.get(key)
	def _add(self, key, value):
		self.keydict[key] = len(self.keydict)
		self.data.append(value)

class UpdatingDict(dict):
	'''A dictionary that will notify about changes.
	AUTHORS:
	v0.4.5+		--> pydsigner'''
	def __init__(self, *args, **kw):
		dict.__init__(self, *args, **kw)
		self.n = []
	
	def __delitem__(self, key):
		dict.__delitem__(self, key)
		[obj.update() for obj in self.n]
	def set(self, key, value):
		dict.__setitem__(self, key, value)
		[obj.update() for obj in self.n]
	__setitem__ = set
	
	def add_notify(self, obj):
		'Add @obj to the notification list. '
		if obj not in self.n:
			self.n.append(obj)
	def del_notify(self, obj):
		'''Remove @obj from the notification list. Will raise AssertionError if 
		@obj is not in the notification list.'''
		assert obj in self.n, ('Cannot remove objects from notification list' + 
								' that are not in it!')
		del self.n[self.n.index(obj)]
		
2
class GUIDictItem(tk.Frame):
	'''A basic item for the GUIDict() graphical implementation of a dictionary. 
	NB: This item converts everything to strings, so be careful where you use 
	it.
	AUTHORS:
	v0.4.5+		--> pydsigner'''
	def __init__(self, master, key, value, *args, **kw):
		tk.Frame.__init__(self, master, *args, **kw)
		self.var = tk.StringVar()
		self.var.set(value[0])
		self.key = key
		tk.Label(self, text = self.key).grid(row = 0, column = 0, sticky = W+E)
		tk.Entry(self, textvariable = self.var).grid(row = 0, column = 1, sticky = W+E)
		tk.Button(self, command = self.update, text = 'Update').grid(row = 0, column = 2, sticky = W+E)
		tk.Button(self, command = self.deleter, text = 'Delete').grid(row = 0, column = 3, sticky = W+E)
		self.columnconfigure(0, weight = 6)
		self.columnconfigure(1, weight = 12)
		self.columnconfigure(2, weight = 3)
		self.columnconfigure(3, weight = 1)
	def update(self):
		self.master.set(self.key, [self.var.get()])
	def deleter(self):
		self.master.delete_key(self.key)

class GUIDict(tk.Frame):
	'''A basic GUI implementation of a dictionary.
	AUTHORS:
	v0.4.5+		--> pydsigner'''
	item = GUIDictItem
	def __init__(self, master, dictobj = UpdatingDict(), *args, **kw):
		tk.Frame.__init__(self, master, *args, **kw)
		bbox = tk.Frame(self)
		#tk.Button(bbox, text = 'Delete keys', command = self.deleter).pack(side = LEFT, expand = True, fill = X)
		tk.Button(bbox, text = 'Add key', command = self.adder).pack(side = RIGHT, expand = True, fill = X)
		bbox.pack(side = BOTTOM, expand = True, fill = X)
		self.dictobj = dictobj
		self.dictobj.add_notify(self)
		self.update()
	def __str__(self):
		return str(self.dictobj)
	def __repr__(self):
		return repr(self.dictobj)
	
	def update(self):
		try:
			for item in self.reps.values():
				item.destroy()
		except:
			pass
		self.reps = {}
		for k in sorted(self.dictobj):
			self.reps[k] = self.item(self, k, self.dictobj.get(k))
			self.reps[k].pack(side = TOP, fill = X, expand = True)
	
	def set(self, key, value):
		self.dictobj.set(key, value)
	def delete_key(self, key):
		del self.dictobj[key]
	
	#def deleter(self):
	#	dtop = tk.Toplevel()
	#	dtop.title('Delete keys')
	#	klist = tk.Listbox(dtop)
	#	done = tk.Button(dtop, text = 'Done', command = dtop.destroy)
	#	lab = tk.Label(dtop, text = 'double-click titles to delete those entries.')
	#	def kdlter(self, event):
	#		indexs = klist.curselection()
	#		for index in indexs:
	#			#print(index)
	#			del self.dictobj[rlist[int(index)]]
	#			del rlist[int(index)]
	#			klist.delete(index)
	#	
	#	klist.bind('<Double-1>', lambda e: (kdlter(self, e)))
	#	rlist = list(sorted(self.dictobj))
	#	[klist.insert(END, k) for k in rlist]
	#	lab.pack(side = TOP)
	#	klist.pack(side = TOP)
	#	done.pack(side = TOP)
		
	def adder(self):
		r = askstring('Add key', 'Enter the key to add:')
		if r:
			self.dictobj.set(r, [''])
