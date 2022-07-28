import time, _thread, machine, queue, random

def core1(q_data):
    global core1ends
    print("core1 starting")
    for i in range(10):
        q_data.put(i)
        time.sleep_ms(random.randint(500,2000))
    print("core1 done")
    core1ends = True
    return
    
core1ends = False
q_data = queue.Queue()
_thread.start_new_thread(core1,(q_data,))

while not core1ends:
    if not q_data.empty():
        print(f"core0 received {q_data.get()}")
    time.sleep_ms(10)

time.sleep_ms(10)
print("core0 done")



