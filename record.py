import cv2

cam = cv2.VideoCapture(2)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cam.set(cv2.CAP_PROP_AUTOFOCUS, 1) # turn the autofocus off
print(cam.get(cv2.CAP_PROP_FOCUS))
# cam.set(cv2.CAP_PROP_FOCUS, 60) # turn the autofocus off
cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
cam.set(cv2.CAP_PROP_EXPOSURE, -6) 

cv2.namedWindow("test")

img_counter = 8

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("test", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()

cv2.destroyAllWindows()

