import sys

import matplotlib.pyplot as plt

def main(filename):
    samplerate = 4000000.0
    samples_per_khz = samplerate / 1000

    with open(filename, "rb") as f:
        idx = 0
        last_fall_idx = -1
        prev_sample = 0xff
        velocity = []
        acceleration = []
        time_keys = []
        n = 0
        while True:
            buf = f.read(4096)
            if not buf:
                break
            for c in buf:
                # active-high
                if (c & 2) != 0 and (prev_sample & 2) == 0:
                    n += 1
                    if last_fall_idx != -1:
                        time_keys.append(idx / samplerate)
                        ds = idx - last_fall_idx
                        khz = samples_per_khz / ds  #samplerate / float(ds) / 1000

                        if not velocity:
                            acceleration.append(1)
                        else:
                            t = khz / velocity[-1]
                            if t < 1:
                                t = 1 / t
                            acceleration.append(t)

                        velocity.append(khz)
                        #print(idx / samplerate, khz)
                    last_fall_idx = idx
                elif c != prev_sample:
                    #print(hex(c ^ prev_sample))
                    pass
                prev_sample = c
                idx += 1

    fig, ax1 = plt.subplots(figsize=(20, 6))
    ax1.set_xlabel("time (sample)")
    ax1.set_ylabel("step rate (khz)", color="red")
    ax1.tick_params(axis="y", labelcolor="red")
    ax1.plot(time_keys, velocity, color="red")

    ax2 = ax1.twinx()
    ax2.set_ylabel("abs(ratio of change)", color="blue")
    ax2.tick_params(axis="y", labelcolor="blue")
    ax2.set_ylim(bottom=1, top=4)
    ax2.plot(time_keys, acceleration, color="blue")

    fig.tight_layout()
    plt.savefig(filename + ".svg")

    print(n, "steps")

if __name__ == "__main__":
    for f in sys.argv[1:]:
        main(f)
