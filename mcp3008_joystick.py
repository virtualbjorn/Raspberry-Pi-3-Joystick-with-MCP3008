#!/usr/bin/python
#--------------------------------------   
# This script reads data from a 
# MCP3008 ADC device using the SPI bus.
#
# Analogue joystick version!
#
# Author : Matt Hawkins
# Date   : 25/12/2017
# Revised: Bryan Jim Paano
# Date Revised: 17/03/2018
# http://www.raspberrypi-spy.co.uk/
#
#--------------------------------------

import spidev
from time import sleep, strftime
from datetime import datetime
from subprocess import *
import lcd
lcd.lcd_init()

# Open SPI bus
spi = spidev.SpiDev()
spi.max_speed_hz=1000000

# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data
 
# Define sensor channels
# (channels 3 to 7 unused)
swt_channel = 0
vrx_channel = 1
vry_channel = 2

# Define delay between readings (s)
delay = 0.05
def main():
    # Print out results
    try:
        while True:
        # Read the joystick position data
            vrx_pos = ReadChannel(vrx_channel)
            vry_pos = ReadChannel(vry_channel)

            # Read switch state
            swt_val = ReadChannel(swt_channel)
            if(swt_val>1):
                swt_state =  'OFF'
            else:
                swt_state = 'ON'
            lcd.lcd_byte(lcd.LCD_LINE_1, lcd.LCD_CMD)
            lcd.lcd_string("X: {}: Y: {}".format(vrx_pos,vry_pos),1)
            lcd.lcd_byte(lcd.LCD_LINE_2, lcd.LCD_CMD)
            lcd.lcd_string("Switch: {}".format(swt_state),1)
            print("--------------------------------------------")
            print("X: {}  Y: {}  Switch : {}".format(vrx_pos,vry_pos,swt_state))
            sleep(0.1)
    except KeyboardInterrupt:
        print('Interrupted by Keyboard')
    finally:
        lcd.GPIO.cleanup()
  # Wait before repeating loop

if __name__ == '__main__':
    main()
