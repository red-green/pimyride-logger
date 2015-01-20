from serial.tools.list_ports import comports

def scanSerial():
	"""scan for available ports. return a list of serial names"""
	try:
		available = [i[0] for i in comports()]
		return available
	except:
		return ['/dev/tty.OBDII-Port','/dev/cu.OBDII_Port']

if __name__ == "__main__":
	print scanSerial()