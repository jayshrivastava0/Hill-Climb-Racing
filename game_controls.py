import time
import pyautogui

class Car:
    def __init__(self):
        self.current_key_pressed = None

    # Pressing any key
    def press(self, key: str):
        if self.current_key_pressed != None:
            self.release()
        pyautogui.keyDown(key)
        self.current_key_pressed = key

    def release(self):
        pyautogui.keyUp(self.current_key_pressed)

