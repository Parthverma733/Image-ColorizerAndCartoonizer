# 🎨 Image Colorizer & Cartoonizer

This is a web application built with **FastAPI** and **React.js** that allows users to:

- 🖼️ Convert grayscale images to colored versions using a trained deep learning model  
- 🧑‍🎨 Transform regular images into cartoon-style images using OpenCV techniques

---

## 🔧 Setup Instructions

### 📥 1. Clone the Repository

git clone https://github.com/your-username/image-colorizer-cartoonizer.git
cd image-colorizer-cartoonizer
---

###📦 2. Download the Pretrained Model
Download the trained model file from the link below and place it inside the backend/ directory:

🔗 Download model_003200.h5


project-root/
└── backend/
    └── model_003200.h5
###🖥 3. Start the Backend (FastAPI)

cd backend
pip install -r requirements.txt
uvicorn main:app --reload
📌 Backend runs on: http://localhost:8000

###🌐 4. Start the Frontend (React)

cd frontend
npm install
npm start
📌 Frontend runs on: http://localhost:3000

###📷 Sample Test Images
Use images from the images/ folder for testing both features.
The colorizer model works best with grayscale landscape images.

###🛠️ Technologies Used
Backend
Python

FastAPI

TensorFlow / Keras

OpenCV

Frontend
React.js

Axios

Framer Motion

###🚀 Features
Smooth React UI for image upload and preview

Real-time cartoonization using OpenCV

Deep learning-powered grayscale to color conversion

Loading animations and error handling
