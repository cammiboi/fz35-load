from serial import Serial
from time import sleep

# wait for new bytes to arrive
# wait until its success for fail
# return result


class FZ35():
    def __init__(self, serial_port: str):
        # open serial port for load and set receieve timeout to 1.5 sec
        self.ser = Serial(port=serial_port, timeout=1.5)
        # tell load to send its measurement every second
        self.send_command("start")

    def send_command(self, command: str):
        print("send command: {}".format(command))
        self.ser.write(command.encode('utf-8'))
        result = self.check_success()
        if result:
            print("command success")
        else:
            print("command fail")
        return result

    def format_number(self, number: float, num_dig_before: int, num_dig_after: int):
        fmt = "0{}.{}f".format(
            num_dig_before + num_dig_after + 1, num_dig_after)
        return format(number, fmt)

    def get_reply(self):
        reply = self.ser.read_until(b'\r\n')
        reply = reply.decode("utf-8")
        reply = reply.replace('\r\n', "")
        return reply

    def check_success(self):
        for i in range(0,5):
            reply = self.get_reply()
            if reply == "sucess":
                return True
            elif reply == "success":
                return True
            elif reply == "fail":
                return False
            elif reply == "":
                return False
    
    def get_measurement(self):
        reply = self.get_reply()
        return reply

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
    load.set_current(0.05)
    load.set_current(0.03)
    load.set_current(0.0)
    load.send_command("dhhdhdff")
    sleep(1)
    load.turn_off()
    sleep(1)
    load.turn_on()
    print(load.get_measurement())
