import cv2
import os
from numpy import imag
import ffmpeg
import platform
from moviepy.editor import *

print('------ Path To Your Input File Name ------', sep='')
INPUT = input()
print('------ Path To Output File Name ------', sep='')
OUTPUT = input()
print('------ UpScale Rate(2/4) ------', sep='')
SCALE = int(input())
print('------ Model(1 - RealESRGAN, 2 - waifu2x, 3 - RealCUGAN) ------', sep='')
MODEL = int(input())

# check inputs

if INPUT == '':
    INPUT='input.mp4'
    
if OUTPUT == '':
    OUTPUT='out.mp4'

if MODEL not in [1,2,3]:
    MODEL=2

if SCALE not in [2,4]:
    SCALE=2

OS = platform.system()

vidcap = cv2.VideoCapture(INPUT)
FPS = vidcap.get(cv2.CAP_PROP_FPS)

os.system('mkdir input_images')
os.system('mkdir output')

success, image = vidcap.read()
last = image

count = 0
while success:
    cv2.imwrite("input_images/frame_%d.jpg" % count, image)
    k = (image-last).sum()/(image.sum()+last.sum())
    if k>=0.0001 or count == 0:
        if(MODEL == 1):
            os.system(f'realesrgan-ncnn-vulkan -i ./input_images/frame_{count}.jpg -o ./output/frame_out_{count}.jpg -s {SCALE}')
        if(MODEL == 2):
            os.system(f'waifu2x-ncnn-vulkan -i ./input_images/frame_{count}.jpg -o ./output/frame_out_{count}.jpg -s {SCALE}')
        if(MODEL == 3):
            os.system(f'realcugan-ncnn-vulkan -i ./input_images/frame_{count}.jpg -o ./output/frame_out_{count}.jpg -s {SCALE}')
    else:
        os.system(f'cp ./output/frame_out_{count-1}.jpg ./output/frame_out_{count}.jpg')
    print('Saved and decoded image ', count)
    last=image
    success, image = vidcap.read()
    count += 1


input = ffmpeg.input('./output/frame_out_%d.jpg').filter('fps',fps=FPS).output('out_temp.mp4')
input.run()
video = VideoFileClip('out_temp.mp4',audio=True)
video.set_audio(VideoFileClip(INPUT).audio).write_videofile(OUTPUT,fps=FPS, audio_codec="aac")

if OS != 'Windows':
    os.system('rm -r input_images')
    os.system('rm -r output')
    os.system('rm out_temp.mp4')
else:
    os.system('rd -r input_images')
    os.system('rd -r output')
    os.system('rd out_temp.mp4')