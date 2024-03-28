
import requests


# curl -X POST http://192.168.0.65:9890/video/describe/ -F "file=demos/video1.0.mp4"


url = "http://localhost:9890/video/describe/"
# url = "http://127.0.0.1/video/describe/"
videoPath = "./demos/video1.0.mp4"
files = {'upload_file': open(videoPath,'rb')}

response = requests.post(url, files=files)
retJson = response.json()
# ret_text = retJson["message"]

print("返回结果")
print(retJson)
# print(ret_text)