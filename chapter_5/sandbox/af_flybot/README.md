# Flybot Simulation

A study in physics simulation and animation for Chapter 5 of How to Train Your Robot ([tyr.fyi](https://tyr.fyi)).

## Install and run

First get your dependencies lined up.

1. Make sure you have Python installed
2. Install `matplotlib`
3. Install [`httyr-tools`](https://github.com/brohrer/httyr-tools)

Then at the command line

```bash
git clone https://github.com/brohrer/how-to-train-your-robot.git
cd how-to-train-your-robot/chapter_5/sandbox/af_flybot/
python3 run.py
```

### For MacOS

I've tested this on Ubuntu and MacOS. To get it running on current versions of MacOS you may have to override an
environment variable. You can do this at the command line with

```bash
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
```

Alternatively you can add

```bash
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
```

to the end of your `.bashrc` file and typing

```bash
source ~/.bashrc
```

at the command line.


## Modify

Edit [config.py](https://github.com/brohrer/how-to-train-your-robot/blob/main/chapter_5/sandbox/af_flybot/config.py)
to generate variations on the simulation.

Feel free to re-share your variants on social media.
