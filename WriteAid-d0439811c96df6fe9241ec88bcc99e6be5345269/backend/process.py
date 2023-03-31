import cv2
import numpy as np
import math
prev_gray = None
prev_flow = None
rf = False
inc = 0
rcorners = None
prev_corners = None
def quadrilateral_area(points):
    # Extract x and y coordinates of the points
    x = points[:, 0, 0]
    y = points[:, 0, 1]

    # Calculate the area using Shoelace formula
    area = 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))

    return area
def angle(p1, p2):
    xDiff = p2[0][0] - p1[0][0]
    yDiff = p2[0][1] - p1[0][1]
    return math.degrees(math.atan2(yDiff, xDiff))

# Sort method to ensure that the order of the corners starts from the top left and goes clockwise
def sort(points):
    distances_to_origin = np.linalg.norm(points, axis=1)
    top_left_point = points[np.argmin(distances_to_origin)]
    # Create a list of the other points
    other_points = [p for p in points if not np.array_equal(p, top_left_point)]
    # Sort the list of other points by their angle with the x-axis
    other_points.sort(key=lambda p: np.arctan2(p[1] - top_left_point[1], p[0] - top_left_point[0]))
    # Return the sorted list of points
    return np.array([top_left_point] + other_points)

# Method to determine the contour that most resembles a piece of paper
def find_largest_rectangle(contours):
    largest_rectangle = None
    largest_area = 0
    bestcnt = None
    for cnt in contours:
        # Approximate the contour as a polygon
        epsilon = 0.02*cv2.arcLength(cnt,True)
        approx = cv2.approxPolyDP(cnt,epsilon,True)
        area = cv2.contourArea(approx)
        if area > largest_area:
            largest_rectangle = approx
            largest_area = area
            bestcnt = cnt
    if bestcnt is not None:
        rect = cv2.minAreaRect(bestcnt)


        rect_width, rect_height = rect[1]


        diff = abs(cv2.contourArea(bestcnt) - rect_width*rect_height)
        if(diff < .8 or rect_width*rect_height < 200000):
            bestcnt = None
    return bestcnt
def removefg(img):
    fgbg = cv2.createBackgroundSubtractorMOG2()

    # Apply the background subtractor to the image
    fgmask = fgbg.apply(img)

    # Apply a binary threshold to the mask to separate the foreground and background
    ret, thresh = cv2.threshold(fgmask, 0, 255, cv2.THRESH_BINARY)

    # Multiply the image with the mask to remove the foreground
    img = img * thresh[:, :, np.newaxis]
    return img
def findrect(points):
    # Approximate the polygon as a quadrilateral
    epsilon = 0.02 * cv2.arcLength(points, True)
    approx = cv2.approxPolyDP(points, epsilon, True)

    # Check if the approximation is a quadrilateral
    if len(approx) == 4:
        return approx
    else:
        # Find the convex hull of the polygon
        hull = cv2.convexHull(points)

        # Find the center of the convex hull
        center = np.mean(hull, axis=0)


        sorted_points = []

        # Get the centroid of the points
        centroid = np.mean(hull, axis=0)

        # Define a function to calculate the angle between two points
        # Sort the points by angle in relation to the centroid
        sorted_points = sorted(hull, key=lambda p: angle(centroid, p))

        # Take the first 4 points of the sorted list
        sorted_points = sorted_points[:4]

        return np.array(sorted_points)

def track_coords(gray, coords, prev_coords, prev_gray):

    # Apply temporal smoothing
    if prev_coords is not None:

        coords = (coords + prev_coords) / 2

    # Calculate optical flow
    # if prev_coords is not None:
    #     print("first", coords.astype(np.float32))
    #     flow, status, err = cv2.calcOpticalFlowPyrLK(prev_gray, gray,prev_coords.astype(np.float32),coords.astype(np.float32), winSize=(10, 10), maxLevel=3, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
    #     coords = coords[status==1]
    #     coords = coords.astype(np.float64)

