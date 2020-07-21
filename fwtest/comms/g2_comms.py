import time
import serial

class G2Comms:
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

        self.chat(b"{xam:1,yam:1,zam:1}\n{clear:n}\n")
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
        # TODO: jerk
        # TODO: accel
        # TODO: note feedrate/velocity difference
        return f"{{xfr:{x_axis_max_feed},xvm:{x_axis_max_feed},1su:{x_steps_per_mm}}}\n".encode()

    def chat(self, data):
        print(">>", data)
        self.serial.write(data)
        self.serial.flush()
        tmp = self.serial.read(8192)  # '$$' has much to output
        print("<<", tmp)
        return tmp

    def wait_for_idle(self, alarm_ok=False):
        # TODO: check timeout instead
        # TODO: link to where these constants are defined
        for i in range(100):
            data = self.chat(b"?\n")
            if b'"stat":3' in data or b'"stat":1' in data:
                break
        else:
            raise Exception("Timeout")
