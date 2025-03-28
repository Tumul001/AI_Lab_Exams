import streamlit as st
import google.generativeai as genai
from phi.agent import Agent
from phi.model.google import Gemini
from PIL import Image
import speech_recognition as sr
import pyttsx3
import io
import base64
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
API_KEY = os.getenv("GOOGLE_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

# Page configuration
st.set_page_config(
    page_title="Medical Assistant",
    page_icon="🩺",
    layout="wide"
)

st.title("AI Medical Assistant 🩺")
st.subheader("Voice-Based Medical Consultation")

def initialize_text_to_speech():
    """Initialize the text-to-speech engine"""
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)
    return engine

def speak_text(engine, text):
    """Convert text to speech"""
    engine.say(text)
    engine.runAndWait()

def autoplay_audio(audio_file):
    """Autoplay audio in Streamlit"""
    with open(audio_file, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    md = f"""
        <audio autoplay>
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """
    st.markdown(md, unsafe_allow_html=True)

def text_to_speech_file(text, output_file="response.mp3"):
    """Convert text to speech and save to file"""
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.save_to_file(text, output_file)
    engine.runAndWait()
    return output_file

@st.cache_resource
def initialize_agent():
    """Initialize the Gemini agent"""
    return Agent(
        name="Medical Assistant",
        model=Gemini(id="gemini-2.0-flash-exp"),
        markdown=True,
    )

# Initialize the medical assistant agent
medical_assistant = initialize_agent()

# Session state initialization
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'current_response' not in st.session_state:
    st.session_state.current_response = ""

# Voice recording component
if 'recorded_text' not in st.session_state:
    st.session_state.recorded_text = ""

# Voice recording component
st.subheader("Describe your symptoms")
col1, col2 = st.columns([3, 1])

with col1:
    # Display the recorded text in the text area
    voice_input = st.text_area(
        "Your symptoms will appear here after recording",
        value=st.session_state.recorded_text,
        height=100,
        key="voice_input"
    )

# Add debug section that can be toggled
if 'debug_mode' not in st.session_state:
    st.session_state.debug_mode = False

debug_toggle = st.checkbox("Show Debug Info", value=st.session_state.debug_mode)
st.session_state.debug_mode = debug_toggle

if st.session_state.debug_mode:
    st.write(f"**Debug Info:**")
    st.write(f"- Recording State: {'Recording' if st.session_state.is_recording else 'Not Recording'}")
    st.write(f"- Recorded Text Length: {len(st.session_state.recorded_text)}")
    st.write(f"- Session State Keys: {list(st.session_state.keys())}")

with col2:
    # Add recording control buttons in a horizontal layout
    record_col, stop_col = st.columns(2)
    
    # Initialize recording state if not exists
    if 'is_recording' not in st.session_state:
        st.session_state.is_recording = False
    
    with record_col:
        start_recording = st.button("🎤 Start", use_container_width=True, 
                                  disabled=st.session_state.is_recording)
    with stop_col:
        stop_recording = st.button("⏹️ Stop", use_container_width=True, 
                                  disabled=not st.session_state.is_recording)
        
    if stop_recording:
        if st.session_state.debug_mode:
            st.write("DEBUG: Stop button pressed")
        st.session_state.is_recording = False
        st.info("Recording stopped.")
        
    if start_recording:
        if st.session_state.debug_mode:
            st.write("DEBUG: Start button pressed")
        st.session_state.is_recording = True
        with st.spinner("Listening... (speak clearly for up to 30 seconds)"):
            r = sr.Recognizer()
            try:
                with sr.Microphone() as source:
                    # Print debug info
                    if st.session_state.debug_mode:
                        st.write("DEBUG: Microphone initialized")
                    
                    st.write("🔴 Recording... Please describe your symptoms.")
                    r.adjust_for_ambient_noise(source)
                    
                    if st.session_state.debug_mode:
                        st.write("DEBUG: Ambient noise adjusted")
                    
                    # Extended timeout to 30 seconds
                    audio = r.listen(source, timeout=5, phrase_time_limit=30)
                    
                    if st.session_state.debug_mode:
                        st.write("DEBUG: Audio captured successfully")
                
                with st.spinner("Processing your speech..."):
                    if st.session_state.debug_mode:
                        st.write("DEBUG: Recognizing speech")
                    
                    text = r.recognize_google(audio)
                    
                    if st.session_state.debug_mode:
                        st.write(f"DEBUG: Speech recognized, length: {len(text)}")
                    
                    # Store in session state, then update on next rerun
                    st.session_state.recorded_text = text
                    st.session_state.is_recording = False
                    
                    if st.session_state.debug_mode:
                        st.write("DEBUG: Stored text in session state")
                        
                    st.rerun()
            except sr.WaitTimeoutError:
                st.warning("No speech detected. Please try again.")
                st.session_state.is_recording = False
            except sr.RequestError:
                st.error("Could not connect to the speech recognition service. Check your internet connection.")
                st.session_state.is_recording = False
            except Exception as e:
                st.error(f"Error recording: {str(e)}")
                if st.session_state.debug_mode:
                    st.write(f"DEBUG: Exception type: {type(e).__name__}")
                st.session_state.is_recording = False
                
# Manual text input option
st.write("Or type your symptoms manually:")
manual_input = st.text_area(
    "Type your symptoms here",
    height=100,
    key="manual_input"
)

# Image upload for medical conditions
st.subheader("Upload Medical Images (Optional)")
uploaded_image = st.file_uploader("Upload an image of your condition (skin, wound, etc.)", type=["jpg", "jpeg", "png"])
image_description = ""

if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", width=300)

# Process the image with Gemini
    with st.spinner("Analyzing image..."):
        try:
            # Convert PIL Image to bytes for processing
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format=image.format if image.format else 'JPEG')
            img_bytes = img_byte_arr.getvalue()
            
            # Use Gemini to describe the image
            gemini_pro_vision = genai.GenerativeModel('gemini-2.0-flash')
            
            # Create a proper content list with both text prompt and image
            response = gemini_pro_vision.generate_content([
                "Describe this medical image in detail, focusing on visible symptoms or conditions",
                {"mime_type": f"image/{image.format.lower() if image.format else 'jpeg'}", "data": img_bytes}
            ])
            
            image_description = response.text
            st.write("**Image Analysis:**")
            st.write(image_description)
        except Exception as e:
            st.error(f"Error processing image: {str(e)}")
            if st.session_state.debug_mode:
                st.write(f"DEBUG: Image error details: {type(e).__name__} - {str(e)}")
                import traceback
                st.write(f"DEBUG: Traceback: {traceback.format_exc()}")
    # Process and generate advice
