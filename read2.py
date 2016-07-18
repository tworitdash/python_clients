#!/usr/bin/env python
import asyncio
import websockets
import json
import time
from random import randint
import serial

from pyfirmata import Arduino, util

board = Arduino('/dev/ttyACM1')

it = util.Iterator(board)
it.start()
board.analog[0].enable_reporting()
board.analog[1].enable_reporting()
board.analog[2].enable_reporting()
board.analog[3].enable_reporting()

import RPi.GPIO as gpio

#ser =serial.Serial("/dev/ttyACM0", 9600, timeout=1)


gpio.setmode(gpio.BCM)
gpio.setup(14, gpio.OUT)


async def hello():
	async with websockets.connect('ws://192.168.43.26:4000/socket/websocket') as websocket:
		data = dict(topic="users:YWxleEBnbWFpbC5jb21hbGV4Y29sZXM=", event="phx_join", payload={}, ref=1)
		#data = dict(topic="users:anVhbkBnbWFpbC5jb21qdWxpYTEyMw==", event="phx_join", payload={}, ref=None)
		await websocket.send(json.dumps(data))
		# print("joined")
		#greeting = await websocket.recv()
		print("Joined")
		#a = ""
		while True:
			msg = await retrieve()
			#await websocket.send(json.dumps(msg))
			#msg = dict(topic="users:YWxleEBnbWFpbC5jb21hbGV4Y29sZXM=", event="shout", payload={"body":"alex"}, ref=None)
			await websocket.send(json.dumps(msg))
			#print("sent")
			call = await websocket.recv()
			control = json.loads(call)
			#print(control['event'])
			if(control['event'] == "control"):
				event(control['payload']['val'])
				
			
			print("< {}".format(call))
			#time.sleep(0.1)
def event(val):
	if(val == "on"):
		gpio.output(14, True)
	if(val == "off"):
		gpio.output(14, False)

async def retrieve():
	#ser.write("&".encode())
	load = board.analog[0].read()
	print(load)
	pf = board.analog[1].read()
	print(pf)
	reading = board.analog[2].read()
	print(reading)
	#pf = analog['analog'][1]
	#reading = analog['analog'][2]
	thd = board.analog[3].read()
	print(thd)
	output = {"load": load, "pf": pf, "reading": reading,"thd": thd}
		
	msg = dict(topic="users:YWxleEBnbWFpbC5jb21hbGV4Y29sZXM=", event="sensor_output", payload=output, ref=None)
 	#data_to_be_sent = await concurrent(data)
	print(msg)
	return(msg)


	

# async def concurrent(data):	
# 	#while True:
# 	for line in data.split('\n'):
# 		if line.startswith('$GPGGA'):
# 			#if pynmea2.ChecksumError(line):
# 			try:
# 				msg = pynmea2.parse(line)
# 				print(msg)
# 				lat = msg.latitude
# 				lng = msg.longitude
# 				print(lat, lng)
# 				coordinate = str(lat) + ', ' + str(lng)
# 				print(coordinate)
# 				geolocator = Nominatim()
# 				location = geolocator.reverse(coordinate,timeout=10)
# 				return(location.address)
# 			except(ChecksumError, ParseError, KeyError) as e:
# 				print(e)
				
			




asyncio.get_event_loop().run_until_complete(hello())
asyncio.get_event_loop().run_forever()
