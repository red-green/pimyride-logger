# gui.py

from Tkinter import *
from obd_sensors import SENSORS as senslist

class readout(object):
	width = 600
	height= 70
	cwidth = 200  # width of canvas (graph)
	bufferlen = cwidth/5

	def __init__(self,parent,name,sname,units):
		self.name = name
		self.sname = sname
		self.unit = units
		self.buffer = [0]*50
		self.frame = Frame(master=parent,width=width,height=height,borderwidth=2,bg='black')
		self.label = Label(self.frame,fg='green',bg='black',text=self.name)
		self.label.grid(column=0)
		self.readout = Label(self.frame,fg='red',bg='black',text='0'+self.unit)
		self.readout.grid(column=1)
		self.graph = Canvas(self.frame,width=cwidth,height=height)
		self.graph.grid(column=2)

	def update(self,data):
		self.buffer = self.buffer[1:] + [data]


class panel(object):
	def __init__(self,title,sensors):
		self.main = Tk()
		# ummmmmmmmmmm i'll just stop here for now