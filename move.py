#! /usr/bin/python

import bot
import sys

if __name__ == "__main__":
	if len(sys.argv) <= 2:
		print "move <xsteps> <ysteps>"
		sys.exit()

	x,y = map(int, sys.argv[1:])
	bot = bot.Bot(speed=10)
	print "Bot version:",bot.get_version(),
	print "Moving",x,y
	bot.move(x,y)
