
import requests
from utils.util import Util

# filePath = Util.getTempMp4FilePath()
videoPath = "./demos/video1.0.mp4"

url = 'http://39.105.194.16:9690/video/describe'
# url = 'http://localhost:9690/video/describe'

file = {'file': open(videoPath, 'rb')}
resp = requests.post(url=url, files=file) 
result = resp.json()

print(resp.json())
print(result['message'])


