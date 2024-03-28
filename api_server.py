
from fastapi import FastAPI, UploadFile, File
from utils.logger_settings import api_logger

from utilDescribeVideo import initModel, describeVideo
from utils.util import Util
import os
import shutil




# api_logger.info("加载模型")
# initModel()
# api_logger.info("加载模型-完毕")

app = FastAPI()
@app.post("/video/describe/")
async def upload_file(file: UploadFile = File(...)):
    saveVideoName = f"{Util.getCurTimeStampStr()}.mp4"
    videoPath = os.path.join("/tmp/", saveVideoName)

    try:
        api_logger.info(f"收到文件：{file.filename}")
        contents = file.file.read()
        with open(videoPath, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()


    # if not file.endswith(".mp4"):
    #     return {"code":201, "message":"Need upload video file"} 
    # api_logger.info(f"收到文件：{file.filename}")

    # with open(videoPath, "wb") as f:
    #     f.write(file.file.read())
    desc = "成功"
    # desc = describeVideo(videoPath)
    api_logger.info(f"视频描述：{file.filename}")
    api_logger.info(f"准备删除视频文件：{videoPath}")
    os.remove(videoPath)
    return {"code":200, "message":desc}   


@app.get("/live/")
def live():
    return {"code":200, "message":"living"}   


@app.post("/upload")
def upload(file: UploadFile = File(...)):
    try:
        with open(file.filename, 'wb') as f:
            shutil.copyfileobj(file.file, f)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()
        
    return {"message": f"Successfully uploaded {file.filename}"}