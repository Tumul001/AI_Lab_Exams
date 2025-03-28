# AI Medical Assistant 🩺

A voice-based AI physician assistant that provides medical consultations through natural conversation.

## 🌟 Overview

This application simulates a physician consultation experience using voice interaction. Users can describe their symptoms verbally, upload medical images (such as skin conditions), and receive AI-generated medical advice delivered through voice response.

## ✨ Key Features

- **Voice-Based Interaction**: Describe your symptoms naturally through speech
- **Image Analysis**: Upload photos of visible conditions for AI assessment
- **Voice Response**: Receive spoken medical advice for a natural consultation experience
- **Consultation History**: Review previous interactions and medical recommendations
- **Text Backup**: All voice interactions are backed up with text for easy reference

## 🛠️ Technologies Used

- **Streamlit**: Interactive web application framework
- **Google Gemini AI**: Advanced large language model for medical analysis
- **SpeechRecognition**: Converts speech to text
- **pyttsx3**: Text-to-speech synthesis
- **PIL**: Image processing and analysis

## 📋 Prerequisites

- Python 3.11 or higher
- A Google API key for Gemini AI
- A working microphone for voice input
- Internet connectivity for API access

## 🚀 Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/ai-medical-assistant.git
   cd ai-medical-assistant
   ```
2. **Set up a Python virtual environment**

   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```
3. **Install required packages**

   ```bash
   uv sync
   ```
4. **Create a .env file with your Google API key**

   ```
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

## 🖥️ Usage

1. **Start the application**

   ```bash
   streamlit run medical_assistant.py
   ```
2. **Describe your symptoms**

   - Click "Start" to begin voice recording
   - Speak clearly about your symptoms
   - Click "Stop" if you finish before the time limit
3. **Upload relevant medical images (optional)**

   - Upload photos of visible symptoms like skin conditions
   - The AI will analyze the images to aid diagnosis
4. **Get medical advice**

   - Click "Get Medical Advice" to generate recommendations
   - Listen to the voice response
   - Read the detailed text recommendations
   - Review previous consultations in the history section

## ⚠️ Important Notice

This application is for educational and demonstration purposes only. The AI-generated medical advice should not replace professional medical consultation. Always consult with a qualified healthcare provider for medical concerns.

## 🙏 Acknowledgments

- Google for providing the Gemini AI API
- The Streamlit team for their excellent framework
- The open-source community for speech recognition and synthesis libraries

---

Made with ❤️ and AI
