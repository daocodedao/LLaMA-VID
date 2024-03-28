from utilDescribeVideo import *

os.environ["CUDA_VISIBLE_DEVICES"] = "1"


initModel()
videoPath = "demos/video1.0.mp4"
desc = describeVideo(videoPath)

print(desc)