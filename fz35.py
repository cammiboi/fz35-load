import serial


class FZ35():
    def __init__(self, serial_port: str):
        self.ser = serial.Serial(serial_port)

    def send_command(self, command: str):
        print("send command: {}".format(command))
        self.ser.write(command)

    def format_number(self, number: float, num_dig_before: int, num_dig_after: int):
        fmt = "0{}.{}f".format(
            num_dig_before + num_dig_after + 1, num_dig_after)
        return format(number, fmt)

    def turn_on(self):
        self.send_command("on")

    def turn_off(self):
        self.send_command("off")

    def set_current(self, current: float):
        num = format_number(current, 1, 2)
        cmd = "{}A".format(num)
        self.send_command(cmd)
