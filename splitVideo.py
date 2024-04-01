import cv2
import os
from pathlib import Path

import cv2
from datetime import datetime
from splitting.splitHelp import *
from utils.logger_settings import api_logger

srcVideoPath="./splitting/input_videos/video1.mp4"
video_name = Path(srcVideoPath).stem
output_folder = f"output/{video_name}"
cutscenes_raw = cutscene_detection(srcVideoPath, cutscene_threshold=25, max_cutscene_len=5)
        

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
for i, timecode in enumerate(timecodes): 
    start_time = datetime.strptime(timecode[0], '%H:%M:%S.%f')
    end_time = datetime.strptime(timecode[1], '%H:%M:%S.%f')
    video_duration = (end_time - start_time).total_seconds()
    outVideoPath = os.path.join(output_folder, video_name+".%i.mp4"%i)
    api_logger.info(f"inputPath: {srcVideoPath}")
    api_logger.info(f"outputPath: {outVideoPath}")
    api_logger.info(f"timecode: {timecode[0]}")
    api_logger.info(f"video_duration: {video_duration}")
    cmd = "ffmpeg -hide_banner -loglevel panic -ss %s -t %.3f -i %s %s"%(timecode[0], video_duration, srcVideoPath, outVideoPath)
    api_logger.info(f"cmd: {cmd}")
    os.system(cmd)
