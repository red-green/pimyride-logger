PyMyRide - a simple gui and cli for OBD reading
===

How to run
---

- To run the CLI, `python main.py`
  - you may need to edit the line `port_names = scanSerial()` . It has problems on some computers, so you may need to make a list of the serial ports like i did
- TO run the GUI, `python gui3.py` (the other two don't work)
  - you may need to edit the serial port list as well (in `panel.connect()`)

