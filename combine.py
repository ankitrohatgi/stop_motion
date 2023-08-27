import cv2
import os
import tqdm

img_path = "blocks2/"
out_file = "blocks2.mp4"
img_end = 216
img_start = 0
fps = 3

def get_image_name(index):
    return os.path.join(img_path, "opencv_frame_{}.png".format(index))


# open 1st image for width and height
img1 = cv2.imread(get_image_name(img_start))
height,width,layers=img1.shape
print(width,height)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video=cv2.VideoWriter(out_file,fourcc,fps,(width,height))

for i in tqdm.tqdm(range(img_start, img_end)):
    img = cv2.imread(get_image_name(i))
    video.write(img)

video.release()
print("done!")
