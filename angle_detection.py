import cv2 as cv
import numpy as np
from screen_record import window_capture
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
# Window name
WINDOW_NAME = "Hill Climb Racing"

# Read the template image
template = cv.imread("driver_down.png", cv.IMREAD_UNCHANGED)

# Initialize ORB detector
orb = cv.ORB_create()

# Capture window in HSV
capture = window_capture(WINDOW_NAME)
HSV_filter_values = {
    'low_H': 50,
    'low_S': 70,
    'low_V': 100,
    'high_H': 180,
    'high_S': 255,
    'high_V': 255,
}

while cv.waitKey(1) != ord("q"):
    # Capture frame
    frame_hsv = capture.start_capture()
    # Extract the Value (V) channel from HSV
    # frame_value = frame_hsv[:,:,2]

    # Convert frame to grayscale
    # frame_gray = cv.cvtColor(frame_value, cv.COLOR_GRAY2BGRA)
    frame_gray = frame_hsv

    # Convert the template to HSV
    # template_hsv = cv.cvtColor(template, cv.COLOR_BGR2HSV)
    # template_value = template_hsv[:,:,2]
    template_hsv = template
    # Detect keypoints and descriptors with ORB
    kp1, des1 = orb.detectAndCompute(template_hsv, None)
    kp2, des2 = orb.detectAndCompute(frame_hsv, None)

    # Use the BFMatcher to find the best matches
    bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)

    # Sort them in ascending order of distance
    matches = sorted(matches, key=lambda x: x.distance)

    # Draw matches
    img_matches = cv.drawMatches(template_hsv, kp1, frame_hsv, kp2, matches[:3], None, flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    # Display the result with matches
    cv.imshow("Matches", img_matches)

    # Get the matched keypoints
    src_pts = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

    # Calculate the homography
    H, _ = cv.findHomography(src_pts, dst_pts, cv.RANSAC, 5.0)

    # Extract rotational angle from the homography matrix
    angle_rad = atan2(H[1, 0], H[0, 0])
    angle_deg = angle_rad * 180.0 / pi

    print(f"Rotational Angle: {angle_deg} degrees")

    # cv.imshow("Object Detection", frame_hsv)

cv.destroyAllWindows()