import time
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By


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
        self.isLocked = True
        self.count = 0

    def _get_driver(self):
        if self.driver is None:
            self.driver = webdriver.Chrome(options=self.options)
        return self.driver

    def search(self, w, precise=False):
        driver = self._get_driver()
        if self.count > 0:
            driver.execute_script('window.open('');')
            driver.switch_to.window(driver.window_handles[-1])
        driver.get(f"https://www.google.com/search?q={w}")
        self.count += 1
        if precise:
            link = driver.find_element(By.CSS_SELECTOR, 'a[jsname="UWckNb"]')
            link.click()

    def initiate_lock(self):
        if self.isLocked:
            self.isLocked = False
            lock_windows()
            time.sleep(5)
            self.isLocked = True

# from pynput import keyboard

# class SystemLockdown:
#     def __init__(self):
#         self.isLocked = True
#

#
#     def on_key_press(self):
#         try:
#             with keyboard.Listener(on_release=self.initiate()) as key_listener:
#                 key_listener.join()
#         except Exception as e:
#             print(f'Error in main: {e}')

# SystemLockdown.on_key_press()
