# Hill Climb Racing AI Agent

## Overview

This project aims to develop an AI agent capable of playing the popular mobile game "Hill Climb Racing" using reinforcement learning techniques. The game involves maneuvering a car to navigate through challenging terrain while performing stunts like backflips and front flips to earn bonus points.

## Gameplay

Hill Climb Racing is a physics-based driving game where the objective is to keep the car upright and advance as far as possible along the terrain. The game features various obstacles, ramps, and opportunities for performing stunts. Executing a successful 360-degree backflip or front flip awards a substantial bonus of approximately 1,000 points.

https://github.com/jayshrivastava0/Hill-Climb-Racing/assets/98177190/568378a0-a9db-48aa-8b37-cdbb5dacba20

## Approach

### Template Matching

During the development process, I encountered various challenges, particularly in the realm of object detection. Initially, I experimented with template matching techniques, but faced limitations in capturing the dynamic movement of the car and its environment accurately. Despite efforts to optimize template matching parameters and incorporate HSV (Hue, Saturation, Value) color space, the results fell short of expectations.

### YOLO and ORB
Initially, I explored the possibility of using object detection techniques like YOLO (You Only Look Once) and ORB (Oriented FAST and Rotated BRIEF) feature matching to detect the car's position and orientation within the game screen.

For **ORB feature matching**, the results were not satisfactory due to a significant number of false positives.

https://github.com/jayshrivastava0/Hill-Climb-Racing/assets/98177190/b69144da-d535-486c-bf5d-060305c9fd01

The feature matching algorithm struggled to accurately identify the car's position and orientation, often confusing it with other visual elements like the gasoline icon, printed text, coins, and other icons. The presence of flashing signals, varying colors, and dynamic visuals in the game environment contributed to the false positive detections. Despite trying different configurations and color spaces, the ORB feature matching approach did not yield the desired level of accuracy for this particular use case.


For **YOLO**, I utilized the YOLOv5 model and added custom classes specific to this game's use case. The results obtained from YOLO are showcased below:


