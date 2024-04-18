import win32gui, win32ui, win32con
from time import time
import cv2
import numpy as np
from ctypes import windll


class window_capture:
    """
    Use this to print all the available opened windows
    win32gui.EnumWindows( window_capture.opened_windows, None )
    """

    # Prints the name of all the available windows opened.
    @staticmethod
    def opened_windows(hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd):
            print(hex(hwnd), win32gui.GetWindowText(hwnd))

    w = 0
    h = 0
    hwnd = None

    def __init__(self, window_name, **kwargs):
        """
        Initialize the window_capture instance to start the screen recording of any window.

        Parameters:
        - window_name (str): The name of the window.
        - **kwargs: Keyword arguments to specify custom rectangle coordinates.
          Valid keys: 'left', 'top', 'right', 'bottom'.

        If custom rectangle coordinates provided are wrong, then ValueError.

        Example:
        my_instance = window_capture(window_name='YourWindowName', left=100, top=50, right=300, bottom=200)
        """

        # To capture the invisble windows
        windll.user32.SetProcessDPIAware()

        # Handle for the window that we want
        self.hwnd = win32gui.FindWindow(None, window_name)
        if not self.hwnd:
            raise Exception(f"Window Not Found {window_name}.")

        # Window Size
        if not kwargs:
            left, top, right, bottom = win32gui.GetClientRect(self.hwnd)
        else:
            left = kwargs.get("left", None)
            top = kwargs.get("top", None)
            right = kwargs.get("right", None)
            bottom = kwargs.get("bottom", None)

        # checking if all the values are present within the kwargs
        if (
            right is not None
            and left is not None
            and top is not None
            and bottom is not None
        ):
            self.w = right - left
            self.h = bottom - top
        else:
            raise ValueError("Incomplete dimensions provided for the window")


    def get_window_coordinates(self):
        """
        Get the coordinates of the window relative to the screen.

        Returns:
        tuple: Tuple containing the left, top, right, and bottom coordinates of the window.
        """
        # Get the coordinates of the window relative to the screen
        rect = win32gui.GetWindowRect(self.hwnd)
        left, top, right, bottom = rect

        return left, top, right, bottom
    
    
    # Method to start the capture of the window
    def start_capture(self):
        # Creating bitmap for capturing
        hwnd_dc = win32gui.GetWindowDC(self.hwnd)
        mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
        save_dc = mfc_dc.CreateCompatibleDC()
        bitmap = win32ui.CreateBitmap()
        bitmap.CreateCompatibleBitmap(mfc_dc, self.w, self.h)
        save_dc.SelectObject(bitmap)

        if win32gui.IsIconic(self.hwnd):
            print("Window is minimized. Skipping screenshot capture.")
            return None  # or any appropriate value
        try:
            # This should always be 3, if 1 then case handling would exit with runtime error
            result = windll.user32.PrintWindow(self.hwnd, save_dc.GetSafeHdc(), 3)
            bmpinfo = bitmap.GetInfo()
            bmpstr = bitmap.GetBitmapBits(True)
            img = np.frombuffer(bmpstr, dtype=np.uint8).reshape(
                (bmpinfo["bmHeight"], bmpinfo["bmWidth"], 4)
            )

            # https://www.youtube.com/watch?v=WymCpVUPWQ4
            img = np.ascontiguousarray(img)[
                ..., :-1
            ]  # make image C_CONTIGUOUS and drop alpha channel

            if not result:  # result should be 1
                raise RuntimeError(f"Unable to acquire screenshot! Result: {result}")

            return img
        finally:
            # After returing the image, all the objects must be delted to prevent leak
            win32gui.DeleteObject(bitmap.GetHandle())
            save_dc.DeleteDC()
            mfc_dc.DeleteDC()
            win32gui.ReleaseDC(self.hwnd, hwnd_dc)

