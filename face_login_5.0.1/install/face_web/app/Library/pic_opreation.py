import base64 as bs64
import numpy as np
from io import BytesIO
from PIL import Image


def prewhiten(x):
    mean = np.mean(x)
    std = np.std(x)
    std_adj = np.maximum(std, 1.0/np.sqrt(x.size))
    y = np.multiply(np.subtract(x, mean), 1/std_adj)
    return y 

def image_to_base64(imgArr):
    img = Image.fromarray(imgArr)
    output_buffer = BytesIO()
    img.save(output_buffer, format='JPEG')
    byte_data = output_buffer.getvalue()
    base64_str = bs64.b64encode(byte_data)
    base64_str = str(base64_str,encoding='utf-8')
    return base64_str

def base2Img(base64):
    byte_data = bs64.b64decode(base64)
    image_data = BytesIO(byte_data)
    img = Image.open(image_data)
    return img

def showImg(base64):
    byte_data = bs64.b64decode(base64)
    image_data = BytesIO(byte_data)
    img = Image.open(image_data)
    return img


