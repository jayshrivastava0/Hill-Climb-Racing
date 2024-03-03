import cv2 as cv
import numpy as np
from math import atan2, cos, sin, sqrt, pi

def drawAxis(img, p_, q_, colour, scale):
    p = list(p_)
    q = list(q_)

    angle = atan2(p[1] - q[1], p[0] - q[0])  # angle in radians
    hypotenuse = sqrt((p[1] - q[1]) * (p[1] - q[1]) + (p[0] - q[0]) * (p[0] - q[0]))

    # Here we lengthen the arrow by a factor of scale
    q[0] = p[0] - scale * hypotenuse * cos(angle)
    q[1] = p[1] - scale * hypotenuse * sin(angle)

    cv.line(img, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), colour, 1, cv.LINE_AA)

    # create the arrow hooks
    p[0] = q[0] + 9 * cos(angle + pi / 4)
    p[1] = q[1] + 9 * sin(angle + pi / 4)
    cv.line(img, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), colour, 1, cv.LINE_AA)

    p[0] = q[0] + 9 * cos(angle - pi / 4)
    p[1] = q[1] + 9 * sin(angle - pi / 4)
    cv.line(img, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), colour, 1, cv.LINE_AA)


def getOrientation(pts, img):
    sz = len(pts)
    data_pts = np.empty((sz, 2), dtype=np.float64)

    for i in range(data_pts.shape[0]):
        data_pts[i, 0] = pts[i, 0, 0]
        data_pts[i, 1] = pts[i, 0, 1]

    # Perform PCA analysis
    mean = np.empty((0))
    mean, eigenvectors, eigenvalues = cv.PCACompute2(data_pts, mean)

    # Store the center of the object
    cntr = (int(mean[0, 0]), int(mean[0, 1]))

    cv.circle(img, cntr, 3, (255, 0, 255), 2)
    p1 = (
        cntr[0] + 0.02 * eigenvectors[0, 0] * eigenvalues[0, 0],
        cntr[1] + 0.02 * eigenvectors[0, 1] * eigenvalues[0, 0],
    )
    p2 = (
        cntr[0] - 0.02 * eigenvectors[1, 0] * eigenvalues[1, 0],
        cntr[1] - 0.02 * eigenvectors[1, 1] * eigenvalues[1, 0],
    )
    drawAxis(img, cntr, p1, (0, 255, 0), 1)
    drawAxis(img, cntr, p2, (255, 255, 0), 5)
    angle = atan2(eigenvectors[0, 1], eigenvectors[0, 0])  # orientation in radians

    return angle, cntr

import time
capture_interval = 2  # seconds
last_capture_time = time.time()
def angle_detection(frame, low_H, low_S, low_V, high_H, high_S, high_V):
    global last_capture_time
    # Convert the frame to HSV
    frame_HSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # Threshold the image based on HSV values
    frame_threshold = cv.inRange(frame_HSV, (low_H, low_S, low_V), (high_H, high_S, high_V))

    # Find contours in the thresholded image
    contours, _ = cv.findContours(frame_threshold, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)

    if contours:
        # Get the largest contour
        max_contour = max(contours, key=cv.contourArea, default=None)

        # Draw the largest contour on the thresholded image
        cv.drawContours(frame_threshold, [max_contour], -1, (255, 255, 255), 2)

        # Get orientation angle and center of the largest contour
        angle, center = getOrientation(max_contour, frame_threshold)
        current_time = time.time()

        # Capture frame every 5 seconds
        if current_time - last_capture_time >= capture_interval:
            print(f"Angle: {angle * 180 / pi} degrees")
            print(f"Center: {center}")
            last_capture_time = current_time

        # Draw the axis on the original frame
        drawAxis(frame, center, (center[0] + cos(angle), center[1] + sin(angle)), (0, 255, 0), 1)


    # Display the thresholded image with HSV trackbars
    cv.imshow('Thresholded Image', frame_threshold)



window_detection_name = 'Object Detection'
cv.namedWindow(window_detection_name)



max_value = 255
max_value_H = 360//2
low_H = 0
low_S = 0
low_V = 0
high_H = max_value_H
high_S = max_value
high_V = max_value
low_H_name = 'Low H'
low_S_name = 'Low S'
low_V_name = 'Low V'
high_H_name = 'High H'
high_S_name = 'High S'
high_V_name = 'High V'


def on_low_H_thresh_trackbar(val):
    global low_H
    global high_H
    low_H = val
    low_H = min(high_H-1, low_H)
    cv.setTrackbarPos(low_H_name, window_detection_name, low_H)
def on_high_H_thresh_trackbar(val):
    global low_H
    global high_H
    high_H = val
    high_H = max(high_H, low_H+1)
    cv.setTrackbarPos(high_H_name, window_detection_name, high_H)
def on_low_S_thresh_trackbar(val):
    global low_S
    global high_S
    low_S = val
    low_S = min(high_S-1, low_S)
    cv.setTrackbarPos(low_S_name, window_detection_name, low_S)
def on_high_S_thresh_trackbar(val):
    global low_S
    global high_S
    high_S = val
    high_S = max(high_S, low_S+1)
    cv.setTrackbarPos(high_S_name, window_detection_name, high_S)
def on_low_V_thresh_trackbar(val):
    global low_V
    global high_V
    low_V = val
    low_V = min(high_V-1, low_V)
    cv.setTrackbarPos(low_V_name, window_detection_name, low_V)
def on_high_V_thresh_trackbar(val):
    global low_V
    global high_V
    high_V = val
    high_V = max(high_V, low_V+1)
    cv.setTrackbarPos(high_V_name, window_detection_name, high_V)


cv.createTrackbar(low_H_name, window_detection_name , low_H, max_value_H, on_low_H_thresh_trackbar)
cv.createTrackbar(high_H_name, window_detection_name , high_H, max_value_H, on_high_H_thresh_trackbar)
cv.createTrackbar(low_S_name, window_detection_name , low_S, max_value, on_low_S_thresh_trackbar)
cv.createTrackbar(high_S_name, window_detection_name , high_S, max_value, on_high_S_thresh_trackbar)
cv.createTrackbar(low_V_name, window_detection_name , low_V, max_value, on_low_V_thresh_trackbar)
cv.createTrackbar(high_V_name, window_detection_name , high_V, max_value, on_high_V_thresh_trackbar)

WINDOW_NAME = "Hill Climb Racing"
from screen_record import window_capture

while cv.waitKey(1) != ord("q"):
    frame = window_capture(WINDOW_NAME).start_capture()

    # Get current trackbar values
    low_H = cv.getTrackbarPos(low_H_name, window_detection_name)
    high_H = cv.getTrackbarPos(high_H_name, window_detection_name)
    low_S = cv.getTrackbarPos(low_S_name, window_detection_name)
    high_S = cv.getTrackbarPos(high_S_name, window_detection_name)
    low_V = cv.getTrackbarPos(low_V_name, window_detection_name)
    high_V = cv.getTrackbarPos(high_V_name, window_detection_name)

    # Perform angle detection with the current HSV thresholds
    angle_detection(frame, low_H, low_S, low_V, high_H, high_S, high_V)

# Close the OpenCV windows when 'q' is pressed
cv.destroyAllWindows()