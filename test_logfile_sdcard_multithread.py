import machine
from machine import SPI, SoftSPI, Pin
import os
import time
import random
import _thread
import queue
import gc
import sdcard

#core0: read queue and write file
#core1: read sensor and write queue

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

def core1(q_data):
    
    global core1ends
    time.sleep(0.25)

    for row in range(ROWS):
        start_loop_time = time.ticks_ms()
        
        data_line = [random.randint(0,255000) for _ in range(COLUMNS)]
        time.sleep_ms(SENSOR_DELAY)

        # Add timing data and write to queue
        data_line.insert(0,time.ticks_diff(time.ticks_ms(), start_loop_time))
        data_line.insert(0,row)
        q_data.put(data_line)

    
    time.sleep_ms(20)    
    core1ends = True
    _thread.exit()

# Main loop on core0

q_data = queue.Queue()

core1ends = False
#core0_q_buffer = []
core0_buffer = None

time.sleep(0.25)

print(f"random: {random.randint(1,10)}")
_thread.start_new_thread(core1,(q_data,))
start_total_time = time.ticks_ms()

i = 0
fp = open('/sd/test_data.txt','w')
print("core0: start waiting")
while not core1ends or not q_data.empty():
    if not q_data.empty():
        #core0_q_buffer.append(q_data.get())
        core0_buffer = q_data.get()
        fp.write(str(core0_buffer)+'\n')
        #print((core0_buffer[0],core0_buffer[1],gc.mem_free()))
        print(core0_buffer[1],q_data.qsize())
        #print((core0_buffer[1],q_data.qsize()/10,gc.mem_free()/1024/10))
        #print(core0_buffer[1])
    if i % GC_FREQ == 0:
        gc.collect()
    i += 1
    time.sleep_ms(CORE0_DELAY)

total_time = time.ticks_diff(time.ticks_ms(), start_total_time)
print(f"Total time (ms) {total_time}")
time.sleep_ms(250)
print("core0: done waiting")
#print(core0_q_buffer)
print(core0_buffer)

fp.close()