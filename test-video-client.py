
import requests


# curl -X POST http://localhost:9890/uploadfile/ -F "file=@my_video.mp4"


url = "http://192.168.0.65:9890/video/describe/"
videoPath = "./demos/video1.0.mp4"
files = {'upload_file': open(videoPath,'rb')}

r = requests.post(url, files=files)

print("返回结果")
print(r)