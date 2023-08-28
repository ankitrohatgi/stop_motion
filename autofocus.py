import cv2
import os

cam = cv2.VideoCapture(2)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cam.set(cv2.CAP_PROP_AUTOFOCUS, 1) # turn the autofocus on
# cam.set(cv2.CAP_PROP_FOCUS, 60) # turn the autofocus off
#cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
#cam.set(cv2.CAP_PROP_EXPOSURE, -6) 

cv2.namedWindow("stop_motion: autofocus")


while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("stop_motion: autofocus", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        print(cam.get(cv2.CAP_PROP_FOCUS))

cam.release()
cv2.destroyAllWindows()

