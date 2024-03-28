

from utils.curl import Curl
from utils.util import Util


class NotifyUtil:
    @staticmethod
    def notifyFeishu(msg:str):
        notifyUrl = "https://open.feishu.cn/open-apis/bot/v2/hook/fd9ab87b-ec49-40e6-a401-58899c08a944"
        para = {
            "msg_type":"text",
            "content":{
                "text":msg
            }
        }
        codeResponse = Curl.Request(notifyUrl, Util.JsonEncode(para), 'POST', {})




