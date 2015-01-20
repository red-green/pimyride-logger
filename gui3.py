# gui.py

from Tkinter import *
from obd_sensors import SENSORS as senslist
from obd_io import OBDPort
from obd_utils import scanSerial

width = 800
height= 40
cwidth = 300  # width of canvas (graph)
rwidth = 20  # width of readout text
bufferlen = 50
update_t = 2000

class readout(object):
	def __init__(self,parent,idx,name,sname,units,row):
		self.name = name
		self.index = idx
		self.row = row
		self.sname = sname
		self.unit = units
		self.buffer = []
		self.frame = parent
		self.label = Label(self.frame,fg='green',bg='black',text=self.name)
		self.label.grid(column=0,row=row)
		self.reado = Label(self.frame,fg='red',bg='black',text='0 '+self.unit,width=rwidth)
		self.reado.grid(column=1,row=row)
		self.stats = Label(self.frame,fg='cyan',bg='black',text='-',width=rwidth*3)
		self.stats.grid(column=2,row=row)
		#self.graph = Canvas(self.frame,width=cwidth,height=height)
		#self.graph.grid(column=3,row=row)

	def update(self,data):
		if type(data) is int or type(data) is float:
			self.buffer.append(data)
		if len(self.buffer) > 50:
			self.buffer = self.buffer[1:]
		self.reado = Label(self.frame,fg='red',bg='black',text=str(data) +' '+self.unit,width=rwidth)
		self.reado.grid(column=1,row=self.row)
		if self.buffer:
			bmin = min(self.buffer)
			bmax = max(self.buffer)
			bavg = sum(self.buffer)/len(self.buffer)
			self.stats = self.stats = Label(self.frame,fg='cyan',bg='black',text='Avg: {0} Min: {1} Max: {2}'.format(bavg,bmin,bmax),width=rwidth*3)
			self.stats.grid(column=2,row=self.row)

class panel(object):
	def __init__(self,title,sensors):
		self.mainwin = Tk()
		self.main = Frame(self.mainwin,bg='black')
		self.main.pack()
		self.sensors = {}
		self.sensor_list = []
		self.port = None
		for idx,i in enumerate(sensors):
			sobj = None
			sid = 0
			for si,j in enumerate(senslist):
				if j.shortname == i:
					sobj = j
					sid = si
					break
			if sobj is None:
				continue
			self.sensors[sobj.shortname] = readout(self.main,sid,sobj.name,sobj.shortname,sobj.unit,idx)
			self.sensor_list.append(sid)

	def connect(self):
		self.port = None
		port_names = scanSerial()
		port_names = ['/dev/tty.OBDII-Port','/dev/cu.OBDII_Port'] 
		for port in port_names:
			self.port = OBDPort(port, None, 2, 2)
			if self.port.State == 0:
				self.port.close()
				self.port = None  # no open ports close
			else:
				break  # break with connection
		if self.port:
			print "Connected "

	def run(self):
		self.connect()
		self.mainwin.after(update_t,self.update)
		self.mainwin.mainloop()

	def get_mpg(self, MPH, MAF):
		#Instant_MPG = (14.7 * 8.637571 * 4.54 * MPH) / (3600 * (MAF * 7.5599) / 100)  # Diesel Inaccurate formula
		Instant_MPG = (14.7 * 7.273744 * 4.54 * MPH) / (3600 * MAF / 100)  # Petrol Should accurate
		return Instant_MPG

	def update(self):
		print "update..."
		try:
			result_set = {}
			for index in self.sensor_list:  # log all of our sensors data from sensor_list
				(name, value, unit) = self.port.sensor(index)
				if value == "NORESPONSE":
					self.connect()
					assert self.port is not None
				result_set[senslist[index].shortname] = value  # add data to a result
			result_set['mpg'] = self.get_mpg(result_set["speed"], result_set["maf"])  # calculate mpg
			for i in self.sensors.keys():
				reado = self.sensors[i]
				value = result_set.get(i,"NODATA")
				reado.update(value)
		except:
			pass
		self.mainwin.after(update_t,self.update)

if __name__ == "__main__":
	a = panel("Testing panel",["speed", "mpg", "rpm", "temp", "maf", "load", "throttle_pos"])
	a.run()