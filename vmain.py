import cv2
import numpy as np

cap = cv2.VideoCapture("v5.webm")

frame = None
roi = cv2.imread("template2.png", cv2.IMREAD_ANYCOLOR)
w, h = 30, 20
top_left_history = []
bottom_right_history = []

cv2.namedWindow("window")
cv2.namedWindow("roi")

def mouse_handle(event, x, y, flags, param):
    global roi, top_left_history, bottom_right_history
    if event == cv2.EVENT_LBUTTONDOWN:
        roi = gray_frame[y - (h // 2) : y + (h // 2), x - (w // 2) : x + (w // 2)]
        top_left_history = []
        bottom_right_history = []

while True:
    ret, frame = cap.read()
    cv2.setMouseCallback("window", mouse_handle)
    
    gray_frame = frame.copy() #cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.GaussianBlur(frame, (5, 5), 0)

    res = cv2.matchTemplate(gray_frame, roi, cv2.TM_SQDIFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    top_left = min_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    draw_frame = cv2.rectangle(frame, top_left, bottom_right, (255, 0, 0 ), 2)

    # Correlation filtering? CSRT. Mean shifting? Camshifting?

    # need to run a daemon that periodically updates the template. workflow:
    # acquire position through ROI
    # estimate future position(RK4, Euler) and average it out
    # estimate likeness between future track and current ROI track
    # if they both agree, update the track to future position
    # if it is dissimilar, then disregard future pos and calculate again. if no confirmation by third try, drop track.

    # track can be considered invalid if the ROI track goes away more than 50pixels in either direction within a single frame or two.

    cv2.imshow("window", frame)
    cv2.imshow("roi", roi)
    # cv2.imshow("res", res)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()