# Libraries
from PIL import ImageFont, ImageDraw, Image
from os import system, path, getenv
from socket import gethostbyname, gethostname
from time import sleep
from datetime import datetime
from waveshare_epd import epd2in13b_V3
from dotenv import load_dotenv
import RPi.GPIO as GPIO

# Environment variables
load_dotenv(path.join(path.dirname(__file__), '.env'))

# DEBUG
LOG_FILE_PATH = path.join(path.dirname(__file__), getenv('LOG_FILE_PATH'))

# FUNCS
def log(msg):
	print(f"{datetime.now().strftime('%d/%m/%Y | %H:%M:%S')} | {msg}", file = open(LOG_FILE_PATH, "a"))

def disableSSH():
	log("SSH stopped")
	system("sudo systemctl stop ssh")

def enableSSH():
	log("SSH started")
	system("sudo systemctl start ssh")

def getIP():
	return gethostbyname(gethostname())

# SUPERVISOR
class Supervisor:
	def __init__(self, screen, switchPin, fontFilePath):
		self._switchPin = switchPin
		self._switchState = False
		self._screen = screen
		self._font = ImageFont.truetype(fontFilePath, 30)
		self._ip = ""
		self._screen.init()
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self._switchPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		log("Supervisor initialized")

	def updateScreen(self):
		log("Screen Updated")
		# Initialisation
		HBlackimage = Image.new('1', (self._screen.height, self._screen.width), 255)
		HRedimage = Image.new('1', (self._screen.height, self._screen.width), 255)
		drawblack = ImageDraw.Draw(HBlackimage)
		# Buffer drawing
		drawblack.rectangle((0, 0, self._screen.height, self._screen.width), fill = 0)
		drawblack.text((10, 0), "IP:", font = self._font, fill = 1)
		drawblack.text((10, 30), self._ip, font = self._font, fill = 1)
		if (self._switchState):
			drawblack.text((10, 60), "SSH: On", font = self._font, fill = 1)
		else:
			drawblack.text((10, 60), "SSH: Off", font = self._font, fill = 1)
		# Screen Displaying
		self._screen.display(self._screen.getbuffer(HBlackimage), self._screen.getbuffer(HRedimage))

	def update(self):
		if (not(GPIO.input(self._switchPin)) != self._switchState):
			self._switchState = not(GPIO.input(self._switchPin))
			if (self._switchState):
				enableSSH()
			else:
				disableSSH()
			self.updateScreen()
		if (self._ip != getIP()):
			self._ip = getIP()
			self.updateScreen()

supervisor = Supervisor(epd2in13b_V3.EPD(), getenv('SSH_SWITCH_PIN'), path.join(path.dirname(__file__), getenv('FONT_PATH')))

# LOOP
while True:
	supervisor.update()