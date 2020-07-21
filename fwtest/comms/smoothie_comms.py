# http://smoothieware.org/supported-g-codes

# M114 (goal) vs M114.1 (actual) but different coordinates
# ok C: X:0.0000 Y:0.0000 Z:0.0000
# ok WCS: X:0.0000 Y:0.0000 Z:0.0000

# M92 sets steps per mm
# M204 S<accel>
# M205 X<junction deviation> S<planner speed?>

# G92 during a move zeros to the goal, not actual

# "?" response "<Idle|MPos:0.0000,0.0000,0.0000|WPos:0.0000,0.0000,0.0000|F:4000.0,100.0>"
# but does not send \r with \n

# "help" and "reset" 

from .grbl_comms import GrblComms

class SmoothieComms(GrblComms):
    def communicate(self, line: str) -> None:
        self.chat(line)
        self.wait_for_idle()

    def configure(
        self, x_steps_per_mm=400, x_axis_max_feed=1000, x_axis_accel=45,
        max_jerk=0.05
    ):
        # No tests currently actually test max_jerk, that's a big TODO
        return f"M92 X{x_steps_per_mm}\nM203 X{x_axis_max_feed}\nM204 S{x_axis_accel}\nM205 X{max_jerk}\n".encode()

