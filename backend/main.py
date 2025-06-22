






from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import cv2
import base64
import time
from fastapi.middleware.cors import CORSMiddleware
from tensorflow.keras.models import load_model
import traceback


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = load_model("model_003200.h5")


class ImageData(BaseModel):
    image: str

# 1. Enhance image with brightness, contrast, sharpening
#def enhance_image_with_opencv(b64_img_str):
 #   img_bytes = base64.b64decode(b64_img_str)
  #  nparr = np.frombuffer(img_bytes, np.uint8)
   # img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

 #   enhanced = cv2.convertScaleAbs(img, alpha=1.5, beta=30)
  #  kernel = np.array([[0, -1, 0],
   #                    [-1, 5, -1],
    #                   [0, -1, 0]])
    #sharpened = cv2.filter2D(enhanced, -1, kernel)

    #return cv2.cvtColor(sharpened, cv2.COLOR_BGR2RGB)

# 2. Edge detection
def edge_mask(img, line_size, blur_value):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    gray_blur = cv2.medianBlur(gray, blur_value)
    edges = cv2.adaptiveThreshold(gray_blur, 255, 
    cv2.ADAPTIVE_THRESH_MEAN_C, 
    cv2.THRESH_BINARY, 
    blockSize=line_size, 
    C=blur_value)
    smoothed_edges = cv2.GaussianBlur(edges, (5, 5), 0)
    return smoothed_edges

# 3. Color quantization using k-means
def color_quantization(img, k):
    data = np.float32(img).reshape((-1, 3))
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)
    _, label, center = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    center = np.uint8(center)
    result = center[label.flatten()]
    result = result.reshape(img.shape)
    return result

# 4. Final cartoonization
def cartoonize(img):
    edges = edge_mask(img, line_size=5, blur_value=7)
    img_quantized = color_quantization(img, k=9)
    blurred = cv2.bilateralFilter(img_quantized, d=2, sigmaColor=100, sigmaSpace=100)
    edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
    cartoon = cv2.bitwise_and(blurred, edges_colored)
    return cartoon

def upscale_image(img, scale_percent=300):  
    height, width = img.shape[:2]
    new_width = int(width * scale_percent / 100)
    new_height = int(height * scale_percent / 100)
    dim = (new_width, new_height)
    upscaled_img = cv2.resize(img, dim, interpolation=cv2.INTER_CUBIC)
    return upscaled_img

def resize_image(img, max_dim=512):
    height, width = img.shape[:2]
    if max(height, width) > max_dim:
        scale = max_dim / max(height, width)
        new_size = (int(width * scale), int(height * scale))
        return cv2.resize(img, new_size, interpolation=cv2.INTER_AREA)
    return img


def colorizer(img):
    # Resize and normalize image
    img_resized = cv2.resize(img, (256, 256))  
    img_normalized = img_resized / 127.5 - 1  
    img_input = np.expand_dims(img_normalized, axis=0)  

    gen_image = model.predict(img_input)[0]  
    gen_image = (gen_image + 1) * 127.5  
    gen_image = np.clip(gen_image, 0, 255).astype(np.uint8)

    return gen_image


# 5. API Endpoint
@app.post("/cartoonize")
def cartoonize_image(data: ImageData):
    try:
        start = time.time()

        # Decode image
        img_data = base64.b64decode(data.image)
        np_img = np.frombuffer(img_data, np.uint8)
        bgr_img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
        if bgr_img is None:
            raise HTTPException(status_code=400, detail="Invalid image")
        rgb_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)

        # Resize for faster processing
        rgb_img = resize_image(rgb_img)

        cartoon_img = cartoonize(rgb_img)

        # Optional: reduce upscale scale
        upscaled_img = upscale_image(cartoon_img, scale_percent=300)

        bgr_cartoon = cv2.cvtColor(upscaled_img, cv2.COLOR_RGB2BGR)
        _, buffer = cv2.imencode('.jpg', bgr_cartoon, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
        cartoon_base64 = base64.b64encode(buffer).decode('utf-8')

        print(f"✅ Process completed in {time.time() - start:.2f}s")
        return {"cartoonImage": cartoon_base64}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")



@app.post("/colorizer")
def cartoonize_image(data: ImageData):
    try:
        # Decode base64 image
        img_data = base64.b64decode(data.image)
        np_img = np.frombuffer(img_data, np.uint8)
        bgr_img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

        if bgr_img is None:
            raise HTTPException(status_code=400, detail="Invalid image")

        rgb_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
        color_img = colorizer(rgb_img)

        # Convert back to BGR for JPEG encoding
        bgr_color = cv2.cvtColor(color_img, cv2.COLOR_RGB2BGR)
        _, buffer = cv2.imencode('.jpg', bgr_color)
        color_base64 = base64.b64encode(buffer).decode('utf-8')

        return {"coloredImage": color_base64}

    except Exception as e:
        traceback.print_exc()  
        raise HTTPException(status_code=500, detail=str(e))









