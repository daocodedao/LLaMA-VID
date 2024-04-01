

from pydantic import BaseModel
import os,time,datetime
import cv2
from pathlib import Path
import shutil

class ShortVideo(BaseModel):
    name:str = None
    duration:float = 0
    startTime:float = 0
    endTime:float = 0
    desc:str = ""
    path:str = None


class LongVideo(BaseModel):
    id:str = None
    name:str = None
    videoPath:str = None
    isHorizontal:bool=True
    width:int = 0
    height:int = 0
    duration:float = 0
    subVideoDir:str = ""
    shortVideos:list[ShortVideo] = []
    desc:str = ""

    def updateVideoInfo(self, videoPath, videoId=None):
        if not os.path.exists(videoPath):
            return 
        # self.videoPath = videoPath
        self.name = Path(videoPath).stem
        videoName = os.path.basename(videoPath)
        self.completeVideoInfo()
        if videoId is None:
            timestamp = int(datetime.datetime.now().timestamp())
            self.id = str(timestamp)
        else:
            self.id = videoId
        videoDir = f"/data/work/longvideo/{videoId}/"
        self.subVideoDir = os.path.join(videoDir, 'subVideos')
        os.makedirs(self.subVideoDir, exist_ok=True)
        outVideoPath = os.path.join(videoDir, videoName)
        if not os.path.exists(outVideoPath):
            shutil.copyfile(self.videoPath, outVideoPath)
            self.videoPath = outVideoPath

    def completeVideoInfo(self):
        video = cv2.VideoCapture(self.videoPath)
        self.duration = video.get(cv2.CAP_PROP_POS_MSEC)
        self.width  = video.get(cv2.CAP_PROP_FRAME_WIDTH)   # float `width`
        self.height = video.get(cv2.CAP_PROP_FRAME_WIDTH)  # float `height`
        if self.width > self.height:
            self.isHorizontal = True
        else:
            self.isHorizontal = False




