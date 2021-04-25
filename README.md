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
#   (Use raspi-config GUI to Enable the SPI Interface)
#	  sudo raspi-config 
#
#   (Add two key libraries...)
#	  git clone https://github.com/adafruit/Adafruit_CircuitPython_Bundle.git
#	  git clone https://github.com/adafruit/circuitpython.git
#	
#   (From <https://www.digitalocean.com/community/tutorials/how-to-set-up-time-synchronization-on-debian-10> )
#   sudo apt-install ntp
#	  sudo systemctl status ntp
#	 
#   (Install Python 3)
#	  sudo apt-get install python3-pip
#	  cd Adafruit_CircuitPython_Bundle/
#	
#   (This next step takes ~33 minutes!)
#	  sudo ./update-submodules.sh    
#	  cd ..
#	
#   (See Adafruit RGB Display Library Documentation)
#   ( https://buildmedia.readthedocs.org/media/pdf/adafruit-circuitpython-rgb-display/latest/adafruit-circuitpython-rgb-display.pdf)
#   sudo pip3 install adafruit-circuitpython-rgb-display
#	 
#   (DejaVu Font family based on the Vera Fonts)
#	  sudo apt-get install ttf-dejavu
#	
#	  (PIL is the Python Imaging Library) 
#	  sudo apt-get install python3-pil
#	
#   (Python Numpy Library)
#	  sudo apt-get install python3-numpy
# **********************************************************************************************************
#	  
# Copy this document over to your RPI via Putty PSFTP ( https://www.puttygen.com/psftp )
#	
#			1.) (Obtain IP address of RPI) 
#			    ifconfig
#			2.) (Open PSFTP on laptop)
#			3.) (Open the connection between your computer and your RPI)
#			    open 192.168.1.39
#			4.) (Point to your local directory where this file is saved)
#			    lcd c:/fromRPI
#			5.) copy this file to your RPI
#			    put vet-track.py
#     6.) (Make the python file executable)
#         Sudo chmod +x vet-track.py
#     7.) (Make this python file run at every reboot automatically)	
#         sudo nano /etc/rc.local
#         (add the below line of code to your rc.local file...)
#         sudo python3 /home/pi/stats_time.py &
# **********************************************************************************************************
