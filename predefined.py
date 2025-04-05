import time
import subprocess
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
import pynput
from typing import Optional


def lock_windows():
    try:
        subprocess.run('rundll32.exe user32.dll,LockWorkStation', shell=True)
    except Exception as e:
        print(f'Error: {e}')


class Predefined:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument(r'user-data-dir=C:\Users\aadit\AppData\Local\Google\Chrome\User Data')
        options.add_experimental_option('detach', True)
        self.driver = None
        self.options = options
        self.isLocked = False
        self.count = 0
        self.key_listener: Optional[pynput.keyboard.Listener] = None

    def _get_driver(self):
        if self.driver is None:
            self.driver = webdriver.Chrome(options=self.options)
        return self.driver

    def search(self, w, precise=False):
        driver = self._get_driver()
        if self.count > 0:
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[-1])
        driver.get(f"https://www.google.com/search?q={w}")
        self.count += 1
        if precise:
            link = driver.find_element(By.CSS_SELECTOR, 'a[jsname="UWckNb"]')
            link.click()

    @staticmethod
    def open_app(app_name):
        pyautogui.press("win")
        time.sleep(0.5)
        pyautogui.write(app_name)
        time.sleep(0.5)
        pyautogui.press("enter")

    def initiate_lock(self):
        if self.isLocked:
            self.isLocked = True
            lock_windows()
            time.sleep(5)
            self.isLocked = False

    def instaLock(self, key):
        self.initiate_lock()

    def arm_system(self):
        if self.key_listener is not None and self.key_listener.is_alive():
            print("Keyboard listener is already running")
            return

        try:
            self.key_listener = pynput.keyboard.Listener(on_release=self.on_key_press)
            self.key_listener.start()
            print("Keyboard listener started")
        except Exception as e:
            print(f'Error starting keyboard listener: {e}')

    def disarm_system(self):
        if self.key_listener is not None and self.key_listener.is_alive():
            self.key_listener.stop()
            print("Keyboard listener stopped")
        else:
            print("No active keyboard listener to stop")


class SystemLockdown:
    def __init__(self):
        self.isLocked = True

    def on_key_press(self):
        try:
            with pynput.keyboard.Listener(on_release=self.initiate()) as key_listener:
                key_listener.join()
        except Exception as e:
            print(f'Error in main: {e}')