if st.button("Get Medical Advice"):
    # Combine voice/manual input with image description
    symptoms = voice_input or manual_input
    
    if not symptoms:
        st.warning("Please describe your symptoms first.")
    else:
        with st.spinner("Consulting AI physician..."):
            # Generate prompt for the medical assistant
            prompt = f"""
            You are a licensed physician assistant. A patient has described the following symptoms:
            {symptoms}
            
            {f"The patient has also provided an image with the following visible symptoms: {image_description}" if image_description else ""}
            
            Provide a thorough assessment including:
            1. Possible conditions based on the symptoms
            2. Recommended home treatments or remedies
            3. When the patient should seek professional medical care
            4. Preventive measures to avoid worsening of the condition
            
            Important: Begin with a disclaimer that this is AI-generated advice and not a substitute for professional medical consultation.
            """
            
            # Get response from the medical assistant
            response = medical_assistant.run(prompt)
            st.session_state.current_response = response.content
            
            # Add to conversation history
            st.session_state.conversation_history.append({
                "symptoms": symptoms, 
                "image": True if uploaded_image else False,
                "advice": response.content
            })
    
        # Display the textual response
        st.subheader("Medical Advice")
        st.markdown(st.session_state.current_response)
        
        # Convert response to speech
        with st.spinner("Generating voice response..."):
            temp_file = "temp_response.mp3"
            text_to_speech_file(st.session_state.current_response, temp_file)
            autoplay_audio(temp_file)
        
        st.success("Voice response generated!")

# Display conversation history
if st.session_state.conversation_history:
    st.subheader("Consultation History")
    for i, entry in enumerate(st.session_state.conversation_history):
        with st.expander(f"Consultation #{i+1}"):
            st.write("**Symptoms Described:**")
            st.write(entry["symptoms"])
            if entry["image"]:
                st.write("*Image was provided*")
            st.write("**Medical Advice:**")
            st.write(entry["advice"])