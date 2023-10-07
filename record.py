import cv2
import os
import time

cam = cv2.VideoCapture(2)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cam.set(cv2.CAP_PROP_AUTOFOCUS, 1) # turn the autofocus off
print(cam.get(cv2.CAP_PROP_FOCUS))
# cam.set(cv2.CAP_PROP_FOCUS, 60) # turn the autofocus off
cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
cam.set(cv2.CAP_PROP_EXPOSURE, -6) 

cv2.namedWindow("stop_motion: record")

img_counter = 0

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("stop_motion: record", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        epoch_ms = int(time.time()*1000.0)
        img_name = "opencv_frame_{}.png".format(epoch_ms)
        img_path = os.path.join('recordings/latest', img_name)
        cv2.imwrite(img_path, frame)
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()

cv2.destroyAllWindows()

