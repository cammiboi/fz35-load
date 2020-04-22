from serial import Serial


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
        for i in range(0, 5):
            reply = self.get_reply()
            if reply == "sucess":
                return True
            elif reply == "success":
                return True
            elif reply == "fail":
                return False
            elif reply == "":
                return False

    def parse_measurements(self, measurement: str):
        try:
            nums = measurement.split(',')
            print(nums)
            if len(nums) != 4:
                return False
            v = float(nums[0].replace('V', ''))
            a = float(nums[1].replace('A', ''))
            ah = float(nums[2].replace('Ah', ''))
            h, m = nums[3].split(':')
            t = (int(h) * 60) + int(m)
            return a, v, ah, t
        except (ValueError):
            return False

    def get_measurement(self):
        reply = self.get_reply()
        return self.parse_measurements(reply)

    def turn_on(self):
        self.send_command("on")

    def turn_off(self):
        self.send_command("off")

    def set_current(self, current: float):
        num = self.format_number(current, 1, 2)
        cmd = "{}A".format(num)
        self.send_command(cmd)
