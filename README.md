# Android Pattern Lockscreen Bruteforce

This script bruteforces the *pattern* lockscreen on an Android device by emulating mouse inputs through a Raspberry Pi Zero OTG.<br /><br />
<pre align="center">
  +-----+            +--+  OTG   +-----+
  |     |            |  |        |     |
  |     |   -------> |Pi| -----> |phone|
+-+-----+-+          |  |        |     |
|   PC    |          |  |        |     |
+---------+          +--+        +-----+
</pre>

Please note that it may *not* be effective on modern Android devices due to increased lockscreen timeouts.

**Requirements:**
- Raspberry Pi Zero.<br />
or<br />
- Raspberry Pi 4 running Raspbian with a kernel version > 6.1

## Step 0: Configure Your Raspberry Pi
- Install your preferred operating system; I recommend using full Raspbian.
- Set up and configure SSH so you can access the Raspberry Pi when connecting your device to the USB port.

## Step 1: Install zero_hid on Your Raspberry Pi
- Follow the installation instructions at [zero_hid GitHub repository](https://github.com/thewh1teagle/zero-hid).

## Step 2: Configure
- Adjust values in the POINTS list to match the specific layout of your device:<br />
  Example: `POINTS = [(0,0),(60, 50), (120, 50), (180, 50), (60, 100), (120, 100), (180, 100), (60, 150), (120, 150), (180, 150)]`<br />
  (Values matching the grid on a Sony Z1)

## Step 3: Configure the List of Patterns
- Create a list of patterns to use for bruteforcing; for example, you can use a repository like [AndroidPatternLock by delight-im](https://github.com/delight-im/AndroidPatternLock).<br />
- Each line of the file should contain the points to test, e.g., "12369".

## Step 4: Run the Script
- SSH into your Raspberry Pi.
- Connect your device to the Raspberry Pi.
- Run the script, for example: `python3 hid_bruteforce.py patternfile.txt`

## How It Works
- The script first moves to the coordinates of the first point.
- Simulates a left click.
- Moves the cursor according to the specified points.
- Upon reaching the last point, releases the left click, and the mouse cursor moves to the top-left corner of the screen.
- After five attempts, the script times out based on MAX_ATTEMPTS_TIMEOUT.

**Note:** The script is simplistic; it does not include checks to determine if the device was successfully unlocked.
