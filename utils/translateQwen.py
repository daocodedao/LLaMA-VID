
import requests
import socket

import json
from utils.logger_settings import api_logger

def getNetworkIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.connect(('<broadcast>', 0))
    return s.getsockname()[0]

serverUrl = "http://39.105.194.16:9191/v1/chat/completions/"
# localIp = getNetworkIp()
# print(f"localIp:{localIp}")
# if "192.168.0" in localIp:
#     serverUrl = "http://192.168.0.67:9191/v1/chat/completions/"


def replaceSpecialWordEnToZh(srcStr:str = None):
    if srcStr is None:
        return ""
    # 读取JSON文件
    with open("./utils/trans-en-zh-dic.json", "r") as file:
        wordList = json.load(file)
        for word in wordList:
            if word["en"] in srcStr:
                srcStr = srcStr.replace(word["en"], word["zh-cn"])

    return srcStr

def translate_en_to_zh(inSrc):
    # url = "http://39.105.194.16:9191/v1/chat/completions/"  # 替换为您要发送请求的URL
    data = {
            "systemRole": "system",
            "systemContent": "You are a helpful assistant.",
            "userRole":"role",
            "userContent":"Trump was always bothered by how Trump Tower fell 41 feet short of the General Motors building two blocks north."
    }

    systemContent = f"你是翻译助手，将后续的内容翻译成中文"

    # data["systemContent"] = systemContent
    data["systemContent"] = systemContent
    data["userContent"] = inSrc

    response = requests.post(serverUrl, json=data, timeout=50)

    if response.status_code == 200:
        # api_logger.info("请求成功")
        retJson = response.json()
        # api_logger.info(retJson)
        ret_text = retJson["message"]
        ret_text = replaceSpecialWordEnToZh(ret_text)
        return ret_text
    else:
        # api_logger.info("请求失败，状态码：", response.status_code)
        # api_logger.info(response.text)
        return ""

def translate_srt_en_to_zh(inSrc, inNewTransLate=True):
    # url = "http://39.105.194.16:9191/v1/chat/completions/"  # 替换为您要发送请求的URL
    data = {
            "systemRole": "system",
            "systemContent": "You are a helpful assistant.",
            "userRole":"role",
            "userContent":"Trump was always bothered by how Trump Tower fell 41 feet short of the General Motors building two blocks north."
    }

    systemContent = f"你是字幕翻译助手，将后续的文字块里的英文翻译成中文，每次翻译都是全新的内容，不用参考之前的内容。输入的文字每3行是一个文字块，第1行是次序行，第2行是时间行，第3行是需要翻译的英文内容。\n输出格式要求：\n1.次序行和时间行必须和输入保持内容一致，行数一致\n2.只有第3行需要翻译，第3行是翻译出的内容\n3.不要输出额外的解释的内容，不要输出备注内容，不要输出额外内容。\n4.如果文字块内容无法翻译，则直接跳过整个文字块，输出是不显示该文字块，继续下一个文字块\n5.翻译要口语化 \n\n\n输入内容参考：\n1\n0:00:00.000 --> 0:00:05.020\nHave you ever wondered who is behind the financing of Saudi Arabia's crazy mega projects?\n2\n0:00:05.380 --> 0:00:09.060\nIt is the richest family in the world, and you've never even heard of them.\n3\n0:00:09.180 --> 0:00:14.640\nThey have gold toilets, gold Lamborghinis, and even purchased the world's most expensive house,\n  输出内容参考：\n1\n0:00:00.000 --> 0:00:05.020\n你有没有想过沙特阿拉伯那些疯狂大项目背后的资助者是谁？\n2\n0:00:05.380 --> 0:00:09.060\n答案是全球最富有的家族，但他们鲜为人知。\n3\n0:00:09.180 --> 0:00:14.640\n他们有镀金马桶、定制的黄金兰博基尼，甚至买下了世上最贵的房子,\n"


    # data["systemContent"] = systemContent
    data["systemContent"] = systemContent
    data["userContent"] = inSrc

    response = requests.post(serverUrl, json=data, timeout=50)

    if response.status_code == 200:
        # api_logger.info("请求成功")
        retJson = response.json()
        # api_logger.info(retJson)
        ret_text = retJson["message"]
        ret_text = replaceSpecialWordEnToZh(ret_text)
        return ret_text
    else:
        api_logger.error("请求失败，状态码：", response.status_code)
        api_logger.error(response.text)
        return ""


def videoFramsTextCombine(txtList):
    data = {
            "systemRole": "system",
            "systemContent": "You are a helpful assistant.",
            "userRole":"role",
            "userContent":"Trump was always bothered by how Trump Tower fell 41 feet short of the General Motors building two blocks north."
    }

    systemContent = f"我将会对视频抽帧，每一帧都会有一段文字描述。你需要将这些描述整合成一个完整的视频的描述。\n"

    inSrc = "\n".join(txtList)

    # data["systemContent"] = systemContent
    data["systemContent"] = systemContent
    data["userContent"] = inSrc

    response = requests.post(serverUrl, json=data, timeout=50)

    if response.status_code == 200:
        # api_logger.info("请求成功")
        retJson = response.json()
        # api_logger.info(retJson)
        ret_text = retJson["message"]
        return ret_text
    else:
        api_logger.error("请求失败，状态码：", response.status_code)
        api_logger.error(response.text)
        return ""
