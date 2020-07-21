import time
import serial

class GrblComms:
    def __init__(self, port: str) -> None:
        # This ought to either look at the usb tree, or trigger a re-enumeration
        # and watch dmesg... for now, require hardcoding the port.
        self.port = port
        self.serial = serial.Serial(self.port, timeout=0.1, xonxoff=1, baudrate=115200)

    def communicate(self, line: str) -> None:
        print("dump")
        while self.chat(b''):
            pass

        # Restore "defaults" for the build
        print("reset settings")
        self.chat(b"\n$RST=$\n")
        self.wait_for_idle(alarm_ok=True)

        print("ctrl-x")
        self.chat(b"\x18")  # Ctrl-X to reset
        self.wait_for_idle(alarm_ok=True)

        print("unlock")
        self.chat(b"$X\n")
        self.wait_for_idle()

        self.chat(b"$$\n")

        print("write")
        self.chat(line)  # can be multiple lines

        print("waiting")
        self.wait_for_idle()

    def configure(
        self, x_steps_per_mm=400, x_axis_max_feed=1000, x_axis_accel=45,
        max_jerk=0.5
    ):
        return f"$100={x_steps_per_mm}\n$110={x_axis_max_feed}\n$120={x_axis_accel}\n".encode()

    def chat(self, data):
        print(">>", data)
        self.serial.write(data)
        self.serial.flush()
        tmp = self.serial.read(1024)
        print("<<", tmp)
        return tmp

    def wait_for_idle(self, alarm_ok=False):
        # TODO: check timeout instead
        for i in range(100):
            data = self.chat(b"?\n")
            if data.startswith(b"ok\r\n"):
                data = data[len(b"ok\r\n"):]
            if data.startswith(b"<Idle"):
                break
            elif alarm_ok and data.startswith(b"<Alarm"):
                break
        else:
            raise Exception("Timeout")
