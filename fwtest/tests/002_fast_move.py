from .base import Base

class StateTest(Base):

    capture_time = 3

    def get_gcode(self, comm):
        return (
            comm.configure(
                x_steps_per_mm=400,
                x_axis_max_feed=12000,
                x_axis_accel=45,
            ) +
            b"G92 X0\n"  # set WCO so we're at zero, in case a previous test moved
            b"G1 X100 F12000\n"
        )

    def analyze(self, capture_filename, samplerate):
        print(capture_filename)
        transitions = 0
        value = None
        with open(capture_filename, 'rb') as f:
            while True:
                buf = f.read(4096)
                if not buf:
                    break

                for c in buf:
                    if value is None:
                        value = c
                    elif value != c:
                        transitions += 1
                        value = c
        print(f"{transitions} transitions")
        return transitions == 80000

