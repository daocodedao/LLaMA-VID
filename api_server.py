
from fastapi import FastAPI, UploadFile, File
from utils.logger_settings import api_logger

from utilDescribeVideo import initModel, describeVideo
from utils.util import Util
import os
import shutil




api_logger.info("加载模型")
initModel()
api_logger.info("加载模型-完毕")

app = FastAPI()
@app.post("/video/describe")
def upload_file(file: UploadFile = File(...)):
    api_logger.info(f"/video/describe 收到文件 {file.filename}")
    saveVideoPath = Util.getTempMp4FilePath()
    api_logger.info(f"保存文件到 {saveVideoPath}")

    try:
        contents = file.file.read()
        with open(saveVideoPath, 'wb') as f:
            f.write(contents)
    except Exception as e:
        api_logger.error(e)
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    desc = "成功"
    desc = describeVideo(saveVideoPath)
    api_logger.info(f"视频描述：{desc}")
    api_logger.info(f"准备删除视频文件：{saveVideoPath}")
    os.remove(saveVideoPath)
    return {"code":200, "message":desc}   


@app.get("/live/")
def live():
    return {"code":200, "message":"living"}   


@app.post("/upload")
def upload(file: UploadFile = File(...)):
    api_logger.info(f"/upload 收到文件 {file.filename}")
    try:
        with open(file.filename, 'wb') as f:
            shutil.copyfileobj(file.file, f)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()
        
    return {"message": f"Successfully uploaded {file.filename}"}