#!/usr/bin/env python
import asyncio
import websockets
import json
import time
from random import randint


#ser =serial.Serial("/dev/tty.usbserial", 9600, timeout=1)


async def hello():
	async with websockets.connect('ws://127.0.0.1:4000/socket/websocket') as websocket:
		data = dict(topic="users:YWxleEBnbWFpbC5jb21hbGV4Y29sZXM=", event="phx_join", payload={}, ref=1)
		#data = dict(topic="users:anVhbkBnbWFpbC5jb21qdWxpYTEyMw==", event="phx_join", payload={}, ref=1)
		await websocket.send(json.dumps(data))
		# print("joined")
		#greeting = await websocket.recv()
		print("Joined")
		while True:
			msg = await retrieve()
			await websocket.send(json.dumps(msg))
			#msg = dict(topic="users:YWxleEBnbWFpbC5jb21hbGV4Y29sZXM=", event="shout", payload={"body":"alex"}, ref=None)
			#await websocket.send(json.dumps(msg))
			#print("sent")
			call = await websocket.recv()
			control = json.loads(call)
			#print(control['event'])
			if(control['event'] == "control"):
				print(control['payload']['val'])
			
			print("< {}".format(call))
			time.sleep(3)

async def retrieve():
	
	msg = dict(topic="users:YWxleEBnbWFpbC5jb21hbGV4Y29sZXM=", event="sensor_output", payload={"load":"1000", "pf":str(randint(0,100)), "thd":"120", "reading":"1800"}, ref=None)
	time.sleep(3)
	return msg

		# while True:
		# 	msg = dict(topic="users:anVhbkBnbWFpbC5jb21qdWxpYTEyMw==", event="shout", payload="hello, sir !", ref=None)
		# 	await websocket.send(json.dumps(msg))
		# 	#print("> {}".format(data))
		# 	greeting = await websocket.recv()
		# 	print("< {}".format(greeting))


# async def retrieve():
# 	data = ser.readline().decode()
# 	data_to_be_sent = await concurrent(data)
# 	return(data_to_be_sent)

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