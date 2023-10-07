import cv2
import os
import tqdm

img_path = "recordings/latest/"
out_file = "recordings/videos/the_star_wars_movie.avi"
img_start = 0
img_end = 409
fps = 5

def get_image_name(index):
    return os.path.join(img_path, "opencv_frame_{}.png".format(index))


# open 1st image for width and height
img1 = cv2.imread(get_image_name(img_start))
height,width,layers=img1.shape
print(width,height)

fourcc = cv2.VideoWriter_fourcc(*'MJPG')
video=cv2.VideoWriter(out_file,fourcc,fps,(width,height))

for i in tqdm.tqdm(range(img_start, img_end)):
    img = cv2.imread(get_image_name(i))
    video.write(img)

video.release()
print("done!")
