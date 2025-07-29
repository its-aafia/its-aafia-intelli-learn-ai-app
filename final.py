import streamlit as st
from PIL import Image
import base64
import pyttsx3
import cv2
import numpy as np
import os
from dotenv import load_dotenv
from cvzone.HandTrackingModule import HandDetector
import google.generativeai as genai

# ------------------ Load Environment Variables ------------------
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("❌ API key not found. Please set GEMINI_API_KEY in .env.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# ------------------ Streamlit Setup ------------------
st.set_page_config(layout="centered", page_title="Interactive Learning App")

# ------------------ Base64 Background Image ------------------
def get_base64(file_path):
    try:
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        st.warning(f"⚠️ Image not found: {file_path}")
        return ""

# ------------------ TTS Engine Setup ------------------
def speak_text(text, name=""):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 1)
        engine.say(f"Hey {name}, {text}")
        engine.runAndWait()
    except:
        pass

# ------------------ Session State Init ------------------
if "step" not in st.session_state:
    st.session_state.step = "input_screen"
    st.session_state.name = ""
    st.session_state.age = 0
    st.session_state.voice_enabled = True
    st.session_state.greeted = False
    st.session_state.webcam_active = False

# ------------------ Step 1: Input Screen ------------------
if st.session_state.step == "input_screen":
    encoded_image = get_base64("Kids.png")
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_image}");
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
        }}
        .input-container {{
            position: absolute;
            top: 45%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
            color: white;
            background-color: rgba(0, 0, 0, 0.6);
            padding: 30px;
            border-radius: 15px;
            width: 80%;
            max-width: 500px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="input-container">
            <h2>Welcome to the Interactive Learning App!</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.session_state.name = st.text_input("Enter Your Name", placeholder="Type your name...")
        st.session_state.age = st.number_input("Enter Your Age", min_value=1, max_value=100, value=10)
        st.session_state.voice_enabled = st.checkbox("Enable Voice", value=True)

        if st.button("Let's Begin!"):
            st.session_state.step = "welcome_screen"

# ------------------ Step 2: Welcome Screen ------------------
if st.session_state.step == "welcome_screen":
    st.markdown(f"<h1 style='text-align:center; color:purple;'>✨ Welcome, {st.session_state.name}! ✨</h1>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align:center; color:blue;'>Get ready to explore and learn! 🎉</h2>", unsafe_allow_html=True)
    if st.session_state.voice_enabled and not st.session_state.greeted:
        speak_text(f"Welcome {st.session_state.name}. Get ready to explore and learn!", st.session_state.name)
        st.session_state.greeted = True
    if st.button("Next"):
        st.session_state.step = "main_app"

# ------------------ Step 3: Main Application ------------------
if st.session_state.step == "main_app":
    st.subheader("🎨 Come, Draw and Get Answers — Learn with Fun!")
    col1, col2 = st.columns([3, 2])
    with col1:
        run = st.checkbox("Run Webcam", value=False, key="webcam_toggle")
        FRAME_WINDOW = st.image([])
    with col2:
        st.title("AI Says 🎤")
        output_text_area = st.empty()

    if run and not st.session_state.webcam_active:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            st.error("❌ Unable to access webcam.")
        else:
            cap.set(3, 1280)
            cap.set(4, 720)
            detector = HandDetector(maxHands=1)
            prev_pos = None
            canvas = None
            st.session_state.webcam_active = True

            while st.session_state.webcam_toggle:
                success, img = cap.read()
                if not success:
                    st.warning("⚠️ Could not read frame from webcam.")
                    break

                img = cv2.flip(img, 1)
                if canvas is None:
                    canvas = np.zeros_like(img)

                hands, img = detector.findHands(img, draw=False, flipType=True)
                if hands:
                    hand = hands[0]
                    lmList = hand["lmList"]
                    fingers = detector.fingersUp(hand)
                    current_pos = None

                    if fingers == [0, 1, 0, 0, 0]:
                        current_pos = lmList[8][0:2]
                        if prev_pos is None:
                            prev_pos = current_pos
                        cv2.line(canvas, prev_pos, current_pos, (0, 255, 0), 15)
                        prev_pos = current_pos
                    elif fingers == [1, 0, 0, 0, 0]:
                        canvas = np.zeros_like(canvas)
                        prev_pos = None
                    elif fingers == [0, 1, 1, 1, 0]:
                        pil_image = Image.fromarray(canvas)
                        prompt = """You are a friendly and humorous AI art teacher for kids aged 5 to 10. Respond to drawings enthusiastically, encourage creativity, and make learning fun (2 to 10 lines).

If Draw 'st': Share a fun story.
If Draw 'Po': Recite a silly poem.
If Draw 'AB': Sing ABC playfully.
If Messy: Encourage experimentation.
If '111': Count in a funny way.
If Math: Solve it smartly.
"""
                        try:
                            response = model.generate_content([prompt, pil_image])
                            output_text = response.text
                            output_text_area.text(output_text)
                            if st.session_state.voice_enabled:
                                speak_text(output_text, st.session_state.name)
                        except Exception:
                            output_text_area.text("Error with AI response.")

                combined = cv2.addWeighted(img, 0.7, canvas, 0.3, 0)
                FRAME_WINDOW.image(combined, channels="BGR")

            cap.release()
            st.session_state.webcam_active = False
