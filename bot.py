#! /usr/bin/python

'''Simple Hacked EggBot controller'''

# pyserial. If you're using Debian or Ubuntu just:
# apt-get install python-serial
import serial 
import time


class Bot(object):
	def __init__(self, port="/dev/ttyACM0", speed=5):
		'''create a bot interface
		speed is in microsteps per millisecond
		'''
		ser = serial.Serial(port, timeout=1)
		ser.setRTS()
                ser.setDTR()  
		ser.flushInput()
		ser.flushOutput()
                time.sleep( 0.1 )

		self.ser = ser
		self.speed = speed

	def _flushin(self):
		iw = self.ser.inWaiting()
		if iw: print "(Flushed",iw,"bytes)",
		print self.ser.read(iw)
		self.ser.flushInput()

	def send_command(self,cmd):
		self.ser.write(cmd+'\r\n')
		ack = self.ser.readline()
		if ack.strip() != "OK":
			print "Spurious input when ACK expected from",cmd,":",ack

	def get_version(self):
		self._flushin()
		self.ser.write("V\r\n")
		return self.ser.readline()

	def input_to_volts(self, inp):
		'''convert the analog input value to a voltage'''
		return inp / 1024. * 3.3

	def get_inputs(self):
		'''return the analog inputs from the QC command'''
		self.ser.write("QC\r\n")
		inps = self.ser.readline().strip()
		ack = self.ser.readline().strip()
		if ack != "OK":
			print "Spurious input when ACK expected from QC:",ack
		return map(int,inps.split(','))

	def enable_analog_input(self):
		self.send_command('EA')
		ignored = self.get_inputs()  # Required for first shot of timer for some reason

	def get_analog_input(self):
		'''return the first sampled analog input
		'''
		self.ser.write("A\r\n")
		inp = self.ser.readline().strip()
		if inp[0:2] != 'A,':
			print "Spurious input when A value expected:",inp
			return 0
		return int(inp[2:])

	def bootloader(self):
		'''put the bot into bootloader mode
		WARNING: This will let you flash the PIC
		'''
		self.ser.write("BL\r\n")

	STEP_OFF = 0
	STEP_DIV_16 = 1
	STEP_DIV_8 = 2
	STEP_DIV_4 = 3
	STEP_DIV_2 = 4
	STEP_DIV_1 = 5
	def set_stepper_divider(self,divider):
		cmd = "EM,%d" % (divider,)
		self.send_command(cmd)

	def move(self, xsteps, ysteps, block=True):
		# invert X input 
		xsteps = -xsteps
		# How long shall we take?
		t = max(abs(xsteps),abs(ysteps)) / self.speed
		# SM: Move Stepper Motor.
		# Args are milliseconds for move,xsteps, ysteps
		cmd = "SM,%d,%d,%d" % (t,xsteps,ysteps)
		self.send_command(cmd)
		if block:
			time.sleep(t/1000) # Wait for the move

if __name__ == "__main__":
	bot = Bot(speed=10)
	print bot.get_version()
	print bot.get_inputs()
	bot.move(-1000,0)
	bot.move(1000,0)
	bot.move(0,-1000)
	bot.move(0,1000)
