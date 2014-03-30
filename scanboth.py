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
	height = 3000

	width /= stepby
	height /= stepby

	bot = Bot(speed=0.3)
	#bot = Bot(speed=6)

	print "Bot version:",bot.get_version(),

	bot.enable_analog_input()
	bot.set_stepper_divider(bot.STEP_DIV_1)

	print "scanning grid ",width,"x",height
	print >>outf, "P2"	# PGM with ascii values
	print >>outf, width, height
	print >>outf, 1024

	for j in xrange(height/2):
		# scan line
		print "LINE",j*2
		for i in xrange(width):
			# record
			time.sleep(0.1)
			val = bot.get_analog_input()
			print calib(val),
			print >>outf, calib(val),
			# move		
			bot.move(stepby,0)
		print >>outf
		print

		# move down
		bot.move(0,-stepby)

		print "LINE ",j*2+1
		out = list()
		for i in xrange(width):
			# move		
			bot.move(-stepby,0)
			# record
			time.sleep(0.1)
			val = bot.get_analog_input()
			print calib(val),
			out.insert(0, calib(val))
		print >>outf, " ".join(map(str, out))
		print

		# move down
		bot.move(0,-stepby)

	# Move back up
	bot.move(0,stepby*height)

	bot.set_stepper_divider(bot.STEP_DIV_16)
	outf.close()
