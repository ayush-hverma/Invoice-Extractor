import easyocr
from PIL import Image

reader = easyocr.Reader(['en'], gpu=False)

def extract_text_from_image(image_path):
    result = reader.readtext(image_path, detail=0)
    text = "\n".join(result)
    return text