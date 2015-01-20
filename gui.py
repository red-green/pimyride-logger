# gui.py

from Tkinter import *
from obd_sensors import SENSORS as senslist
from threading import Thread
from random import randint

width = 800
height= 40
cwidth = 300  # width of canvas (graph)
rwidth = 20  # width of readout text
bufferlen = cwidth/5

class readout(object):
	def __init__(self,parent,name,sname,units,row):
		self.name = name
		self.sname = sname
		self.unit = units
		self.buffer = [0]*50
		self.frame = Frame(parent,width=width,height=height,borderwidth=0,bg='black')
		self.label = Label(self.frame,fg='green',bg='black',text=self.name)
		self.label.grid(column=0,row=0)
		self.reado = Label(self.frame,fg='red',bg='black',text='0 '+self.unit,width=rwidth)
		self.reado.grid(column=1,row=0)
		self.graph = Canvas(self.frame,width=cwidth,height=height)
		self.graph.grid(column=2,row=0)
		self.frame.pack_propagate(0)
		self.frame.grid(column=0,row=row)

	def update(self,data):
		self.buffer = self.buffer[1:]
		self.buffer.append(data)
		self.reado.text = str(data) + ' ' + self.unit


class panel(object):
	def __init__(self,title,sensors):
		self.main = Tk()
		self.sensors = {}
		for idx,i in enumerate(sensors):
			sobj = None
			for j in senslist:
				if j.shortname == i:
					sobj = j
					break
			if sobj is None:
				continue
			self.sensors[sobj.shortname] = readout(self.main,sobj.name,sobj.shortname,sobj.unit,idx)
		self.thread = Thread(target=self.main.mainloop())
		self.thread.run()

if __name__ == "__main__":
	a = panel("Testing panel",["speed", "mpg", "rpm", "temp", "maf"])