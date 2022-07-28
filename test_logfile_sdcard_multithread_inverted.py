import machine
from machine import SPI, SoftSPI, Pin
import os
import time
import random
import _thread
import queue
import gc
import sdcard

#Inverted version
#core0: read sensor and write queue
#core1: read queue and write file


ROWS = const(500)				# Number of sample cycles
COLUMNS = const(50)				# Number of data values generated each sample cycle
SENSOR_DELAY = const(10)		# Sample period. The delay each sampling loop introduces
CORE0_DELAY = const(3)			# Small delay in core0 loop
GC_FREQ = const(999999)         # Execute gc.collect() every X samples. For no explicit call to gc.collect use GC_FREQ > ROWS




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
time.sleep(0.25)
os.mount(sd, "/sd")
time.sleep(0.25)
fp = open('/sd/fc_data/test_data.txt','w')
print("File opened",fp)

def core1(q_data):
    
    global core0ends
    global core1ends
    q_size_max = 0
    q_size = 0 
    
    while not core0ends or not q_data.empty():
        if not q_data.empty():
            core1_buffer = q_data.get()
            fp.write(str(core1_buffer)+'\n')
            #print((core0_buffer[0],core0_buffer[1],gc.mem_free()))
            q_size = q_data.qsize()
            #print(core1_buffer[1],q_size)
            #print((core0_buffer[1],q_data.qsize()/10,gc.mem_free()/1024/10))
            #print(core0_buffer[1])
        q_size_max = max(q_size,q_size_max)
        time.sleep_ms(CORE0_DELAY)
    
    core1ends = True
    print("ROWS = ",ROWS)
    print("q_size_max = ",q_size_max)
    print("q_size_max / ROWS = ",q_size_max/ROWS)
    time.sleep_ms(20)
    _thread.exit()


# Main loop on core0

q_data = queue.Queue()

core0ends = False
core1ends = False

core0_buffer = None

time.sleep(0.25)

#print(f"random: {random.randint(1,10)}")
_thread.start_new_thread(core1,(q_data,))
start_total_time = time.ticks_ms()

print("core0: start sampling")


time.sleep(0.25)

for row in range(ROWS):
    start_loop_time = time.ticks_ms()
        
    data_line = [random.randint(0,255000) for _ in range(COLUMNS)]
    time.sleep_ms(SENSOR_DELAY)

    # Add timing data and write to queue
    data_line.insert(0,time.ticks_diff(time.ticks_ms(), start_loop_time))
    data_line.insert(0,row)
    q_data.put(data_line)

core0ends = True

time.sleep_ms(20)    
#print("core0: start waiting")

while not core1ends:
    time.sleep_ms(25)

total_time = time.ticks_diff(time.ticks_ms(), start_total_time)
print(f"Total time (ms) {total_time}")
time.sleep_ms(250)
print("core0: done waiting")
#print(core0_q_buffer)
#print(core0_buffer)

fp.close()


 