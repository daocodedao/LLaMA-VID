
import requests
from utils.util import Util

# filePath = Util.getTempMp4FilePath()
videoPath = "./demos/video1.0.mp4"

url = 'http://localhost:9890/video/describe'
file = {'file': open(videoPath, 'rb')}
resp = requests.post(url=url, files=file) 
print(resp.json())

exit()
