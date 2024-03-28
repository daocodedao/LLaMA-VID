from utilDescribeVideo import *
import os
from utils.logger_settings import api_logger


initModel()
videoPath = "demos/video1.0.mp4"
desc = describeVideo(videoPath)
api_logger.info("视频描述：")
api_logger.info(desc)