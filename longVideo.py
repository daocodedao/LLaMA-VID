

from pydantic import BaseModel
import os,time,datetime
import cv2
from pathlib import Path
import shutil

class ShortVideo(BaseModel):
    name:str
    duration:float
    startTime:float
    endTime:float
    desc:str
    path:str


class LongVideo(BaseModel):
    id:str
    name:str
    dir:str
    fileName:str
    isHorizontal:bool=True
    width:int = 0
    height:int = 0
    duration:float = 0
    subVideoDir:str
    shortVideos:list[ShortVideo] = []
    desc:str

    def __init__(self, videoPath, videoId=None):
        if not os.path.exists(videoPath):
            return 

        self.name = Path(videoPath).stem
        videoName = os.path.basename(videoPath)
        self.updateVideoInfo()
        if videoId is None:
            timestamp = int(datetime.datetime.now().timestamp())
            self.id = str(timestamp)
        else:
            self.id = videoId
        self.dir = f"/data/work/longvideo/{videoId}/"
        self.subVideoDir = os.path.join(self.dir, 'subVideos')
        os.makedirs(self.subVideoDir, exist_ok=True)

        outVideoPath = os.path.join(self.dir, videoName)
        if not os.path.exists(outVideoPath):
            shutil.copyfile(videoPath, outVideoPath)

    def getVideoPath(self):
        return os.path.join(self.dir, self.fileName)


    def updateVideoInfo(self):
        videoPath = self.getVideoPath()
        video = cv2.VideoCapture(videoPath)
        self.duration = video.get(cv2.CAP_PROP_POS_MSEC)
        self.width  = video.get(cv2.CAP_PROP_FRAME_WIDTH)   # float `width`
        self.height = video.get(cv2.CAP_PROP_FRAME_WIDTH)  # float `height`
        if self.width > self.height:
            self.isHorizontal = True
        else:
            self.isHorizontal = False

        print(f"{self.name} duration: {self.duration}, width: {self.width}, height: {self.height}, isHorizontal: {self.isHorizontal}")



