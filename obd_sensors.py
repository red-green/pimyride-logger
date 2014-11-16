#!/usr/bin/env python
###########################################################################
# obd_sensors.py
#
# Copyright 2004 Donour Sizemore (donour@uchicago.edu)
# Copyright 2009 Secons Ltd. (www.obdtester.com)
#
# This file is part of pyOBD.
#
# pyOBD is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# pyOBD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyOBD; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
###########################################################################

def hex_to_int(str):
    i = eval("0x" + str, {}, {})
    return i


def maf(code):
#code = hex_to_int(code)
#return code * 0.00132276
    numA = hex_to_int(code[:2]) #A byte
    numB = hex_to_int(code[2:4]) #B byte
    code = (numA * 256 + numB) / 100.0
    return code


def throttle_pos(code):
    code = hex_to_int(code)
    return code * 100.0 / 255.0


def intake_m_pres(code): # in kPa
    #code = hex_to_int(code)
    #return code / 0.14504
    numA = hex_to_int(code[:2]) #A byte
    kpa = numA
    return kpa


def FuelRailPressD(code):
    code = hex_to_int(code)
    kpa = (code) * 10
    return kpa


def rpm(code):
    code = hex_to_int(code)
    return code / 4


def speed(code):
    code = hex_to_int(code)
    return code / 1.609


def percent_scale(code):
    code = hex_to_int(code)
    return code * 100.0 / 255.0


def timing_advance(code):
    code = hex_to_int(code)
    return (code - 128) / 2.0


def sec_to_min(code):
    code = hex_to_int(code)
    return code / 60


def temp(code):
    code = hex_to_int(code)
    return code - 40


def cpass(code):
    #fixme
    return code


def fuel_trim_percent(code):
    code = hex_to_int(code)
    return (code - 128.0) * 100.0 / 128


def dtc_decrypt(code):
    #first byte is byte after PID and without spaces
    num = hex_to_int(code[:2]) #A byte
    res = []

    if num & 0x80: # is mil light on
        mil = 1
    else:
        mil = 0

    # bit 0-6 are the number of dtc's. 
    num = num & 0x7f

    res.append(num)
    res.append(mil)

    numB = hex_to_int(code[2:4]) #B byte

    for i in range(0, 3):
        res.append(((numB >> i) & 0x01) + ((numB >> (3 + i)) & 0x02))

    numC = hex_to_int(code[4:6]) #C byte
    numD = hex_to_int(code[6:8]) #D byte

    for i in range(0, 7):
        res.append(((numC >> i) & 0x01) + (((numD >> i) & 0x01) << 1))

    res.append(((numD >> 7) & 0x01))

    return res


def hex_to_bitstring(str):
    bitstring = ""
    for i in str:
        if type(i) == type(''):
            v = eval("0x%s" % i)
            if v & 8:
                bitstring += '1'
            else:
                bitstring += '0'
            if v & 4:
                bitstring += '1'
            else:
                bitstring += '0'
            if v & 2:
                bitstring += '1'
            else:
                bitstring += '0'
            if v & 1:
                bitstring += '1'
            else:
                bitstring += '0'
    return bitstring


def pid151(code):
    fueltype = ""
    code = hex_to_int(code)
    if code == 1:
        fueltype = "Petrol"
    elif code == 2:
        fueltype = "Methanol"
    elif code == 3:
        fueltype = "Ethanol"
    elif code == 4:
        fueltype = "Diesel"
    elif code == 5:
        fueltype = "LPG"
    elif code == 6:
        fueltype = "CNG"
    elif code == 7:
        fueltype = "Propane"
    elif code == 8:
        fueltype = "Electric"
    elif code == 9:
        fueltype = "Bifuel running Gasoline"
    elif code == 10:
        fueltype = "Bifuel running Methanol"
    elif code == 11:
        fueltype = "Bifuel running Ethanol"
    elif code == 12:
        fueltype = "Bifuel running LPG"
    elif code == 13:
        fueltype = "Bifuel running CNG"
    elif code == 14:
        fueltype = "Bifuel running Prop"
    elif code == 15:
        fueltype = "Bifuel running Electricity"
    elif code == 16:
        fueltype = "Bifuel mixed gas/electric"
    elif code == 17:
        fueltype = "Hybrid petrol"
    elif code == 18:
        fueltype = "Hybrid Ethanol"
    elif code == 19:
        fueltype = "Hybrid Diesel"
    elif code == 20:
        fueltype = "Hybrid Electric"
    elif code == 21:
        fueltype = "Hybrid Mixed fuel"
    elif code == 22:
        fueltype = "Hybrid Regenerative"
    else:
        fueltype = "?"

    return fueltype


