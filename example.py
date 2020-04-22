from fz35 import FZ35
from time import sleep

load = FZ35("COM8")
load.turn_off()
load.set_current(1)
load.turn_on()
sleep(1)

while 1:
    print(load.get_measurement())
    sleep(1)
