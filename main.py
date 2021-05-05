import cv2
import imutils
from picamera.array import PiRGBArray
from picamera import PiCamera
from servo_control import *

green_lower = (10, 10, 6)
green_upper = (64, 255, 255)

cam = PiCamera()
cam.resolution = (640, 480)
cam.framerate = 32
cap = PiRGBArray(cam, size=(640, 480))

with_motion = True

for frame in cam.capture_continuous(cap, format='bgr', use_video_port=True):
    img = frame.array
    
    img = imutils.resize(img, width=600)
    blurred = cv2.GaussianBlur(img, (11, 11), 0)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, green_lower, green_upper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None

    if len(cnts) > 0:
        area = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(area)
        M = cv2.moments(area)
        center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))

        if radius > 10:
            cv2.circle(img, (int(x), int(y)), int(radius),
                       (0, 255, 255), 2)
            cv2.circle(img, center, 5, (0, 0, 255), -1)
            
            if with_motion:
                momentum = 0.005
                center_x = 320
                
                if x > center_x:
                    move_left((x - center_x) * momentum)
                    print('left ' + str(x - center_x))
                else:
                    move_right((center_x - x) * momentum)
                    print('left ' + str(center_x - x))

    cv2.imshow('Ball tracking', img)
    cap.truncate(0)

    if cv2.waitKey(1) == 27:
        break

truncate_pwm()
cap.release()
cv2.destroyAllWindows()
