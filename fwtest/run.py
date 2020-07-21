from pathlib import Path
import glob
import tomlkit
import sys

from fwtest.comms.grbl_comms import GrblComms
from fwtest.comms.g2_comms import G2Comms
from fwtest.comms.smoothie_comms import SmoothieComms

COMMS = {
    "g2": G2Comms,
    "grbl": GrblComms,
    "smoothie": SmoothieComms,
}

def main(firmware_key, run_id, test):
    # TODO figure out how to store a hash in all uploaded firmware so we can
    # fail if it's out of date.

    test_matrix = tomlkit.parse(Path("test-matrix.toml").read_text())
    tbl = test_matrix["fw"][firmware_key]
    ports = glob.glob(f"/dev/serial/by-id/*{tbl['usb_match']}*")
    if len(ports) != 1:
        print("Could not find exactly one port")
        print(ports)
        return 1

    c = COMMS[tbl["comms"]](ports[0])

    if test.startswith("fwtest/tests/"):
        test = test[len("fwtest/tests/"):-3]
    test_import_name = f"fwtest.tests.{test}"
    __import__(test_import_name)
    t = sys.modules[test_import_name].StateTest(test, f"{firmware_key}-{run_id}")
    t.run(c)

if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
