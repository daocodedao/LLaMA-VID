# from utilDescribeVideo import *
import os,datetime
from utils.logger_settings import api_logger
from utils.mediaUtil import MediaUtil
from datetime import datetime, time


time1 = "0:00:00.000"

# start_time = datetime.strptime(time1, '%H:%M:%S.%f')
# res = datetime.strptime(time1, '%S.%f')

# start_time = datetime.strptime(time1, '%H:%M:%S.%f')


res = MediaUtil.time_to_seconds(time1)

time1 = "0:00:15.982"
res = MediaUtil.time_to_seconds(time1)

print(res)

# initModel()
# videoPath = "demos/video1.0.mp4"
# desc = describeVideo(videoPath)
# api_logger.info("视频描述：")
# api_logger.info(desc)