
import os
from utils.logger_settings import api_logger

os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"   # see issue #152
os.environ["CUDA_VISIBLE_DEVICES"]="1"
api_logger.info(f"Using GPU is CUDA:{os.environ['CUDA_VISIBLE_DEVICES']}")



from decord import VideoReader, cpu
from llava.utils import disable_torch_init
from llamavid.model.builder import load_pretrained_model
from llava.mm_utils import tokenizer_image_token, get_model_name_from_path, KeywordsStoppingCriteria
from llamavid.conversation import conv_templates, SeparatorStyle
from llamavid.constants import IMAGE_TOKEN_INDEX, DEFAULT_IMAGE_TOKEN, DEFAULT_IM_START_TOKEN, DEFAULT_IM_END_TOKEN
from transformers import TextStreamer
import torch

gVideoTokenizer = None
gVideoModel = None
gVideoProcessor = None
gConvMode = None



def load_video(video_path, fps=1):
    vr = VideoReader(video_path, ctx=cpu(0))
    fps = round(vr.get_avg_fps()/fps)
    frame_idx = [i for i in range(0, len(vr), fps)]
    spare_frames = vr.get_batch(frame_idx).asnumpy()
    return spare_frames

def initModel():
    # Model
    global gVideoTokenizer,gVideoModel,gVideoProcessor,gConvMode

    model_path="model_zoo/llama-vid-7b-full-224-video-fps-1"
    model_base=None
    model_name = get_model_name_from_path(model_path)
    load_8bit = True
    load_4bit = False
    conv_mode = None

    disable_torch_init()

    # device="cuda:0"
    # if torch.cuda.device_count() > 1:
    #     device = "cuda:1"

    gVideoTokenizer, gVideoModel, gVideoProcessor, context_len = load_pretrained_model(model_path, 
                                                                                       model_base, 
                                                                                       model_name, 
                                                                                       load_8bit=load_8bit, 
                                                                                       load_4bit=load_4bit,
                                                                                    #    device_map=None,
                                                                                    #    device=device
                                                                                       )

    if 'llama-2' in model_name.lower():
        conv_mode = "llava_llama_2"
    elif "v1" in model_name.lower() or "vid" in model_name.lower():
        conv_mode = "llava_v1"
    elif "mpt" in model_name.lower():
        conv_mode = "mpt"
    else:
        conv_mode = "llava_v0"

    gConvMode = conv_mode


def describeVideo(videoPath, prompt="describe the video"):
    global gVideoTokenizer,gVideoModel,gVideoProcessor,gConvMode

    inp = prompt

    api_logger.info(f"videoPath: {videoPath}")
    conv = conv_templates[gConvMode].copy()
    
    image = load_video(videoPath)
    image_tensor = gVideoProcessor.preprocess(image, return_tensors='pt')['pixel_values'].half().cuda()
    image_tensor = [image_tensor]


    gVideoModel.update_prompt([[inp]])

    if gVideoModel.config.mm_use_im_start_end:
        inp = DEFAULT_IM_START_TOKEN + DEFAULT_IMAGE_TOKEN + DEFAULT_IM_END_TOKEN + '\n' + inp
    else:
        inp = DEFAULT_IMAGE_TOKEN + '\n' + inp
    conv.append_message(conv.roles[0], inp)
    image = None

    conv.append_message(conv.roles[1], None)
    prompt = conv.get_prompt()
    api_logger.info(f"prompt = {prompt}")

    input_ids = tokenizer_image_token(prompt, gVideoTokenizer, IMAGE_TOKEN_INDEX, return_tensors='pt').unsqueeze(0).cuda()
    stop_str = conv.sep if conv.sep_style != SeparatorStyle.TWO else conv.sep2
    api_logger.info(f"conv: {conv}")
    
    keywords = [stop_str]
    stopping_criteria = KeywordsStoppingCriteria(keywords, gVideoTokenizer, input_ids)
    streamer = TextStreamer(gVideoTokenizer, skip_prompt=True, skip_special_tokens=True)

    with torch.inference_mode():
        output_ids = gVideoModel.generate(
            input_ids,
            images=image_tensor,
            do_sample=True,
            temperature=0.5,
            top_p=0.7,
            max_new_tokens=512,
            streamer=streamer,
            use_cache=True,
            stopping_criteria=[stopping_criteria])

    outputs = gVideoTokenizer.decode(output_ids[0, input_ids.shape[1]:]).strip()
    # conv.messages[-1][-1] = outputs
    # conv.messages[-2][-1] = conv.messages[-2][-1].replace(DEFAULT_IMAGE_TOKEN+'\n','')

    # if args.debug:
    # print("\n", {"prompt": prompt, "outputs": outputs}, "\n")
    api_logger.info(f"outputs:{outputs}")
    return outputs