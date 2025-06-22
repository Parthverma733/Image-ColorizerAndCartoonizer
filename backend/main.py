

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import cv2
import base64
from PIL import Image, ImageEnhance
import io
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ImageData(BaseModel):
    image: str

# 📸 Pillow Enhancement
def enhance_image_with_pillow(b64_img_str):
    img_bytes = base64.b64decode(b64_img_str)
    image = Image.open(io.BytesIO(img_bytes)).convert('RGB')

    image = ImageEnhance.Sharpness(image).enhance(2.5)
    image = ImageEnhance.Contrast(image).enhance(1.3)
    image = ImageEnhance.Brightness(image).enhance(1.5)

    img_np = np.array(image)
    return img_np

# 🖊️ Stronger Edge Mask
def edge_mask(img, line_size=9, blur_value=9):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    gray_blur = cv2.medianBlur(gray, blur_value)
    edges = cv2.adaptiveThreshold(gray_blur, 255,
                                  cv2.ADAPTIVE_THRESH_MEAN_C,
                                  cv2.THRESH_BINARY,
                                  line_size, blur_value)
    return edges

# 🎨 Reduced Color Quantization (flat colors)
def color_quantization(img, k=5):
    data = np.float32(img).reshape((-1, 3))
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)
    _, label, center = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    center = np.uint8(center)
    result = center[label.flatten()]
    return result.reshape(img.shape)

# 🧠 Full Cartoon Effect
def cartoonize(img):
    edges = edge_mask(img, line_size=9, blur_value=9)
    quantized = color_quantization(img, k=4)
    blurred = cv2.bilateralFilter(quantized, d=7, sigmaColor=300, sigmaSpace=300)
    cartoon = cv2.bitwise_and(blurred, blurred, mask=edges)
    return cartoon

# 🚀 API Route
@app.post("/cartoonize")
def cartoonize_image(data: ImageData):
    try:
        rgb_img = enhance_image_with_pillow(data.image)
        cartoon_img = cartoonize(rgb_img)
        bgr_cartoon = cv2.cvtColor(cartoon_img, cv2.COLOR_RGB2BGR)
        _, buffer = cv2.imencode('.jpg', bgr_cartoon)
        cartoon_base64 = base64.b64encode(buffer).decode('utf-8')
        return {"cartoonImage": cartoon_base64}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")
