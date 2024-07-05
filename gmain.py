import cv2
import numpy as np

class Node:
    def __init__(self, coords):
        self.next: Node = None
        self.coords = coords

class LinkedList:
    def __init__(self):
        self.rear = None
        self.front = None
    
    def push(self, coords):
        if self.rear is None:
            self.rear = Node(coords)
            self.front = self.rear
        else:
            self.rear.next = Node(coords)
            self.rear = self.rear.next
    
    def poll(self):
        coords = self.front.coords
        if self.front == self.rear:
            self.front = None
            self.rear = None
        else:
            self.front = self.front.next
        return coords
    
    def isEmpty(self):
        return self.front == self.rear and self.front == None

def inrange(col1, col2, tolerance):
    # isn't this just the scalar product..?
    # hsv1 = cv2.cvtColor(np.uint8([[col1]]), cv2.COLOR_BGR2HSV)[0][0]
    # hsv2 = cv2.cvtColor(np.uint8([[col2]]), cv2.COLOR_BGR2HSV)[0][0]

    col1 = col1.astype(np.float32)
    col2 = col2.astype(np.float32)

    rdiff = abs(col1[0] - col2[0]) / 255
    gdiff = abs(col1[1] - col2[1]) / 255
    bdiff = abs(col1[2] - col2[2]) / 255

    totaldiff = ((rdiff + gdiff + bdiff) / 3) * 100
    # print(totaldiff)

    return totaldiff < tolerance

def traversal(x, y, limx, limy, iters):
    # queue based mechanism
    bfs = LinkedList()
    visited = set()
    bfs.push((x, y))

    org_colors = img[y][x]
    tolerance = 2.5
    step_length = 2

    while not bfs.isEmpty() and iters > 0:
        _x, _y = bfs.poll()
        visited.add(f'{_x}::{_y}')
        cv2.circle(img, (_x, _y), 1, (0, 0, 255), 1)

        for i in [[0, step_length], [0, -step_length], [step_length, 0], [-step_length, 0]]:
            ox, oy = i
            if f"{ox + _x}::{oy + _y}" not in visited and ox + _x < limx and oy + _y < limy and ox + _x > 0 and oy + _y > 0:
                if inrange(org_colors, img[(oy + _y)][(ox + _x)], tolerance):
                    bfs.push((ox + _x, oy + _y))
        iters -= 1
    print(f"Total runs: {128000 - iters}")

def mouse_handle(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)
        traversal(x, y, img.shape[1], img.shape[0], 128000)
        cv2.imshow("window", img)


img = cv2.imread("6.jpg", cv2.IMREAD_ANYCOLOR)
print(img.shape)

blur = cv2.bilateralFilter(img, 7, 125, 125)
img = blur

cv2.imshow("window", img)
cv2.setMouseCallback("window", mouse_handle)
cv2.waitKey(0)
cv2.destroyAllWindows()

# add in a video format based processing