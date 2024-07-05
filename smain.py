import cv2
import sys
import cv2.legacy

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

cv2.namedWindow("window")
cv2.namedWindow("roi")


# Read first frame
ok, frame = video.read()
bbox = cv2.selectROI(frame, False)
ok = tracker.init(frame, bbox)

while True:
    # Read a new frame
    cv2.setMouseCallback("window", selectroi)
    ok, frame = video.read()
    if not ok:
        break
    
    timer = cv2.getTickCount()
    ok, bbox = tracker.update(frame)
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

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

    cv2.putText(frame, "CSRT", (100, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)

    cv2.putText(frame, "FPS : " + str(int(fps)), (100, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)

    cv2.imshow("window", frame)
    cv2.imshow("roi", bbox)

    # Exit if ESC pressed
    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break

video.release()
cv2.destroyAllWindows()
