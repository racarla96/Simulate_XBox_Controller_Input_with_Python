from pynput import keyboard as Keyboard
import pyvjoy
import time
import logging, sys

# General Variable
global joy, exit_flag
joy = pyvjoy.VJoyDevice(1)
exit_flag = False # end the program

# Constant values
## Vjoy Gamepad
### Button state
PRESS = 1
RELEASE = 0
### Axis values
MIN_JOY = 0
MID_JOY = 16384
MAX_JOY = 32767

# Map keys (Hash table)
# Xbox Gamepad      - Vjoy Gamepad       - Windows Map - Keyboard Key
# (R) Stick Axis X  - pyvjoy.HID_USAGE_X - Axis 1      -
# (R) Stick Axis X  - pyvjoy.HID_USAGE_X - Axis 1      -
# (R) Stick Axis Y  - pyvjoy.HID_USAGE_Y - Axis 2      -
# (R) Stick Axis Y  - pyvjoy.HID_USAGE_Y - Axis 2      -
# (L) Stick Axis X  - pyvjoy.HID_USAGE_RX - Axis 4     - Right
# (L) Stick Axis X  - pyvjoy.HID_USAGE_RX - Axis 4     - Left
# (L) Stick Axis Y  - pyvjoy.HID_USAGE_RY - Axis 5     - Up
# (L) Stick Axis Y  - pyvjoy.HID_USAGE_RY - Axis 5     - Down

# Button Y          - Button 4                         - W
# Button X          - Button 3                         - A
# Button A          - Button 1                         - S
# Button B          - Button 2                         - D
# Bumper (RB)       - Button 5                         - E
# Bumper (LB)       - Button 6                         - Q
# Back              - Button 7                         - B
# Start             - Button 8                         - T
# Guide             - Button 9                         - G
# (R) Stick Button  - Button 11                        - O
# (L) Stick Button  - Button 12                        - p

key_but_map = {
    'w': 4,
    'a': 3,
    's': 1,
    'd': 2,
    'e': 5,
    'q': 6,
    'b': 7,
    't': 8,
    'g': 9,
    'o': 11,
    'p': 12
}

def on_press(key):
    global exit_flag

    logging.debug('special key {0} pressed'.format(key))

    # Stick Axis X
    if key == Keyboard.Key.right:
        joy.set_axis(pyvjoy.HID_USAGE_RX, MAX_JOY)
    elif key == Keyboard.Key.left:
        joy.set_axis(pyvjoy.HID_USAGE_RX, MIN_JOY)

    # Stick Axis Y
    if key == Keyboard.Key.up:
        joy.set_axis(pyvjoy.HID_USAGE_RY, MAX_JOY)
    elif key == Keyboard.Key.down:
        joy.set_axis(pyvjoy.HID_USAGE_RY, MIN_JOY)

    if hasattr(key, 'char') and key.char:
        if key.char.lower() in key_but_map: # Contains
            joy.set_button(key_but_map[key.char.lower()], PRESS)

    # Exit program
    if key == Keyboard.Key.esc:
        logging.debug("Finishing the program!")
        exit_flag = True

def on_release(key):
    logging.debug('special key {0} pressed'.format(key))

    # Stick Axis X
    if key == Keyboard.Key.left or key == Keyboard.Key.right:
        joy.set_axis(pyvjoy.HID_USAGE_RX, MID_JOY)

    # Stick Axis Y
    if key == Keyboard.Key.up or key == Keyboard.Key.down:
        joy.set_axis(pyvjoy.HID_USAGE_RY, MID_JOY)

    if hasattr(key, 'char') and key.char:
        if key.char.lower() in key_but_map: # Contains
            joy.set_button(key_but_map[key.char.lower()], RELEASE)

def clear_joy():
    for i in range(12):
        joy.set_button(i+1, 0)
    joy.set_axis(pyvjoy.HID_USAGE_X,  MID_JOY)
    joy.set_axis(pyvjoy.HID_USAGE_Y,  MID_JOY)
    joy.set_axis(pyvjoy.HID_USAGE_Z,  MID_JOY)
    joy.set_axis(pyvjoy.HID_USAGE_RX, MID_JOY)
    joy.set_axis(pyvjoy.HID_USAGE_RY, MID_JOY)

# General
if __name__ == '__main__':

    logging.basicConfig(stream=sys.stderr, level=logging.INFO)
#    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    logging.debug("Clear joystick")
    clear_joy()

    listener = Keyboard.Listener(
        on_press=on_press,
        on_release=on_release)
    listener.start()

    while not exit_flag:
        time.sleep(0.01)