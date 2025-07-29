# 📚 AI-Powered Interactive Learning App with Webcam & Gemini API 🤖🎥

Welcome to the **AI-Powered Interactive Learning App** — a smart educational assistant that combines **real-time webcam input** with **Google’s Gemini AI** to deliver intelligent, interactive responses. Built using **Streamlit**, **OpenCV**, and the **Gemini API**, this tool enables a hands-free learning experience driven by vision and voice.

---

## 🔍 Project Overview

This application leverages:
- 📷 **Webcam input** using OpenCV
- 🧠 **Natural language AI** with Gemini (Generative AI)
- 🌐 **Streamlit** for intuitive, real-time web UI

Users can interact through gestures or capture a live frame from their webcam, and Gemini responds with AI-generated educational explanations, summaries, or helpful content.

---

## 🎯 Features

✅ Real-time webcam integration using OpenCV  
✅ AI-generated responses from Gemini (Google's LLM)  
✅ Streamlit-powered live web interface  
✅ Interactive and minimal design for learning and demonstration  
✅ Secure API management using environment variables  

---

## 📂 Folder Structure

interactive-learning-app/
├── final.py # Streamlit app code
├── requirements.txt # All dependencies
├── .env # Secret API key (Not uploaded to GitHub)
├── .gitignore # Ignore .env and other unnecessary files
├── README.md # Project description (this file)


---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/interactive-learning-app.git
cd interactive-learning-app

---

### 2. Create a Virtual Environment (Optional but Recommended)

python -m venv venv
source venv/bin/activate    # On Linux/Mac
venv\Scripts\activate       # On Windows

---

###3. Install Dependencies
pip install -r requirements.txt

---
###4. Create a .env File
Create a .env file in the root of your project and add your Gemini API key:
GEMINI_API_KEY=your_api_key_here

---
Run the App
streamlit run final.py

🔐 Environment Variables
To keep your API key secure, we use dotenv to load the key from a .env file.

✅ Make sure your .env file is added to .gitignore so it is never pushed to GitHub.
