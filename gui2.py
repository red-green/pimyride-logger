# gui.py
## gui interface for my fork of piMyRide
## by Jackon Servheen
## CC BY-NC-SA 2.0

from Tkinter import *
from obd_sensors import SENSORS as senslist
from threading import Thread
from random import randint
from time import sleep

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
		self.label = Label(parent,fg='green',bg='black',text=self.name)
		self.label.grid(column=0,row=row)
		self.reado = Label(parent,fg='red',bg='black',text='0 '+self.unit,width=rwidth)
		self.reado.grid(column=1,row=row)
		self.graph = Canvas(parent,width=cwidth,height=height,bg='grey')
		self.graph.grid(column=2,row=row)

	def update(self,data):
		self.buffer = self.buffer[1:]
		self.buffer.append(data)
		self.reado.text = str(data) + ' ' + self.unit


class panel(Thread):
	def run(self,title,sensors):
		self.mainwin = Tk()
		self.main = Frame(self.mainwin,bg='black')
		self.main.pack()
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
		self.mainwin.mainloop()
		
	def __init__(self,title,sensors):
		Thread.__init__(self)
		self.start()
		

if __name__ == "__main__":
	s = ["speed", "mpg", "rpm", "temp", "maf"]
	a = panel("Testing panel",s)
	sleep(5)
	while 1:
		for i in s:
			sobj = a.sensors.get(i,None)
			if sobj is None:
				continue
			sobj.update(randint(0,50))
			print i
		sleep(2)