def complete_stencil(input_path, coordinates, stencil_path):
    coordinates = np.array(coordinates, dtype=np.float32).reshape(4,1,2)
    # Sample stencil
    stencil = cv2.imread(stencil_path)
    frame = cv2.imread(input_path)
    src_img = np.ones((512, 512, 3), dtype=np.uint8) * 255

    framecopy = frame.copy()
    polygon = frame.copy()
    page = frame.copy()
    bg = removefg(frame)
    result = frame
    # Grayscale
    gray = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY)
    # Gaussian blur
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    blur = cv2.bitwise_not(blur)
    # Threshold
    #thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    #thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    otsu = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    k = np.ones((3,3), np.uint8)
    # Apply the darkening kernel to the non-white pixels
    erode = cv2.erode(thresh, k, iterations = 1)
    # Apply morphology
    kernel = np.ones((7,7), np.uint8)
    morph = cv2.morphologyEx(otsu, cv2.MORPH_CLOSE, kernel)
    morph = cv2.morphologyEx(erode, cv2.MORPH_CLOSE, kernel)
    morph = cv2.morphologyEx(morph, cv2.MORPH_OPEN, kernel)
    morph = cv2.bitwise_not(morph)
    contours = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Determine optimal contour

    contours = contours[0]
    contour = find_largest_rectangle(contours)

    if (contour is not None):
            # Find corners
        cv2.drawContours(frame, [contour], 0, (255,255,255), -1)
        page = np.zeros_like(frame)
        cv2.drawContours(morph, contours, 0, (255,255,255), -1)

        segment = cv2.arcLength(contour, True)
        corners = cv2.approxPolyDP(contour, 0.04 * segment, True)
        prev_corners = corners.copy()
        corners = findrect(corners)


        polygon = frame.copy()
        cv2.polylines(polygon, [corners], True, (0,0,255), 1, cv2.LINE_AA)
        pts_src = np.array([[0, 0], [src_img.shape[1] - 1, 0], [src_img.shape[1] - 1, src_img.shape[0] - 1], [0, src_img.shape[0] - 1]])
        pts_sten = np.array([[0, 0], [stencil.shape[1] - 1, 0], [stencil.shape[1] - 1, stencil.shape[0] - 1], [0, stencil.shape[0] - 1]])

        # Displays the stencil if the contour is a quadrilateral
        if (len(corners)) == 4:
            # Sort points

            if(rcorners is not None):
                pts_dst = sort(rcorners.reshape(-1, 2)).reshape(4, 1, 2)
            else:
                pts_dst = sort(corners.reshape(-1, 2)).reshape(4, 1, 2)
            # Find homography (perspective conversion) matrix
            mat, status = cv2.findHomography(pts_src, pts_dst)
            # Converts perspective
            rmat, status = cv2.findHomography(pts_dst, pts_src)
            warped_points = cv2.perspectiveTransform(coordinates.reshape(-1, 1, 2), rmat)
            stenmat, status = cv2.findHomography(warped_points, pts_sten)
            stenwarp = cv2.warpPerspective(stencil, stenmat, (src_img.shape[1], src_img.shape[0]))
            src_img += stenwarp
            warp = cv2.warpPerspective(src_img, mat, (frame.shape[1], frame.shape[0]))
            # Overlay the stencil
            # result = framecopy + warp
            # Translucency
            alpha = 0.3

            # Performs the translucent overlay
            result = cv2.addWeighted(framecopy, 1 - alpha, warp, alpha, 0)
            cv2.imwrite("processed.jpg", result)
            cv2.imwrite("complete_sten.jpg", src_img)

def process_frame(input_path, sten_path):
    # Sample stencil
    stencil = cv2.imread(sten_path)
    frame = cv2.imread(input_path)

    framecopy = frame.copy()
    polygon = frame.copy()
    page = frame.copy()
    bg = removefg(frame)
    result = frame
    # Grayscale
    gray = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY)
    # Gaussian blur
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    blur = cv2.bitwise_not(blur)
    # Threshold
    #thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    #thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    otsu = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    k = np.ones((3,3), np.uint8)
    # Apply the darkening kernel to the non-white pixels
    erode = cv2.erode(thresh, k, iterations = 1)
    # Apply morphology
    kernel = np.ones((7,7), np.uint8)
    morph = cv2.morphologyEx(otsu, cv2.MORPH_CLOSE, kernel)
    morph = cv2.morphologyEx(erode, cv2.MORPH_CLOSE, kernel)
    morph = cv2.morphologyEx(morph, cv2.MORPH_OPEN, kernel)
    morph = cv2.bitwise_not(morph)
    contours = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Determine optimal contour

    contours = contours[0]
    contour = find_largest_rectangle(contours)

    if (contour is not None):
            # Find corners
        cv2.drawContours(frame, [contour], 0, (255,255,255), -1)
        page = np.zeros_like(frame)
        cv2.drawContours(morph, contours, 0, (255,255,255), -1)

        segment = cv2.arcLength(contour, True)
        corners = cv2.approxPolyDP(contour, 0.04 * segment, True)
        prev_corners = corners.copy()
        corners = findrect(corners)


        polygon = frame.copy()
        cv2.polylines(polygon, [corners], True, (0,0,255), 1, cv2.LINE_AA)
        pts_src = np.array([[0, 0], [stencil.shape[1] - 1, 0], [stencil.shape[1] - 1, stencil.shape[0] - 1], [0, stencil.shape[0] - 1]])
        # Displays the stencil if the contour is a quadrilateral
        if (len(corners)) == 4:
            # Sort points

            if(rcorners is not None):
                pts_dst = sort(rcorners.reshape(-1, 2)).reshape(4, 1, 2)
            else:
                pts_dst = sort(corners.reshape(-1, 2)).reshape(4, 1, 2)
            # Find homography (perspective conversion) matrix
            mat, status = cv2.findHomography(pts_src, pts_dst)

            warp = cv2.warpPerspective(stencil, mat, (frame.shape[1], frame.shape[0]))
            # Overlay the stencil
            # result = framecopy + warp
            # Translucency
            alpha = 0.3

            # Performs the translucent overlay
            result = cv2.addWeighted(framecopy, 1 - alpha, warp, alpha, 0)
            cv2.imwrite("processed.jpg", result)
