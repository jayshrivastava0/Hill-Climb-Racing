import cv2 as cv
import numpy as np
from multiprocessing import Pool

def match_template(frame, template_path, threshold=0.8, match_cordinates = False):
    """
    Perform template matching on the given frame.

    Args:
        frame: A frame captured by window_capture.
        template_path (str): Path to the template image.
        threshold (float): Threshold value for template matching.

    Returns:
        bool: True if a template match is found, False otherwise.
    """
    # Read the template image
    template = cv.imread(template_path, cv.IMREAD_UNCHANGED)

    # Convert the frame and template to grayscale
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    template_gray = cv.cvtColor(template, cv.COLOR_BGR2GRAY)

    # Perform template matching
    res = cv.matchTemplate(frame_gray, template_gray, cv.TM_CCOEFF_NORMED)

    # Find locations with high matching scores
    loc = np.where(res >= threshold)

    # Draw rectangles around the matched regions
    if match_cordinates == False:
        if len(loc[0]) > 0:
            return True  # Match found

        return False  # No match found
    else:
        if len(loc[0]) > 0:
            top_left = (np.min(loc[1]), np.min(loc[0]))
            bottom_right = (np.max(loc[1]) + template.shape[1], np.max(loc[0]) + template.shape[0])
            match_coords = (top_left, bottom_right)
            return match_coords

        return None  # No match found




# Example usage:
# Assuming `frame` is a frame captured by window_capture and 'template1.png' and 'template2.png' are the paths to the template images
# templates = ['template1.png', 'template2.png']
# match_found = match_templates_parallel(frame, templates)
