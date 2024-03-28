from utilDescribeVideo import *
import os
# 
# os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"   # see issue #152
# os.environ["CUDA_VISIBLE_DEVICES"]="1"

initModel()
videoPath = "demos/video1.0.mp4"
desc = describeVideo(videoPath)

print(desc)