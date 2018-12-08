from pipeline import pipeline, process_image
from moviepy.editor import VideoFileClip
import os 


def detect_lane_line_image(img_addrs):
    for img_addr in img_addrs:
        pipeline(os.path.join('CarND-LaneLines-P1/test_images', img_addr), os.path.abspath('CarND-LaneLines-P1/test_images_output'))

def detect_lane_line_video(video_addrs):
    for video_addr in video_addrs:
        if video_addr.endswith(".mp4"):
            clip1 = VideoFileClip(os.path.join('CarND-LaneLines-P1/test_videos/', video_addr))
            white_clip = clip1.fl_image(process_image) #NOTE: this function expects color images!!
            white_clip.write_videofile(os.path.join('CarND-LaneLines-P1/test_videos_output', os.path.basename(video_addr)), audio=False)

img_addrs = os.listdir("CarND-LaneLines-P1/test_images/")
video_addrs = os.listdir("CarND-LaneLines-P1/test_videos/")

detect_lane_line_image(img_addrs)
detect_lane_line_video(video_addrs)