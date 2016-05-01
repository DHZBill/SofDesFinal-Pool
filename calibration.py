'''
Allows user to calibrate to pool table

Instructions: Set an input image, click on four corners in order (TL, TR, BR, BL)

Credits: Code is adapted from Adrian Rosebrock's "4 point openCV Example"
            on pyimagesearch.com
'''
import numpy as np
import cv2

ref_pts = [] # global list of corner points

def order_points(pts):
    # initialzie a list of coordinates that will be ordered
    # such that the first entry in the list is the top-left,
    # the second entry is the top-right, the third is the
    # bottom-right, and the fourth is the bottom-left
    rect = np.zeros((4, 2), dtype = "float32")

    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    s = pts.sum(axis = 1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # now, compute the difference between the points, the
    # top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff = np.diff(pts, axis = 1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    # return the ordered coordinates
    return rect

def four_point_transform(image, pts):
    # obtain a consistent order of the points and unpack them
    # individually
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    # compute the width of the new image, which will be the
    # maximum distance between bottom-right and bottom-left
    # x-coordiates or the top-right and top-left x-coordinates
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    # compute the height of the new image, which will be the
    # maximum distance between the top-right and bottom-right
    # y-coordinates or the top-left and bottom-left y-coordinates
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    # now that we have the dimensions of the new image, construct
    # the set of destination points to obtain a "birds eye view",
    # (i.e. top-down view) of the image, again specifying points
    # in the top-left, top-right, bottom-right, and bottom-left
    # order
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype = "float32")

    # compute the perspective transform matrix and then apply it
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    # return the warped image
    return warped

def store_points(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        global ref_pts
        coords = (x, y)
        ref_pts.append(coords)

def calibrate_interface(file_name):
    '''
    Runs the four-point click calibration process.
    Click in order: top-left, top-right, bottom-right, bottom-left

    Inputs:
    file_name: a string that points to the image used for specifying the corners
    '''

    img = cv2.imread(file_name) # set input image
    # initialize the window and set interaction function
    cv2.namedWindow('original')
    cv2.setMouseCallback('original', store_points)

    while True:
        # display the input image
        cv2.imshow('original',img)

        # wait until there have been 4 clicks
        if len(ref_pts) > 3:
            pts = np.array(ref_pts)
            warped = four_point_transform(img, pts)
            #display the transformed image
            cv2.imshow('warped', warped)
            cv2.waitKey(0)
            break

        #press esc to exit
        key = cv2.waitKey(10)
        if key == 27:
            raise RuntimeError('User escaped the four-point calibration process')
            break
    cv2.destroyAllWindows

calibrate_interface('pool_pic.JPG')
