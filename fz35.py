from serial import Serial


class FZ35():
    def __init__(self, serial_port: str):
        # open serial port for load and set receieve timeout to 2 sec
        self.ser = Serial(port=serial_port, timeout=2)
        # tell load to send its measurement every second
        self.send_command("start")

    def send_command(self, command: str, check_success: bool = True):
        print("send command: {}".format(command))
        self.ser.write(command.encode('utf-8'))
        if check_success:
            result = self.check_success()
            if result:
                print("command success")
            else:
                print("command fail")
            return result
        return True

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
            v = float(nums[0].replace('V', ''))
            a = float(nums[1].replace('A', ''))
            ah = float(nums[2].replace('Ah', ''))
            h, m = nums[3].split(':')
            t = (int(h) * 60) + int(m)
            return a, v, ah, t
        except (ValueError, IndexError, TypeError):
            return False

    def get_measurement(self):
        for n in range(0, 3):  # retry up to 3 times if getting measurement fails
            reply = self.get_reply()
            meas = self.parse_measurements(reply)
            if meas:
                return meas
        return False

    def turn_on(self):
        self.send_command("on")

    def turn_off(self):
        self.send_command("off")

    def set_current(self, current: float):
        num = self.format_number(current, 1, 2)
        cmd = "{}A".format(num)
        self.send_command(cmd)

    def set_low_voltage_protection(self, voltage: float):
        num = self.format_number(voltage, 2, 1)
        cmd = "LVP:{}".format(num)
        self.send_command(cmd)

    def set_over_voltage_protection(self, voltage: float):
        num = self.format_number(voltage, 2, 1)
        cmd = "OVP:{}".format(num)
        self.send_command(cmd)

    def set_over_current_protection(self, current: float):
        num = self.format_number(current, 1, 2)
        cmd = "OCP:{}".format(num)
        self.send_command(cmd)

    def set_over_power_protection(self, power: float):
        num = self.format_number(power, 2, 2)
        cmd = "OPP:{}".format(num)
        self.send_command(cmd)

    def set_max_ah_protection(self, ah: float):
        num = self.format_number(ah, 1, 3)
        cmd = "OAH:{}".format(num)
        self.send_command(cmd)

    def set_max_time_protection(self, min: int):
        hr = int(min / 60)
        min = min - (hr * 60)
        hr = format(hr, "02.0f")
        min = format(min, "02.0f")
        cmd = "OHP:{}:{}".format(hr, min)
        self.send_command(cmd)

    def get_protection_settings(self):
        self.send_command("read", check_success=False)
        for n in range(0,3):
            reply = self.get_reply()
            if reply.startswith("OVP"):
                print("protection settings: {}".format(reply))
                return reply
        return False