from pynput import keyboard
import time
import subprocess


def lock_windows():
    try:
        subprocess.run("rundll32.exe user32.dll,LockWorkStation", shell=True)
    except Exception as e:
        print(f"Error: {e}")


class SystemLockdown:
    def __init__(self):
        self.isLocked = True

    def initiate(self, key):
        if self.isLocked:
            self.isLocked = False
            lock_windows()
            time.sleep(5)
            self.isLocked = True

    def on_key_press(self):
        try:
            with keyboard.Listener(on_release=self.initiate()) as key_listener:
                key_listener.join()
        except Exception as e:
            print(f"Error in main: {e}")

# SystemLockdown.on_key_press()
