
from fastapi import FastAPI, UploadFile, File
from utils.logger_settings import api_logger

from utilDescribeVideo import initModel, describeVideo
from utils.util import Util
import os

api_logger.info("加载模型")
initModel()
api_logger.info("加载模型-完毕")

app = FastAPI()
@app.post("/video/describe/")
async def upload_file(file: UploadFile = File(...)):
    if not file.endswith(".mp4"):
        return {"code":201, "message":"Need upload video file"} 
    api_logger.info(f"收到文件：{file.filename}")
    saveVideoName = f"{Util.getCurTimeStampStr()}.mp4"
    videoPath = os.path.join("/tmp/", saveVideoName)
    with open(videoPath, "wb") as f:
        f.write(file.file.read())

    desc = describeVideo(videoPath)
    api_logger.info(f"视频描述：{file.filename}")
    return {"code":200, "message":desc}   



@app.get("/live/")
def live():
    return {"code":200, "message":"living"}   
