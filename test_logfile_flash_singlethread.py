import machine
import os
import time
import random

ROWS = const(500)				# Number of sample cycles
COLUMNS = const(50)				# Number of data values generated each sample cycle
SENSOR_DELAY = const(10)		# Sample period. The delay each sampling loop introduces

data_matrix = []
fp = open('test_data.txt','w')

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