def pid15e(code):
    numA = hex_to_int(code[:2]) #A byte
    numB = hex_to_int(code[2:4]) #B byte
    l = (numA * 256 + numB) * 0.05
    return l


class Sensor:
    def __init__(self, shortName, sensorName, sensorcommand, sensorValueFunction, u):
        self.shortname = shortName
        self.name = sensorName
        self.cmd = sensorcommand
        self.value = sensorValueFunction
        self.unit = u


SENSORS = [
    Sensor("pids", "          Supported PIDs", "0100", hex_to_bitstring, ""),
    Sensor("dtc_status", "Status Since DTC Cleared", "0101", dtc_decrypt, ""),
    Sensor("dtc_ff", "DTC Causing Freeze Frame", "0102", cpass, ""),
    Sensor("fuel_status", "      Fuel System Status", "0103", cpass, ""),
    Sensor("load", "   Calculated Load Value", "01041", percent_scale, "%"),
    Sensor("temp", "     Coolant Temperature", "0105", temp, "C"),
    Sensor("short_term_fuel_trim_1", "    Short Term Fuel Trim", "0106", fuel_trim_percent, "%"),
    Sensor("long_term_fuel_trim_1", "     Long Term Fuel Trim", "0107", fuel_trim_percent, "%"),
    Sensor("short_term_fuel_trim_2", "    Short Term Fuel Trim", "0108", fuel_trim_percent, "%"),
    Sensor("long_term_fuel_trim_2", "     Long Term Fuel Trim", "0109", fuel_trim_percent, "%"),
    Sensor("fuel_pressure", "      Fuel Rail Pressure", "010A", cpass, ""),
    Sensor("manifold_pressure", "Intake Manifold Pressure", "010B", intake_m_pres, "kpa"),
    Sensor("rpm", "              Engine RPM", "010C1", rpm, ""),
    Sensor("speed", "           Vehicle Speed", "010D1", speed, "MPH"),
    Sensor("timing_advance", "          Timing Advance", "010E", timing_advance, "degrees"),
    Sensor("intake_air_temp", "         Intake Air Temp", "010F", temp, "C"),
    Sensor("maf", "     Air Flow Rate (MAF)", "0110", maf, "g/s"),
    Sensor("throttle_pos", "       Throttle Position", "01111", throttle_pos, "%"),
    Sensor("secondary_air_status", "    Secondary Air Status", "0112", cpass, ""),
    Sensor("o2_sensor_positions", "  Location of O2 sensors", "0113", cpass, ""),
    Sensor("o211", "        O2 Sensor: 1 - 1", "0114", fuel_trim_percent, "%"),
    Sensor("o212", "        O2 Sensor: 1 - 2", "0115", fuel_trim_percent, "%"),
    Sensor("o213", "        O2 Sensor: 1 - 3", "0116", fuel_trim_percent, "%"),
    Sensor("o214", "        O2 Sensor: 1 - 4", "0117", fuel_trim_percent, "%"),
    Sensor("o221", "        O2 Sensor: 2 - 1", "0118", fuel_trim_percent, "%"),
    Sensor("o222", "        O2 Sensor: 2 - 2", "0119", fuel_trim_percent, "%"),
    Sensor("o223", "        O2 Sensor: 2 - 3", "011A", fuel_trim_percent, "%"),
    Sensor("o224", "        O2 Sensor: 2 - 4", "011B", fuel_trim_percent, "%"),
    Sensor("obd_standard", "         OBD Designation", "011C", cpass, ""),
    Sensor("o2_sensor_position_b", "  Location of O2 sensors", "011D", cpass, ""),
    Sensor("aux_input", "        Aux input status", "011E", cpass, ""),
    Sensor("engine_time", " Time Since Engine Start", "011F", sec_to_min, "min"),
    Sensor("engine_mil_time", "  Engine Run with MIL on", "014D", sec_to_min, "min"),
    Sensor("Fuel_Type", " Fuel Type              ", "0151", pid151, "BitEnc."),
    Sensor("Fuel_pressure", " Fuel rail pressure     ", "0123", FuelRailPressD, "kPa"),
    Sensor("fuel_rate", " Engine fuel rate       ", "015E", pid15e, "L/h"),
    Sensor("mpg"," Miles per Gallon", "0000", cpass, "mpg"),   #this one is a dummy to accomidate the 'fake' mpg reading
]


#___________________________________________________________

def test():
    for i in SENSORS:
        print i.name, i.value("F")


if __name__ == "__main__":
    test()
