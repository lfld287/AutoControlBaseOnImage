from typing import List
import easyocr
import PIL.Image
import io


def ListWord(img:PIL.Image.Image) -> List :
    buf = io.BytesIO()
    img.save(buf, format='JPEG')
    byte_im = buf.getvalue()
    reader = easyocr.Reader(['ch_sim','en']) # need to run only once to load model into memory
    result = reader.readtext(byte_im)
    return result

def ListWordFile(filePath:str) -> list :
    reader = easyocr.Reader(['ch_sim','en']) # need to run only once to load model into memory
    result = reader.readtext(filePath)
    return result