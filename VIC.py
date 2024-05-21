from pynput import keyboard
import time
import subprocess

bool = True

def lock_windows():
    try:
        subprocess.run("rundll32.exe user32.dll,LockWorkStation", shell=True)
    except Exception as e:
        print(f"Error: {e}")

def on_key_release(key):
    global bool
    try:
        if bool:
            bool = False
            lock_windows()
            time.sleep(5)
            bool = True
    except Exception as e:
        print(f"Error: {e}")

def main():
    try:
        with keyboard.Listener(on_release=on_key_release) as key_listener:
            key_listener.join()
    except Exception as e:
        print(f"Error in main: {e}")

if __name__ == "__main__":
    
    main()

