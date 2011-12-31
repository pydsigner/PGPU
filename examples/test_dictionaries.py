import pgpu.dictionaries as ds
from pgpu.compatibility import *
import time

def recursive_size(obj):
	#Print(obj)
	#Print(dir(obj))
	do = [a for a in dir(obj) if not (a.startswith('__') or a.startswith('im_'))]
	#Print(do)
	return obj.__sizeof__() + sum(recursive_size(getattr(obj, a))  for a in do)

class Clueless(object):
	def update(self):
		Print('What happened?')

class TimeBreakdown:
	def __init__(self, method = time.time):
		self.method = method
		self.times = []
	
	def flag(self):
		self.times.append(self.method())
	
	def reset(self):
		self.times = []
	
	def get_vals(self):
		res = []
		last = self.times[0]
		for t in self.times[1:]:
			res.append(t - last)
			last = t
		res.append(self.times[-1] - self.times[0])
		return res
		
	def __str__(self):
		return '\n'.join([str(i) for i in self.get_vals()])

if __name__ == '__main__':
	c = Clueless()
	d = ds.UpdatingDict(a=1,v=3)
	d.add_notify(c)
	del d['v']
	d['c'] = 3
	
	timer = TimeBreakdown()
	d = ds.SortedDict(('a', 1), ('b',2), ('c',3))
	Print(d)
	Print(d.get_at(0))
	d.delete_at(1)
	Print(d['c'])
	timer.flag()
	d.rebuild()
	timer.flag()
	d.rebuild()
	timer.flag()
	Print(timer)
	Print('----')
	timer.reset()
	timer.flag()
	d = ds.SortedDict(range(5500), range(5500))
	timer.flag()
	d[5] = 45
	d[7] = 12424
	del d[2]
	for i in range(5, 150):
		del d[i]
	timer.flag()
	Print(timer)
	Print('----')
	timer.reset()
	Print(recursive_size(d))
	timer.flag()
	d.rebuild()
	timer.flag()
	Print(recursive_size(d))
	Print(timer)
	Print('----')
