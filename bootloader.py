#! /usr/bin/python

import bot

if __name__ == "__main__":
	bot = bot.Bot()
	print "Bot version:",bot.get_version()
	print bot.bootloader()
