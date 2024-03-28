
from utils.logger_settings import api_logger
import time,datetime,json,os
import random
import subprocess
import av
from PIL import Image
import cv2
from moviepy.editor import *
import srt

# 常用工具
class MediaUtil:

    def getVideoPathsFromDir(fromDir):
        videoList = [os.path.join(fromDir, f) for f in os.listdir(fromDir) if f.endswith(".mp4")]
        return videoList

    def getRandomMp3FilePath(fromDir):
        mp3_files = [f for f in os.listdir(fromDir) if f.endswith(".mp3")]
        if not mp3_files:
            api_logger.info("No mp3 files found in the folder.")
            return ""
        else:
            random_mp3_file = random.choice(mp3_files)
            random_mp3_path = os.path.join(fromDir, random_mp3_file)
            api_logger.info(f"Random mp3 file: {random_mp3_path}")
            return random_mp3_path
    
    def getMediaDuration(filePath):
      try:
          cmd=f"ffprobe -i {filePath} -show_entries format=duration -v quiet -of csv=\"p=0\""
          result = subprocess.check_output(cmd, shell=True)
          durationFloat = float(result)
          return durationFloat
      except Exception as e:
          return 0

    def getRandomTransitionEffect():
      effects = ["DISSOLVE", "RADIAL", "CIRCLEOPEN", "CIRCLECLOSE", "PIXELIZE", "HLSLICE", 
              "HRSLICE", "VUSLICE", "VDSLICE", "HBLUR", "FADEGRAYS", "FADEBLACK", "FADEWHITE","RECTCROP",
              "CIRCLECROP", "WIPELEFT", "WIPERIGHT", "SLIDEDOWN", "SLIDEUP", "SLIDELEFT", "SLIDERIGHT"]
      return random.choice(effects).lower()
  
    def read_frames(video_path):
        container = av.open(video_path)

        video_stream = next(s for s in container.streams if s.type == "video")
        frames = []
        for packet in container.demux(video_stream):
            for frame in packet.decode():
                image = Image.frombytes(
                    "RGB",
                    (frame.width, frame.height),
                    frame.to_rgb().to_ndarray(),
                )
                frames.append(image)

        return frames
    
    def extract_video_to_frames(video_path, outDir):
        vidcap = cv2.VideoCapture(video_path)
        success,image = vidcap.read()
        count = 0
        framePaths = []
        while success:
            framePath = os.path.join(outDir, f"{count}.jpg")
            cv2.imwrite(framePath, image)     # save frame as JPEG file      
            framePaths.append(framePath)
            success,image = vidcap.read()
            # print('Read a new frame: ', success)
            count += 1

            return framePaths
        
    def get_image_paths_from_folder(folder_path):
        image_extensions = [".jpg", ".jpeg", ".png", ".bmp"]
        image_paths = []

        for root, dirs, files in os.walk(folder_path):
            for file in files:
                for ext in image_extensions:
                    if file.endswith(ext):
                        image_path = os.path.join(root, file)
                        image_paths.append(image_path)

        image_paths.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
        return image_paths
    
    def get_fps(video_path):
        container = av.open(video_path)
        video_stream = next(s for s in container.streams if s.type == "video")
        fps = video_stream.average_rate
        container.close()
        return fps
  
    def changeVideoFps(filePath, fps=30, outFilePath=None):
        # print(f"now fps = {int(get_fps(filePath))}")
        clip = VideoFileClip(filePath)
        if outFilePath is None:
            outFilePath = filePath

        clip.write_videofile(outFilePath, fps=fps)
        # print(f"now fps = {int(get_fps(outFilePath))}")


    def create_video(frames, fps, savePath):
        clip = ImageSequenceClip(frames, fps=fps)
        clip.write_videofile(savePath, fps=fps, verbose=False)


    def create_ffmpeg_cmd(deleteRange, input_file, output_file):
        segments = []
        last_end = 0.0  # Start of video

        for start, end in deleteRange:
            segments.append((last_end, start))
            last_end = end

        segments.append((last_end, None))  # End of video

        filter_parts = []
        for idx, (start, end) in enumerate(segments):
            if end is None:
                video_segment = f"[0:v]trim=start={start},setpts=PTS-STARTPTS[v{idx}];"
                audio_segment = f"[0:a]atrim=start={start},asetpts=PTS-STARTPTS[a{idx}];"
            else:
                video_segment = f"[0:v]trim=start={start}:end={end},setpts=PTS-STARTPTS[v{idx}];"
                audio_segment = f"[0:a]atrim=start={start}:end={end},asetpts=PTS-STARTPTS[a{idx}];"
            filter_parts.extend([video_segment, audio_segment])

        filter_concat = "".join(filter_parts)
        filter_concat += "".join([f"[v{i}][a{i}]" for i in range(len(segments))])
        filter_concat += f"concat=n={len(segments)}:v=1:a=1[outv][outa]"

        cmd = f"ffmpeg -y -i {input_file} -filter_complex \"{filter_concat}\" -map \"[outv]\" -map \"[outa]\" {output_file}"
        return cmd


    def getNoHumanParts(srtPath, cutThreshold=2):
        # deleteRange = [(40.12/1000, 46.583/1000), (51.312/1000, 53.229/1000), (128.055/1000, 130.536/1000)]

        noHumanParts = []
        subList = []
        with open(srtPath, 'r') as srcFile:
            # 读取文件内容
            content = srcFile.read()
            subs = srt.parse(content)
            subList = list(subs)

            for index, sub in enumerate(subList):
                if index + 1 >= len(subList):
                    break
                
                sub = subList[index]
                nextSub = subList[index + 1]

                timeDiff = nextSub.start.total_seconds() - sub.end.total_seconds()
                api_logger.info(f"下个字幕{index + 1}时间-当前字幕{index}时间:{timeDiff} ")
                if timeDiff > cutThreshold:
                    noHumanParts.append((sub.end.total_seconds(), nextSub.start.total_seconds()))
        return noHumanParts