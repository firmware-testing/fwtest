import sys
from pathlib import Path
import time
import tempfile
import subprocess

class Base:
    samplerate = 4000000
    capture_time = 2  # seconds

    def __init__(self, test_name, run):
        self.base_path = Path("log", run, test_name)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def run(self, comm):
        to_write = self.get_gcode(comm)
        assert to_write.endswith(b"\n")

        out_bin = str(self.base_path / "logic.bin")

        # TODO check output status
        samples = self.capture_time * self.samplerate
        t0 = time.time()
        sigrok = subprocess.Popen([
            "sigrok-cli", "-d", "fx2lafw", "--config",
            f"samplerate={self.samplerate}",
            "--samples", f"{samples}", "-O", "binary", "-o", out_bin])
        comm.communicate(to_write)

        t1 = time.time()
        p = sigrok.poll()
        if p == 0:
            raise Exception(f"sigrok-cli exited too early; should set capture_time >= {t1-t0}; currently {self.capture_time}")
        elif p is not None:
            raise Exception(f"sigrok-cli exited nonzero: {p}")

        sigrok.wait(self.capture_time)
        if not self.analyze(out_bin, samples):
            print("FAIL")
            sys.exit(1)

        # pulseview -I binary:samplerate=2m /tmp/tmpa9_oi6t9
