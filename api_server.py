
from fastapi import FastAPI
from utils.logger_settings import api_logger
from typing import Dict, Generator, List, Optional, Union




app = FastAPI()
@app.post("/translate/en-cn/")
# 添加图书
def translate_en_cn(item:TranslateItem):
    global model, tokenizer
    # api_logger.info(f"准备开始翻译, 收到的参数：{item}")
    retStr = ""
    try:
        # api_logger.info(f"准备翻译:{item}")
        tokenizer.src_lang = item.srcLang
        # 有bug， Force 开头的不翻译
        waitTrans = item.description.replace("Force ", "force ")
        encoded_zh = tokenizer(waitTrans, return_tensors="pt").to('cuda')
        generated_tokens = model.generate(**encoded_zh, forced_bos_token_id=tokenizer.lang_code_to_id[item.dstLang])
        results = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
        print(results)
        if len(results) > 0:
            retStr = results[0]
    except IOError as e:
        api_logger.error(f"An error occurred while processing the file: {e}")
        return{"code":400, "message":f"翻译添加异常：{e}"}
    # finally:
        # api_logger.info("翻译完成！")

    return {"code":200, "message":retStr}   



@app.get("/live/")
def live():
    return {"code":200, "message":"living"}   
