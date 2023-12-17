# Android-Pattern-Bruteforce
Bruteforce the pattern lockscreen on a Android device emulating mouse inputs via RPI Zero OTG.<br />
Should *not* work on modern Android due to lockscreen timemouts increasing.

Requirements: RPi Zero, or RPi 4 running Raspian, kernel > 6.1

## Step 0) Configure you RPi
- Install your os, i'm running full Raspian.
- Setup and configure SSH so you can access the RPi when you connect your device to the USB-port.
  
## Step 1) Install zero_hid on your RPi
- installation -> https://github.com/thewh1teagle/zero-hid

## Step 2) Configure
- Change values in POINTS to match your specific device:<br />
  Ex: POINTS = [(60, 50), (120, 50), (180, 50), (60, 100), (120, 100), (180, 100), (60, 150), (120, 150), (180, 150)]<br />
  (Values matching the grid on a Sony Z1)

## Step 3) Configure list of patterns
- Create a list of patterns to use when bruteforcing, ex: https://github.com/delight-im/AndroidPatternLock<br />
- Each line of the file should contain what points to test, eg: "12369"

## Step 4) Run script
- SSH into your RPi
- Connect the device to you RPi.
- Run Script, eg: python3 hid_bruteforce.py patternfile.txt

## How it works
- The script will first move to the coordinates of the first point.
- A left click is simulated.
- The script then moves the cursor according to the points that are specified.
- When the last point is reached, left click is released, and the mousecursor moves to the top left corner of the screen.
- After five attempts the script times out according to MAX_ATTEMPTS_TIMEOUT

- The script is *dumb*, there are NO checks to see if the device was unlocked.
