import win32gui, win32ui, win32con
from time import time
from screen_record import window_capture
import cv2

# template = cv2.imread(
#     "D:\OneDrive - University at Buffalo\Projects\Misc\Hill Climb Racing\car_object.png",
#     cv2.IMREAD_GRAYSCALE,
# )

HSV_filter_values = {
    'low_H': 50,
    'low_S': 70,
    'low_V': 100,
    'high_H': 180,
    'high_S': 255,
    'high_V': 255,
}

def main():
    # Capturing Hill Climb Racing Window
    WINDOW_NAME = "Hill Climb Racing"
    start_time = time()
    frame_count = 0

    win32gui.EnumWindows(window_capture.opened_windows, None)



    while True:
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        screenshot = window_capture(WINDOW_NAME).start_capture()
        
   
        cv2.imshow('CV', screenshot)


        frame_count += 1
        elapsed_time = time() - start_time

        if elapsed_time >= 0.01:  # Update FPS every second
            fps = frame_count / elapsed_time
            print(f"FPS: {fps:.2f}")
            frame_count = 0
            start_time = time()

    # if q is pressed close the CV windows
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
