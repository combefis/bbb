#!/usr/bin/env python
# sonar.py
# author: Sébastien Combéfis
# version: February 28, 2017

import ctypes
import signal
import time

import Adafruit_BBIO.GPIO as GPIO

libc = ctypes.CDLL('libc.so.6')

def delayMicroseconds(us):
	libc.usleep(int(us))

class Timeout:
	class Timeout(Exception):
		pass

	def __init__(self, seconds):
		self.seconds = seconds

	def __enter__(self):
		signal.signal(signal.SIGALRM, self.raiseTimeout)
		signal.alarm(self.seconds)

	def __exit__(self, *args):
		signal.alarm(0)

	def raiseTimeout(self, *args):
		raise Timeout.Timeout()

def sendPulse(pin):
	"""Send a 10us pulse on specified input pin"""
        GPIO.output(pin, GPIO.LOW)
        delayMicroseconds(2)
        GPIO.output(pin, GPIO.HIGH)
        delayMicroseconds(10)
        GPIO.output(pin, GPIO.LOW)

def pulseIn(pin):
	"""Measure the length of a pulse in seconds on a specified pin"""
	try:
		with Timeout(1):
			while not GPIO.input(pin):
				delayMicroseconds(1)
			start = time.time() * 1000
			while GPIO.input(pin):
				delayMicroseconds(1)
			return (time.time() * 1000 - start) / 1000
	except Timeout.Timeout:
		return None

if __name__ == "__main__":
	GPIO.setup("P9_12", GPIO.OUT)
	GPIO.setup("P9_15", GPIO.IN)

	N = 100
	i, distance = 0, 0
	while True:
		sendPulse("P9_12")
		duration = pulseIn("P9_15")
		if duration:
			distance += duration * 340 / 2
			i += 1
			if i == N:
				print("Distance: {}cm".format(distance / N * 100))
				i, distance = 0, 0
		else:
			print('Measure failed')
		delayMicroseconds(1000)