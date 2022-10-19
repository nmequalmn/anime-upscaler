import cv2
import os
from numpy import imag
import ffmpeg
import platform
from moviepy.editor import *

FPS = 25
INPUT = 'input.mov'
OUTPUT = 'output.mp4'
SCALE = 2

vidcap = cv2.VideoCapture(INPUT)

os.system('mkdir input_images')
os.system('mkdir output')

success, image = vidcap.read()
last = image

count = 0
while success:
    cv2.imwrite("input_images/frame_%d.jpg" % count, image)
    k = (image-last).sum()/(image.sum()+last.sum())
    if k>=0.00001 or count == 0:
        os.system(f'./realesrgan-ncnn-vulkanss -i ./input_images/frame_{count}.jpg -o ./output/frame_out_{count}.jpg -s {SCALE}')
    else:
        os.system(f'cp ./output/frame_out_{count-1}.jpg ./output/frame_out_{count}.jpg')
    print('Saved and decoded image ', count)
    last=image
    success, image = vidcap.read()
    count += 1


input = ffmpeg.input('./output/frame_out_%d.jpg').filter('fps',fps=FPS).output('out_temp.mp4')
input.run()
os.system('rm -r input_images')
os.system('rm -r output')
video = VideoFileClip('out_temp.mp4',audio=True)
video.set_audio(VideoFileClip(INPUT).audio).write_videofile(OUTPUT,fps=FPS, audio_codec="aac")
os.system('rm out_temp.mp4')