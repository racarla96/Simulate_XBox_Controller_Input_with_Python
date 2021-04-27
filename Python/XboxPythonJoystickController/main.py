import keyboard  # using module keyboard
import pyvjoy
import time

def waiting():
    while True:  # making a loop
        j = pyvjoy.VJoyDevice(1)
        print(keyboard.read_key())
        try:  # used try so that if user pressed other than the given key error will not be shown
            if keyboard.is_pressed('q'):  # if key 'q' is pressed
                print('You Pressed A Key!')
                break  # finishing the loop
            if keyboard.is_pressed('a'):  # if key 'q' is pressed
                j.set_button(1, 1)
                time.sleep(0.1)
                j.set_button(1, 0)
        except:
            break  # if user pressed a key other than the given key the loop will break



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    waiting()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
