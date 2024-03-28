from utilDescribeVideo import *
import os
# 


initModel()
videoPath = "demos/video1.0.mp4"
desc = describeVideo(videoPath)

print(desc)