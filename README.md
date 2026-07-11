# Deepfake Detection Chrome Extension

A browser-based deepfake image detection system built as a Chrome Extension.  
This extension allows users to analyze images from webpages and classify them as Real or Deepfake using a deep learning model based on MobileNetV2.

---

## 🚀 Overview

Deepfake technology has made it increasingly difficult to distinguish manipulated images from authentic ones.  
This project integrates deep learning with a browser extension to provide real-time image classification directly within Chrome.

The extension processes selected images and sends them through a prediction pipeline powered by a transfer learning model.

---

## 🛠 Tech Stack

Frontend (Extension):
- JavaScript
- HTML
- CSS
- Chrome Extension APIs (Manifest V3)

Backend / Model:
- Python
- TensorFlow / Keras
- MobileNetV2 (Transfer Learning)
- Flask (for API-based inference)
- OpenCV
- NumPy

---

## 🧠 Model Architecture

- Input Size: 224x224x3
- Base Model: MobileNetV2 (Pre-trained on ImageNet)
- GlobalAveragePooling Layer
- Dense(1, sigmoid) Output Layer
- Loss Function: Binary Crossentropy
- Optimizer: Adam

---

## ⚙️ How It Works

1. User activates the Chrome Extension.
2. The extension captures or selects an image from the webpage.
3. Image is resized and preprocessed.
4. Image is sent to the prediction pipeline.
5. Model returns classification result:
   - Real
   - Deepfake
6. Result is displayed in the extension popup.

---

## 📂 Project Structure

deepfake-chrome-extension/
│
├── manifest.json
├── popup.html
├── popup.js
├── content.js
├── background.js
├── model/
├── app.py (if using Flask backend)
├── requirements.txt
└── README.md

---

## 📊 Dataset

The model was trained on approximately 22200 images consisting of real and deepfake samples.

Due to repository size limitations, the dataset is not included in this repository.

---

## ▶️ How To Run

### If using Flask backend:

1. Install dependencies:
   pip install -r requirements.txt

2. Run backend:
   python app.py

3. Load extension in Chrome:
   - Go to chrome://extensions
   - Enable Developer Mode
   - Click "Load Unpacked"
   - Select extension folder

---

## 🔍 Features

- Real-time image classification
- Integration of AI model with browser extension
- Modular preprocessing and prediction pipeline
- REST API integration (if backend used)
- Clean extension architecture using Manifest V3

---

## 📈 Future Improvements

- Improve model accuracy with larger dataset
- Add advanced augmentation
- Optimize inference speed
- Deploy backend to cloud
- Add batch image scanning support

---

## 🎯 Learning Outcomes

- Applied transfer learning for binary classification
- Built end-to-end ML pipeline
- Integrated AI model with browser-based application
- Worked with Chrome Extension architecture
- Improved debugging and modular code structuring skills

---

## 👩‍💻 Author

Yogitha Surya Viswanadh Gavara
