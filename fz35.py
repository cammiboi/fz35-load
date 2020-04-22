from serial import Serial
from time import sleep

class FZ35():
    def __init__(self, serial_port: str):
        self.ser = Serial(serial_port)
        self.send_command("start") # tell load to send its measurement every second

    def send_command(self, command: str):
        print("send command: {}".format(command))
        self.ser.write(command.encode('utf-8'))

    def format_number(self, number: float, num_dig_before: int, num_dig_after: int):
        fmt = "0{}.{}f".format(
            num_dig_before + num_dig_after + 1, num_dig_after)
        return format(number, fmt)

    def turn_on(self):
        self.send_command("on")

    def turn_off(self):
        self.send_command("off")

    def set_current(self, current: float):
        num = self.format_number(current, 1, 2)
        cmd = "{}A".format(num)
        self.send_command(cmd)

if __name__ == '__main__':

    # example script to control load
    load = FZ35("COM8")
    sleep(1)
    load.set_current(3)
    sleep(3)
    load.set_current(0.06)
    sleep(1)
    load.turn_off()
    sleep(1)
    load.turn_on()