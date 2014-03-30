#! /usr/bin/python

from bot import Bot
import sys
import time

def calib(n):
	return max(0,n-150)

if __name__ == "__main__":
	print "MUST START AT TOP LEFT"

	if len(sys.argv) <= 1:
		print "simplescan <outfile>"
		sys.exit()
	outf = open(sys.argv[1],"w")


	# Using 60,000 steps wide by 30,000 steps deep
	# Origin is at bottom left, but our scan starts top left
	stepby = 10
	width = 1500 
	height = 1000

	width /= stepby
	height /= stepby

	bot = Bot(speed=0.3)
	#bot = Bot(speed=6)

	print "Bot version:",bot.get_version(),

	bot.enable_analog_input()
	bot.set_stepper_divider(bot.STEP_DIV_1)

	relx = 0
	rely = 0

	print "scanning grid ",width,"x",height
	print >>outf, "P2"	# PGM with ascii values
	print >>outf, width, height
	print >>outf, 1024

	for j in xrange(height):
		# scan line
		print "LINE",j
		for i in xrange(width):
			# record
			time.sleep(0.1)
			val = bot.get_analog_input()
			#print val,calib(val), '@',relx, rely
			print calib(val),
			print >>outf, calib(val),
			# move		
			bot.move(stepby,0)
			relx += stepby
		print >>outf
		print

		# retrace
		for i in xrange(width):
			bot.move(-stepby,0)
			relx -= stepby

		# move down
		bot.move(0,-stepby)
		rely -= stepby

	# Move back up
	bot.move(0,stepby*height)

	bot.set_stepper_divider(bot.STEP_DIV_16)
	outf.close()
