#! /usr/bin/python

import bot
import sys

if __name__ == "__main__":
	if len(sys.argv) <= 2:
		print "move <xsteps> <ysteps>"
		sys.exit()
	x,y = map(int, sys.argv[1:])
	bot = bot.Bot(speed=0.5)
	print "Bot version:",bot.get_version(),

	print "Setting step divider to 1"
	bot.set_stepper_divider(bot.STEP_DIV_1)

	print "Moving",x,y
	bot.move(x,y)

	print "Setting step divider to 16"
	bot.set_stepper_divider(bot.STEP_DIV_16)
