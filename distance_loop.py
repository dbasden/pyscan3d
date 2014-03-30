#! /usr/bin/python

from bot import Bot
import time

if __name__ == "__main__":
	b = Bot()
	print b.get_version()
	b.enable_analog_input()
	while True:
		print b.get_analog_input()
		time.sleep(.1)
