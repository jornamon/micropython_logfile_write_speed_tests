import machine
from machine import SPI, SoftSPI, Pin
import os
import time
import sdcard


# FeatherS3 main SPI
SCK = Pin(36)
MOSI = Pin(35)
MISO = Pin(37)
CS = Pin(3) # Pin 3 is fixed if you want to use Adalogger Featherwing
SPI_N = const(2)

#Pi Pico main SPI
# SCK = Pin(18)
# MOSI = Pin(19)
# MISO = Pin(16)
# CS = Pin(17)
# SPI_N = const(0)

spi = SPI(SPI_N,sck=SCK, mosi=MOSI, miso=MISO)
sd = sdcard.SDCard(spi,CS) 
time.sleep(0.5)
os.mount(sd, "/sd")
