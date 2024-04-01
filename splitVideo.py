import cv2
import os
from pathlib import Path

import cv2
from datetime import datetime, time
from splitting.splitHelp import *
from utils.logger_settings import api_logger
from utils.util import Util
from longVideo import LongVideo, ShortVideo
import shutil
from utils.mediaUtil import MediaUtil
from utilDescribeVideo import *
import requests


def reqVideoDesc(videoPath):
    url = 'http://39.105.194.16:9690/video/describe'

    file = {'file': open(videoPath, 'rb')}
    resp = requests.post(url=url, files=file) 
    result = resp.json()
    # api_logger.info("视频描述：")
    # print(resp.json())
    print(result['message'])
    return result['message']

srcVideoPath="./splitting/input_videos/video1.mp4"
video_name = Path(srcVideoPath).stem
videoId = Util.getCurTimeStampStr()
cutscenes_raw = cutscene_detection(srcVideoPath, cutscene_threshold=25, max_cutscene_len=5)
        
longVideo = LongVideo()
longVideo.updateVideoInfo(videoId=videoId, videoPath=srcVideoPath)
api_logger.info(f"long video info: {longVideo}")

device = "cuda"
api_logger.info("loading model")
model = imagebind_model.imagebind_huge(pretrained=True)
model.eval()
model.to(device)


video_events = {}
# for srcVideoPath in tqdm(srcVideoPaths):
cap = cv2.VideoCapture(srcVideoPath)
fps = cap.get(cv2.CAP_PROP_FPS)
# cutscene = video_cutscenes[srcVideoPath.split("/")[-1]]
cutscene = cutscenes_raw

api_logger.info("prepare extract_cutscene_feature")
cutscene_raw_feature, cutscene_raw_status = extract_cutscene_feature(srcVideoPath, cutscene, model, device)

cutscenes, cutscene_feature = verify_cutscene(cutscene, cutscene_raw_feature, cutscene_raw_status, transition_threshold=1.)
events_raw, event_feature_raw = cutscene_stitching(cutscenes, cutscene_feature, eventcut_threshold=0.6)

events, event_feature = verify_event(events_raw, event_feature_raw, fps, min_event_len=2.0, max_event_len=1200, redundant_event_threshold=0.0, trim_begin_last_percent=0.0, still_event_threshold=0.15)

video_event = transfer_timecode(events, fps)
timecodes = video_event

shutil.rmtree(longVideo.subVideoDir, ignore_errors=True)
os.makedirs(longVideo.subVideoDir)
longVideo.shortVideos = []

for i, timecode in enumerate(timecodes): 
    subVideo = ShortVideo()
    start_time = datetime.strptime(timecode[0], '%H:%M:%S.%f')
    end_time = datetime.strptime(timecode[1], '%H:%M:%S.%f')
    video_duration = (end_time - start_time).total_seconds()
    subVideo.name = f"{video_name}.{i}.mp4"
    outVideoPath = os.path.join(longVideo.subVideoDir, subVideo.name)
    subVideo.path =outVideoPath
    subVideo.duration = video_duration
    print(f"startTime = {timecode[0]} endTime = {timecode[1]}")
    subVideo.startTime = MediaUtil.time_to_seconds(timecode[0])
    subVideo.endTime = MediaUtil.time_to_seconds(timecode[1])
    
    os.makedirs(os.path.dirname(outVideoPath), exist_ok=True)
    cmd = "ffmpeg -y -hide_banner -loglevel panic -ss %s -t %.3f -i %s %s"%(timecode[0], video_duration, srcVideoPath, outVideoPath)
    api_logger.info(f"cmd: {cmd}")
    os.system(cmd)

    # api_logger.info(subVideo)
    # desc = describeVideo(outVideoPath)
    subVideo.desc = reqVideoDesc(outVideoPath)

    longVideo.shortVideos.append(subVideo)


api_logger.info(longVideo)