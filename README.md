pyscan3d
========

Drive modified eggbot controller firmware from Python to act as a makeshift 3D scanner

bot.py 	- contains a class to abstract out the eggbot control. It requires pyserial
scan.py	- will take a 3d scan and output a PGM file. Most values are set in the script.
ver.py	- Shows the eggbot firmware version
move.py	- Move the X/Y axis of the eggbot/plotter
distance-loop.py - Continuously show the distance sensor output for testing
bootloader.py	- Puts the eggbot into bootloader mode so it can be flashed

