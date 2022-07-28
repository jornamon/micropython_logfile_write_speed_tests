import machine
from machine import SPI, SoftSPI, Pin
import os
import time
import random
import sdcard

ROWS = const(500)				# Number of sample cycles
COLUMNS = const(50)				# Number of data values generated each sample cycle
SENSOR_DELAY = const(10)		# Sample period. The delay each sampling loop introduces

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

spi = SPI(SPI_N,sck=SCK, mosi=MOSI, miso=MISO,baudrate=80_000_000)
sd = sdcard.SDCard(spi,CS, baudrate=80_000_000) 
time.sleep(0.25)
os.mount(sd, "/sd")
time.sleep(0.25)
fp = open('/sd/test_data.txt','w')

start_total_time = time.ticks_ms()

for _ in range(ROWS):
    start_loop_time = time.ticks_ms()
    
    data_line = [random.randint(0,255000) for _ in range(COLUMNS)]
    time.sleep_ms(SENSOR_DELAY)

    # Write line to file
    
    fp.write(str(data_line)+'\n')
    # fp.flush() # flushing every line takes muuuuuuch more time ~2x time compared to default buffering behaviour    
    print(time.ticks_diff(time.ticks_ms(), start_loop_time))
    
fp.close()
print(f"Total time (ms) {time.ticks_diff(time.ticks_ms(), start_total_time)}")