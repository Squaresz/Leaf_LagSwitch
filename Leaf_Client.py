import time
import os
import signal
import random
import threading
import atexit
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode

class Autoclicker:
    def __init__(self):
        self.min_cps = 8.0  # Default minimum clicks per second
        self.max_cps = 13.0  # Default maximum clicks per second
        self.randomize = True  # Default randomize setting
        self.random_level = 0.06  # Default random level
        self.advanced_random = True  # Default advanced random setting
        self.running = False
        self.click_thread = None
        self.keybind = KeyCode(char='`')  # Default keybind is backtick (`)
        self.anti_aliasing = False
        self.aa_interval = 0.05

    def set_cps(self, min_cps, max_cps):
        self.min_cps = min_cps
        self.max_cps = max_cps

    def set_keybind(self, key):
        self.keybind = key

    def set_randomize(self, randomize):
        self.randomize = randomize

    def set_random_level(self, level):
        self.random_level = level

    def set_advanced_random(self, advanced_random):
        self.advanced_random = advanced_random

    def click_loop(self):
        while self.running:
            mouse.click(Button.left)
            if self.randomize:
                if self.advanced_random:
                    sleep_duration = random.uniform(1 / self.max_cps, 1 / self.min_cps)
                    sleep_duration += random.uniform(-self.random_level, self.random_level)
                    sleep_duration = max(sleep_duration, self.aa_interval)
                else:
                    sleep_duration = random.uniform(1 / self.max_cps, 1 / self.min_cps)
            else:
                sleep_duration = random.uniform(1 / self.max_cps, 1 / self.min_cps)
            time.sleep(sleep_duration)

    def on_press(self, key):
        if key == self.keybind:
            if self.running:
                self.stop_clicking()
            else:
                self.start_clicking()

    def on_release(self, key):
        pass

    def start_listener(self):
        with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

    def start_clicking(self):
        if not self.running:
            self.running = True
            self.click_thread = threading.Thread(target=self.click_loop)
            self.click_thread.start()

    def stop_clicking(self):
        self.running = False
        if self.click_thread:
            self.click_thread.join()

    def on_close(self):
        autoclicker.stop_clicking()
        os.kill(os.getpid(), signal.SIGTERM)

    def reload(self):
        os.system('cls')
        print("Leaf Client | Version 2.0")
        print("Press (`) to toggle the auto clicker.")
        print(f"Type 'mincps' to change the min clicks per second. Currently: {self.min_cps}")
        print(f"Type 'maxcps' to change the max clicks per second. Currently: {self.max_cps}")
        print(f"Type 'random' enable randomization. {'Enabled' if self.randomize else 'Disabled'}")
        print(f"Type 'extrarandom' to toggle extra randomization. {'Enabled' if self.advanced_random else 'Disabled'}")
        print(f"Type 'randomlevel' to change the random level.  Currently: {self.random_level}")
        print(f"Type 'bind' to change the keybind. Currently: {self.keybind}")
        print("Type 'exit' to quit the application.")

if __name__ == "__main__":
    autoclicker = Autoclicker()
    mouse = Controller()

    print("Leaf Client | Version 2.0")
    time.sleep(1)
    autoclicker.reload()

    listener_thread = threading.Thread(target=autoclicker.start_listener)
    listener_thread.start()

    atexit.register(autoclicker.on_close)

    while True:
        command = input()
        if command.lower() == 'mincps':
            autoclicker.reload()
            min_cps = float(input("Enter the new minimum clicks per second: "))
            if min_cps > 0:
                autoclicker.set_cps(min_cps, autoclicker.max_cps)
                autoclicker.reload()
                print(f"Minimum clicks per second set to {min_cps}.")
            else:
                print("Invalid input. Minimum clicks per second must be a positive value.")
        elif command.lower() == 'maxcps':
            autoclicker.reload()
            max_cps = float(input("Enter the new maximum clicks per second: "))
            if max_cps > 0:
                autoclicker.set_cps(autoclicker.min_cps, max_cps)
                autoclicker.reload()
                print(f"Maximum clicks per second set to {max_cps}.")
            else:
                print("Invalid input. Maximum clicks per second must be a positive value.")
        elif command.lower() == 'random':
            autoclicker.reload()
            randomize = not autoclicker.randomize
            autoclicker.set_randomize(randomize)
            autoclicker.reload()
            print(f"Randomize {'enabled' if randomize else 'disabled'}.")
        elif command.lower() == 'extrarandom':
            if not autoclicker.randomize:
                print("Error: You must enable randomization before enabling extra randomization.")
            else:
                autoclicker.reload()
                advanced_random = not autoclicker.advanced_random
                autoclicker.set_advanced_random(advanced_random)
                autoclicker.reload()
                print(f"Extra randomization {'enabled' if advanced_random else 'disabled'}.")
        elif command.lower() == 'randomlevel':
            autoclicker.reload()
            level = float(input("Enter the new random level (between 0 and 0.1): "))
            if 0 <= level <= 0.1:
                autoclicker.set_random_level(level)
                autoclicker.reload()
                print(f"Random level set to {level}.")
            else:
                print("Invalid input. Random level must be between 0 and 0.1.")
        elif command.lower() == 'bind':
            autoclicker.reload()
            key = input("Enter the new keybind (e.g., a, 1, `): ")
            autoclicker.set_keybind(KeyCode.from_char(key))
            autoclicker.reload()
            print(f"Keybind set to {key}.")
        elif command.lower() == 'exit':
            os.system('cls')
            print('Leaf Client | Version 1.1')
            time.sleep(0.5)
            print('bye')
            time.sleep(0.5)
            autoclicker.stop_clicking()
            os.kill(os.getpid(), signal.SIGTERM)
            break
        else:
            autoclicker.reload()
            print("Invalid command. Type 'mincps', 'maxcps', 'random', 'extrarandom', 'randomlevel', 'bind', or 'exit'.")