| Labels <br> ![Labels](https://github.com/jayshrivastava0/Hill-Climb-Racing/blob/main/yolo_results/labels.jpg) | Labels Correlogram <br> ![Labels Correlogram](https://github.com/jayshrivastava0/Hill-Climb-Racing/blob/main/yolo_results/labels_correlogram.jpg) |
|:---:|:---:|
| F1 Curve <br> ![F1 Curve](https://github.com/jayshrivastava0/Hill-Climb-Racing/blob/main/yolo_results/F1_curve.png) | Confusion Matrix <br> ![Confusion Matrix](https://github.com/jayshrivastava0/Hill-Climb-Racing/blob/main/yolo_results/confusion_matrix.png) |
| P Curve <br> ![P Curve](https://github.com/jayshrivastava0/Hill-Climb-Racing/blob/main/yolo_results/P_curve.png) | PR Curve <br> ![PR Curve](https://github.com/jayshrivastava0/Hill-Climb-Racing/blob/main/yolo_results/PR_curve.png) |
| R Curve <br> ![R Curve](https://github.com/jayshrivastava0/Hill-Climb-Racing/blob/main/yolo_results/R_curve.png) | Results <br> ![Results](https://github.com/jayshrivastava0/Hill-Climb-Racing/blob/main/yolo_results/results.png) |


However, these approaches proved increasingly tedious and challenging, particularly when accounting for the car's rotation during stunts and other visual complexities.

After careful consideration, I decided to focus my efforts on developing an AI agent using reinforcement learning techniques. This approach allows the agent to learn and adapt through trial-and-error interactions with the game environment, potentially leading to more robust and effective gameplay.

## Current Progress

Currently, the project is in the active development phase, and several redundant files and an unorganized README exist. However, substantial progress has been made in preparing the groundwork for the reinforcement learning agent.


## Contribution

As this project is still a work in progress, I welcome contributions from the community. If you're interested in collaborating or have suggestions for improvement, please feel free to raise a pull request or reach out to me directly.

Additionally, I maintain a [blog](https://jayshrivastava.blogspot.com/2024/01/hill-climb-racing-automation.html) where I document my journey and share insights gained throughout the project's development.

## Future Work

As we look ahead, there are several key areas that will drive the evolution of this project, enhancing both its functionality and performance. Here's a brief overview of the future endeavors:

-  Reward System Design: Define a comprehensive reward system that incentivizes the agent's desired behaviors, such as collecting coins, performing flips, and maintaining car stability.


-  Reinforcement Learning Algorithm Selection: Choose an appropriate reinforcement learning algorithm (e.g., Deep Q-Networks, Proximal Policy Optimization) to train the agent based on the defined rewards.


-  Training and Evaluation: Conduct extensive training simulations to refine the agent's decision-making and evaluate its performance against various game scenarios.










<!---


# This blog covers my journey for this project.
https://jayshrivastava.blogspot.com/2024/01/hill-climb-racing-automation.html 


## Gameplay

https://github.com/jayshrivastava0/Hill-Climb-Racing/assets/98177190/568378a0-a9db-48aa-8b37-cdbb5dacba20



###
## The project is still in the works therefore there are so many redundant files and readme is still not organized
###

So after moving the mss and varios other window capture, I decided to go window api screenshot
it was giving me the flexiblity to capture any window, not the whole screen. So it was good and the FPS was also
respectable, and with just few optimizations the FPS jumped to pretty good.



Now i'm struck at template matching for object detection. Without nay preprocssing HSRV and all it is capturing the car,
but not keeping the car withing the bounding box and many times i would say half of the time the bounding box is 
pointing ti the sky on thee right part of the screen rather on the car which is on the left part of the screen.
So template matching is working but not as nicely as i would have hoped for. So let's try some optimization


So i tried for template matching
result = cv.matchTemplate(image, template, cv.TM_SQDIFF)
result = cv.matchTemplate(image, template, cv.TM_SQDIFF_NORMED)
result = cv.matchTemplate(image, template, cv.TM_CCORR)
result = cv.matchTemplate(image, template, cv.TM_CCORR_NORMED)
result = cv.matchTemplate(image, template, cv.TM_CCOEFF)
result = cv.matchTemplate(image, template, cv.TM_CCOEFF_NORMED)



For SQDIFF i even tried with already grayscale image, and even without background, filling the background with white , to create a drastic difference. 
Also i tried with others as well, to provide an image without background but it's not working.

Best is CCOEFF it matches the car, but jitters very much, idk why so for now it's threshold is 0.65
But let's see tomorrow we can change HSRV and try to do template matching with that.











After trying out HSV and incorporating it into the screen capture with object detection using template matching, I encountered a a roadblock. Now I tried to template match for object detection this created a very huge problem for me as, when the car moves in the game, the camera rolls backward according to speed. Now this is very problematic because my template has the car in certain angle i.e. 0 degree from the ground meaning totally flat to the ground. The game is over when car hits the floor at 180 snapping the neck of the driver and finsihing the game. So with template matching, this would not be able to observe since there is actually very large bonus points are given if you rotate in mid air, meaning, flip 360 in mid air in any direction. So this risk you take to flip gives out the reward in monetary terms so to collect the data, i have to actually at all times collect the data of rotation, but since this is not possible with template matching. I'll drop this pipeline now. 

Now there are two options to explore
1. YOLO

https://github.com/jayshrivastava0/Hill-Climb-Racing/assets/98177190/3c387d98-a89a-421f-869e-01ca21e2feb2


   
1. Feature Matching using ORB

https://github.com/jayshrivastava0/Hill-Climb-Racing/assets/98177190/b69144da-d535-486c-bf5d-060305c9fd01





Now i tried with feature matching with orb as well, but the problem is That Feature mapping is not performing as I would have wanted it to the reason that I saw was because when I was featured matching it the icon for gasoline actually very closely matches with the color ofOffer that's Why it was getting confused moreover I was constantly observing that whenever anything is printed on the screen while playing the game suppose air time or neck flip bonus or any kind of bonus or any kind of flashing text is generated it is actually outllined by black color And the same color was of the car's front so it was again getting very confused with thatI think feature matching would have Formed very well if the game was little less flashy there are coins there is the meter for gasoline there is the icon to get the gasoline and fill up your tank also there is some gems as well also whenever the fuel starts to get low flashing right signals appear on the screen signaling that the fuel is low that color it is little less red but it again could be a problem also after so much of Of playing out with different configurations most of the time feature matching was happening from the hat of the driver....closely matches with other icons such as Highest record and full screen icon so again if I was increasing the number of feature matching it was getting confused between all those things if I was reducing it then I was not properly satisfied with the feature matching so feature matching using org didn't turn out as well as I would have liked it too also to feature match I tried to do it in grayscale in rgb and bgr is different configuration in the colors as well, but upto no avail.



So it can be clearly seen that yolo was performing better. So i decided to go with YOLO.
This is the yolo results. I have not deleted the already shipped classification instances provided by YOLOv5. I just added some of my own classes for this particular use cases.


![YOLO Confusion Matrix](https://github.com/jayshrivastava0/Hill-Climb-Racing/blob/main/yolo_results/confusion_matrix.png)


![F1 Curve](https://github.com/jayshrivastava0/Hill-Climb-Racing/blob/main/yolo_results/F1_curve.png)


![Labels_Correlogram](https://github.com/jayshrivastava0/Hill-Climb-Racing/blob/main/yolo_results/labels_correlogram.jpg)


![P_curve](https://github.com/jayshrivastava0/Hill-Climb-Racing/blob/main/yolo_results/P_curve.png)


![PR_curve](https://github.com/jayshrivastava0/Hill-Climb-Racing/blob/main/yolo_results/PR_curve.png)


![R_curve](https://github.com/jayshrivastava0/Hill-Climb-Racing/blob/main/yolo_results/R_curve.png)


![Labels](https://github.com/jayshrivastava0/Hill-Climb-Racing/blob/main/yolo_results/labels.jpg)


![Results|50%](https://github.com/jayshrivastava0/Hill-Climb-Racing/blob/main/yolo_results/results.png)

-->
