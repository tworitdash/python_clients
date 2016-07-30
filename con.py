import asyncio
import RPi.GPIO as gpio

gpio.setmode(gpio.BCM)
gpio.setup(14, gpio.IN)
gpio.setup(15, gpio.IN)

async def read14():
	print("fetching data from pin 14")
	data14 = gpio.input(14)
	#await asyncio.sleep(2)
	await asyncio.sleep(2)
	return("result of 14: {}".format(data14))

async def read15():
	print("fetching data from pin 15")
	data15 = gpio.input(15)
	await asyncio.sleep(2)
	return("result of 15: {}".format(data15))

async def main():
	print('starting main')
	phases = {
		read14(),
		read15()
	}
	print("waiting for read operations to complete !")
	results = []
	for next_to_complete in asyncio.as_completed(phases):
		answer = await next_to_complete
		print('received answer: {!r}'.format(answer))
		results.append(answer)

	print("results {!r}".format(results))
	return(results)

loop = asyncio.get_event_loop()

try:
	while True:
		loop.run_until_complete(main())
	#loop.run_forever()
finally:
	loop.close()
