from utilDescribeVideo import *



initModel()
videoPath = "demos/video1.0.mp4"
desc = describeVideo(videoPath)

print(desc)