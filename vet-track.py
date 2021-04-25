# **********************************************************************************************************
# Crypto Tracker
# by @cloudchamber4
# 24 April 2021
# **********************************************************************************************************
# Hardware Used (~$25 USD): 
#
#  Raspberry Pi Zero W: 
#   ( https://www.raspberrypi.org/products/raspberry-pi-zero-w/ )
#
#  Adafruit Mini PiTFT 135x240 Color Display 
#   ( https://shop.pimoroni.com/products/adafruit-mini-pitft-135x240-color-tft-add-on-for-raspberry-pi )
#   
# **********************************************************************************************************
# RPI Configuration Steps:
#
#   Lots of tutorials out there far better than mine, but below are the key steps
#
#   	(Use raspi-config GUI to Enable the SPI Interface)
#	sudo raspi-config 
#
#   	(Add two key libraries...)
#	git clone https://github.com/adafruit/Adafruit_CircuitPython_Bundle.git
#	git clone https://github.com/adafruit/circuitpython.git
#	
#   	(From <https://www.digitalocean.com/community/tutorials/how-to-set-up-time-synchronization-on-debian-10> )
#   	sudo apt-install ntp
#	sudo systemctl status ntp
#	 
#   	(Install Python 3)
#	sudo apt-get install python3-pip
#	cd Adafruit_CircuitPython_Bundle/
#	
#   	(This next step takes ~33 minutes!)
#	sudo ./update-submodules.sh    
#	cd ..
#	
#   	(See Adafruit RGB Display Library Documentation)
#   	( https://buildmedia.readthedocs.org/media/pdf/adafruit-circuitpython-rgb-display/latest/adafruit-circuitpython-rgb-display.pdf)
#   	sudo pip3 install adafruit-circuitpython-rgb-display
#	 
#   	(DejaVu Font family based on the Vera Fonts)
#	sudo apt-get install ttf-dejavu
#	
#	(PIL is the Python Imaging Library) 
#	sudo apt-get install python3-pil
#	
#   	(Python Numpy Library)
#	sudo apt-get install python3-numpy
# **********************************************************************************************************
#	  
# Copy this document over to your RPI via Putty PSFTP ( https://www.puttygen.com/psftp )
#	
#	1.) (Obtain IP address of RPI) 
#	    ifconfig
#	2.) (Open PSFTP on laptop)
#	3.) (Open the connection between your computer and your RPI)
#	    open 192.168.1.39
#	4.) (Point to your local directory where this file is saved)
#	    lcd c:/fromRPI
#	5.) copy this file to your RPI
#	    put vet-track.py
#       6.) (Make the python file executable)
#           Sudo chmod +x vet-track.py
#       7.) (Make this python file run at every reboot automatically)	
#           sudo nano /etc/rc.local
#           (add the below line of code to your rc.local file...)
#           sudo python3 /home/pi/stats_time.py &
# **********************************************************************************************************
#Code below:
import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
import json
import cfscrape

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(spi, cs=cs_pin, dc=dc_pin, rst=reset_pin, baudrate=BAUDRATE,
width=135, height=240, x_offset=53, y_offset=40)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new('RGB', (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding

# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Alternatively load a TTF font. Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 24)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

#primary loop...
while True:
	# Crypto Tracker
	scraper = cfscrape.create_scraper()
	url = 'https://api.cryptonator.com/api/ticker/vet-usd'
	cfurl = scraper.get(url).content

	data = json.loads(cfurl)

	coin = data['ticker']['base']
	currency = data['ticker']['target']
	price = data['ticker']['price'][0:6] #First 4 decimal places
	volume = data['ticker']['volume']
	change = data['ticker']['change'][0:5]
	float_change = 100 * float(change)
	string_change = str(float_change)

	# Draw a black filled box to clear the image.
	draw.rectangle((0, 0, width, height), outline=0, fill=0)

	# Shell scripts for system monitoring from here:
	# https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-andcpu-load

   	#1 TITLE:
	cmd = "echo VeChain Tracker"
	Title = subprocess.check_output(cmd, shell=True).decode("utf-8")

	#2 Time:
	cmd = "date +%H:%M:%S | cut -d\' \' -f1"
	Time = "TIME: "+subprocess.check_output(cmd, shell=True).decode("utf-8")

   	#3 Date:
	cmd = "date -I | cut -d\' \' -f1"
	Date = "DATE: "+subprocess.check_output(cmd, shell=True).decode("utf-8")

   	#4 COIN:
	cmd = "echo coin"
	Coin = "COIN: "+subprocess.check_output(cmd, shell=True).decode("utf-8")

   	#5 Price:
	Price = "VeChain: " + price

   	#6 % Change:
	Change = "%Ch. 1-hr: " + string_change + "%"

	# Write five lines of text.
	y = top

	#1st LINE:
	#TITLE
	draw.text((x,y), Title, font=font, fill="#6495ED") #CornFlowerBlue
	y += font.getsize(Title)[1]

	#2nd LINE:
	#DATE
	draw.text((x, y), Date, font=font, fill="#FFFAFA") #Snow White
	y += font.getsize(Date)[1]

   	#3rd LINE:
	#TIME
	draw.text((x, y), Time, font=font, fill="#FFFF00") #Yellow
	y += font.getsize(Time)[1]

	#4th LINE
	#PRICE
	draw.text((x, y), Price, font=font, fill="#00FA9A") #Medium Spring Green
	y += font.getsize(Price)[1]

	#5th Price:
	#% CHANGE (past 1-hr)
    	#Color Code %change, with "+%" = Green; "-%"=RED
	if float_change > 0:
		draw.text((x, y), Change, font=font, fill="#00FF00") #Lime Green
	else:
		draw.text((x, y), Change, font=font, fill="#DC143C")  #Crimson
	y += font.getsize(Change)[1]

	# Display image.
	disp.image(image, rotation)

	# Update every 500ms...
	time.sleep(.5)
