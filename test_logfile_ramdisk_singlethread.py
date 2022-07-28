import machine
import os
import time
import random
import ramdisk_lib

class RAMBlockDev:
    def __init__(self, block_size, num_blocks):
        self.block_size = block_size
        self.data = bytearray(block_size * num_blocks)

    def readblocks(self, block_num, buf, offset=0):
        addr = block_num * self.block_size + offset
        for i in range(len(buf)):
            buf[i] = self.data[addr + i]

    def writeblocks(self, block_num, buf, offset=None):
        if offset is None:
            # do erase, then write
            for i in range(len(buf) // self.block_size):
                self.ioctl(6, block_num + i)
            offset = 0
        addr = block_num * self.block_size + offset
        for i in range(len(buf)):
            self.data[addr + i] = buf[i]

    def ioctl(self, op, arg):
        if op == 4: # block count
            return len(self.data) // self.block_size
        if op == 5: # block size
            return self.block_size
        if op == 6: # block erase
            return 0

ROWS = const(500)				# Number of sample cycles
COLUMNS = const(50)				# Number of data values generated each sample cycle
SENSOR_DELAY = const(10)		# Sample period. The delay each sampling loop introduces

bdev = RAMBlockDev(512, 1024)
os.VfsLfs2.mkfs(bdev)
os.mount(bdev, '/ramdisk')

data_matrix = []
fp = open('/ramdisk/test_data.txt','w')

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
print(f"Tiempo total (ms) {time.ticks_diff(time.ticks_ms(), start_total_time)}")