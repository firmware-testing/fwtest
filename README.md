# Firmware Tests

This repo contains some acceptance tests intended for evaluating 3D printer and
CNC controllers' firmware.

## Hardware

Because this does not intend to evaluate drivers, current, or anything else
except motion planning and step timing, you don't need much.

* grblHAL: Blue Pill
* G2: Arduino Due
* Smoothie: any smoothieboard or mbed

Plus

* An inexpensive USB logic analyzer based on fx2lalw

## Connection

```
Board under test          Logic Analyzer
----------------          --------------
           X Dir    ->    CH1
          X Step    ->    CH2
             GND    ->    GND
```

You can have multiple boards plugged in simultaneously, and it will pick the
correct one for your firmware, but the logic analyzer connections need to be
moved around manually.


## Current tests

(Needs some curating)

* 001: Short move (4 KHz)
* 002: Fast move (80 KHz)


## Running


```
$ ./runall.sh

or

$ python -m fwtest.run <firmware> <run id> <test name>
```

## Debugging

* Viewing captures

  ```
  $ pulseview -I binary:samplerate=4m /path/to/logic.bin
  ```

  Then add decoder (last toolbar button), Timing, click left side, choose D1, (rising or falling)

* Interacting with serial ports

  (this doesn't require consistent `\r\n` endings like `screen` does)

  ```
  $ python -m fwtest.pychat /path/to/port
  ```

* Graphing

  ```
  $ python -m fwtest.plot_accel /path/to/logic.bin [...]
  ```

  writes the corresponding `/path/to/logic.bin.svg`
