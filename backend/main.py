

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
def enhance_image_with_opencv(b64_img_str):
    img_bytes = base64.b64decode(b64_img_str)
    nparr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Brightness and contrast
    enhanced = cv2.convertScaleAbs(img, alpha=1.5, beta=30)  # alpha: contrast, beta: brightness

    # Sharpening kernel
    kernel = np.array([[0, -1, 0],
                       [-1, 5,-1],
                       [0, -1, 0]])
    sharpened = cv2.filter2D(enhanced, -1, kernel)

    return cv2.cvtColor(sharpened, cv2.COLOR_BGR2RGB)

# 🖊️ Stronger Edge Mask
def edge_mask(img, line_size=5, blur_value=7):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    gray_blur = cv2.medianBlur(gray, blur_value)
    edges = cv2.adaptiveThreshold(gray_blur, 255,
                                  cv2.ADAPTIVE_THRESH_MEAN_C,
                                  cv2.THRESH_BINARY,
                                  line_size, blur_value)
    return edges

# 🎨 Reduced Color Quantization (flat colors)
def color_quantization(img, k=7):
    data = np.float32(img).reshape((-1, 3))
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)
    _, label, center = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    center = np.uint8(center)
    result = center[label.flatten()]
    return result.reshape(img.shape)

# 🧠 Full Cartoon Effect
def cartoonize(img):
    edges = edge_mask(img, line_size=5, blur_value=7)
    quantized = color_quantization(img, k=9)
    blurred = cv2.bilateralFilter(quantized, d=4, sigmaColor=200, sigmaSpace=200)
    cartoon = cv2.bitwise_and(blurred, blurred, mask=edges)
    return cartoon

# 🚀 API Route
@app.post("/cartoonize")
def cartoonize_image(data: ImageData):
    try:
        rgb_img = enhance_image_with_opencv(data.image)
        cartoon_img = cartoonize(rgb_img)
        bgr_cartoon = cv2.cvtColor(cartoon_img, cv2.COLOR_RGB2BGR)
        _, buffer = cv2.imencode('.jpg', bgr_cartoon)
        cartoon_base64 = base64.b64encode(buffer).decode('utf-8')
        return {"cartoonImage": cartoon_base64}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")
