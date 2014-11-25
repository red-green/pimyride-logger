#!/usr/bin/env python

###########################################################################
# main.py
#
# Copyright 2013 Alan Kehoe, David O'Regan (www.pimyride.com)
# Copyright 2014 Jackson Servheen
#
# This file was part of PiMyRide.
#
# PiMyRide is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# PiMyRide is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PiMyRide; if not, visit http://www.gnu.org/licenses/gpl.html
###########################################################################

from datetime import datetime
from obd_utils import scanSerial
from time import sleep
import sys
import os

import obd_io
import obd_sensors

#from gui import panel


class OBDLogger():
	def __init__(self, log_sensors):
		self.port = None
		self.sensor_log = log_sensors
		self.sensor_list = []
		for sensor in log_sensors:
			self.add_log_sensor(sensor)
		#self.panel = panel()

	def connect(self):
		#port_names = scanSerial()  # Check all serial ports.
		port_names = ['/dev/tty.OBDII-Port','/dev/tty.usbserial-A60292K6','/dev/cu.usbserial-A60292K6'] # scanSerial errors for me
		print port_names  # print available ports
		for port in port_names:
			self.port = obd_io.OBDPort(port, None, 2, 2)
			if self.port.State == 0:
				self.port.close()
				self.port = None  # no open ports close
			else:
				break  # break with connection

		if self.port:
			print "Connected "

	def is_connected(self):  # check if connected
		return self.port

	# add the sensors to read from from the list below. this sensors are in obd_sensors.py
	def add_log_sensor(self, sensor):
		for index, e in enumerate(obd_sensors.SENSORS):
			if sensor == e.shortname:
				self.sensor_list.append(index)
				print "Logging Sensor: " + e.name  # logging this sensor
				break

	def get_sensor(self, sensor):
		for index, e in enumerate(obd_sensors.SENSORS):
			if sensor == e.shortname:
				return e

	def get_mpg(self, MPH, MAF):
		#Instant_MPG = (14.7 * 8.637571 * 4.54 * MPH) / (3600 * (MAF * 7.5599) / 100)  # Diesel Inaccurate formula
		Instant_MPG = (14.7 * 7.273744 * 4.54 * MPH) / (3600 * MAF / 100)  # Petrol Should accurate
		return Instant_MPG

	def run(self):  # logging starts
		if self.port is None:
			return None  # leave if there is no connection

		print "Started"

		while 1:
			result_set = {}
			for index in self.sensor_list:  # log all of our sensors data from sensor_list
				(name, value, unit) = self.port.sensor(index)
				result_set[obd_sensors.SENSORS[index].shortname] = value  # add data to a result
			result_set['mpg'] = self.get_mpg(result_set["speed"], result_set["maf"])  # calculate mpg
			
			os.system('clear')
			for name in self.sensor_log:
				val = result_set[name]
				sen = self.get_sensor(name)
				print sen.name.strip(),':',val,sen.unit
			sleep(1)



log_sensors = ["speed", "mpg", "rpm", "throttle_pos", "load", "temp", "intake_air_temp", "manifold_pressure", "maf", "o211", "fuel_pressure", "pressure"]
obd = OBDLogger(log_sensors)
obd.connect()
if not obd.is_connected():
	print "Not connected"
obd.run()

