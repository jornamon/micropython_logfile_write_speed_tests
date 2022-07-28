import time, _thread, machine

def task(n, delay):
    led = machine.Pin(25, machine.Pin.OUT)
    print(f"Inside: {_thread.get_ident()}\n")
    for i in range(n):
        led.high()
        time.sleep(delay)
        led.low()
        time.sleep(delay)
        print(i)
    print('done')

_thread.start_new_thread(task, (10, 0.3))
print(f"Outside: {_thread.get_ident()}\n")
print("Ouside waiting \n")
time.sleep(10)
print("Outside done waiting")
