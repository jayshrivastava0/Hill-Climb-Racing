from gymnasium import Env
import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt
import importlib
# from screen_record import window_capture
import cv2
import template_matching
import time
import screen_record
# importlib.reload(screen_record)
importlib.reload(screen_record)
importlib.reload(template_matching)
from screen_record import window_capture
import pydirectinput
import pyautogui
import pygetwindow




height = 200
width = 200
channels = 3


class HillClimbRacingEnv(Env):
    def __init__(self) -> None:
        super().__init__()
        ## Action spaces will be gas, break, and doing nothing
        self.action_space = gym.spaces.Discrete(3)
        # Define observation space
        self.observation_space = gym.spaces.Box(low=0, high=255, shape=(10, height, width, channels), dtype=np.uint8)  # Image frame 
        self.left_coordinate = 0
        self.bottom_coordinate = 0
        self.top_coordinate = 0
        self.right_coordinate = 0


    def get_screen_capture(self):
        WINDOW_NAME = "Hill Climb Racing"

        # Capture window
        capture = window_capture(WINDOW_NAME)
        frame_hsv = capture.start_capture()
        img_rgb = cv2.cvtColor(frame_hsv, cv2.COLOR_BGR2RGB)
        # Get the coordinates of the game window relative to the screen
        self.left_coordinate, self.top_coordinate, self.right_coordinate, self.bottom_coordinate = capture.get_window_coordinates()
        return img_rgb


    
    def game_over(self, screen_frame):
        template_match_check1 = template_matching.match_template(screen_frame, r"D:\OneDrive - University at Buffalo\Projects\Misc\Hill Climb Racing\game_over\out_of_fuel.png")
        template_match_check2 = template_matching.match_template(screen_frame, r"D:\OneDrive - University at Buffalo\Projects\Misc\Hill Climb Racing\game_over\driver_down.png")
        if template_match_check2 or template_match_check1:
            return True
        return False
    
    def step(self, action):
        action_map = {
            0: None,  # No Key
            1: "right",  # Right Arrow Key
            2: "left"  # Left Arrow Key
        }

        # Release all keys
        pydirectinput.keyUp('right')
        pydirectinput.keyUp('left')

        # Press the specified key
        if action != 0:
            key = action_map.get(action)
            if key:
                pydirectinput.keyDown(key)

        next_frame = self.get_screen_capture()
        is_game_over = self.game_over(next_frame)
        reward = 1
        info = {}

        return next_frame, reward, is_game_over, info
    
    def render(self):
        while cv2.waitKey(1) != ord("q"):
            cv2.imshow("GamePlay", cv2.cvtColor(self.get_screen_capture(), cv2.COLOR_BGR2RGB))

        
    def close(self):
        cv2.destroyAllWindows()
            
    def reset(self, screen_frame):
        match_coords = template_matching.match_template(screen_frame, r'D:\OneDrive - University at Buffalo\Projects\Misc\Hill Climb Racing\restarting_game\press_button_to_continue.png', match_cordinates=True)
        if match_coords:
                print("Matching coordinates found of template", match_coords)
                print("bottom_coordinate", self.bottom_coordinate, "\ntop_coordinate",self.top_coordinate, 
                    "\nleft_coordinate", self.left_coordinate, "\nright_coordinate",self.right_coordinate)
                # Calculate the absolute coordinates of the match relative to the game window
                (x1, y1), (x2, y2) = match_coords
                avg_x = (x1 + x2) // 2
                avg_y = (y1 + y2) // 2

                # Adjust coordinates relative to the game window
                avg_x += self.left_coordinate
                avg_y += self.top_coordinate

                print("click cordinates : ", avg_x, avg_y)

                # Draw a circle at the click location
                click_visualization = cv2.circle(screen_frame, (avg_x, avg_y), radius=10, color=(0, 255, 0), thickness=-1)
                
                # Display the image with the click visualization
                # plt.imshow(click_visualization)
                # plt.show()

                # Bring the game window to the foreground
                game_window = pygetwindow.getWindowsWithTitle("Hill Climb Racing")[0]
                game_window.activate()

                # Simulate pressing the space key within the game window
                pyautogui.press('space')
                print("Pressed space key within the game window")




hill_climb_racing = HillClimbRacingEnv()
hill_climb_racing.reset(hill_climb_racing.get_screen_capture())