# CSRT algorithm implementation

import time

import cv2

ESCAPE_KEY = 27
C_KEY = 99


# Get the OpenCV version tuple
w, h = 30, 20

(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
def selectroi(event, x, y, flags, param):
    global bbox
    if event == cv2.EVENT_LBUTTONDOWN:
        bbox = frame[y - (h // 2) : y + (h // 2), x - (w // 2) : x + (w // 2)]
        # bbox = cv2.selectROI(frame, False)

tracker = cv2.TrackerCSRT_create()
video = cv2.VideoCapture("v1.mp4")
video_fps = video.get(cv2.CAP_PROP_FPS)
ideal_delay = 1 / video_fps

cv2.namedWindow("window")
cv2.namedWindow("roi")


# Read first frame
ok, frame = video.read()
bbox = cv2.selectROI(frame, False)
ok = tracker.init(frame, bbox)

cv2.destroyAllWindows()
cv2.namedWindow("window")
cv2.namedWindow("roi")

while True:
    loop_start = time.time()
    
    cv2.setMouseCallback("window", selectroi)
    ok, frame = video.read()
    if not ok:
        break
    
    timer = cv2.getTickCount()
    ok, bbox = tracker.update(frame)

    if ok:
        # Tracking success
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
    else:
        # Tracking failure
        cv2.putText(frame, "Tracking failure detected", (100, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
        bbox = cv2.selectROI(frame, False)
        ok = tracker.init(frame, bbox)

    cv2.putText(frame, "CSRT", (100, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)

    cv2.imshow("window", frame)

    x, y, w, h = bbox
    cv2.imshow("roi", frame[y:y+h, x:x+w])

    loop_end = time.time() - loop_start
    fps_wait_time = max(1, int(ideal_delay - loop_end) * 1000)

    # Exit if ESC pressed
    k = cv2.waitKey(33) & 0xff
    if k == ESCAPE_KEY:
        break

    # Reselect tracking target if `C` is pressed
    if k == C_KEY:
      cv2.destroyAllWindows()
      bbox = cv2.selectROI(frame, False)
      ok = tracker.init(frame, bbox)
      
      cv2.destroyAllWindows()
      cv2.namedWindow("window")
      cv2.namedWindow("roi")

video.release()
cv2.destroyAllWindows()
