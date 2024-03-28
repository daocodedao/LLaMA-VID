
import requests


url = "http://localhost:9890/video/describe/"
videoPath = "./demos/video1.0.mp4"
files = {'upload_file': open(videoPath,'rb')}

r = requests.post(url, files=files)

print("返回结果")
print(r)