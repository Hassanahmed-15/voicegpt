# VoiceGPT – Talk with AI in My Own Voice

Welcome to **VoiceGPT**, an AI-powered voice assistant I built that not only chats with you but **speaks back using my own cloned voice**.  
I used **Eleven Labs** to clone my voice, **FastAPI** for the backend, and a sleek **HTML/CSS frontend**. The app converts your speech to text, generates intelligent responses using **ChatGPT (OpenAI API)**, and then speaks the answers in my voice.

---

## ✨ Features
- **Realistic Voice Cloning** – Powered by **Eleven Labs**, responses come back in my voice.
- **Speech-to-Text (STT)** – Uses **Faster Whisper** for lightning-fast and accurate transcription of your audio input.
- **AI-Powered Responses** – Integrated **ChatGPT (OpenAI API)** to generate intelligent and conversational replies.
- **FastAPI Backend** – Handles all API calls, processing, and response generation efficiently.
- **Clean Frontend** – A simple and responsive interface built with **HTML & CSS**.
- **Audio Playback** – Outputs responses as real-time audio in my cloned voice.

---

## 🛠️ Tech Stack
- **Frontend**: HTML, CSS
- **Backend**: FastAPI (Python)
- **Speech-to-Text**: Faster Whisper
- **Text Generation**: OpenAI ChatGPT API
- **Voice Cloning**: Eleven Labs
- **Audio Handling**: Python audio libraries

---

## 🚀 How It Works
1. **You speak** – The microphone records your audio.
2. **Audio → Text** – Faster Whisper transcribes your voice into text.
3. **AI Thinks** – The text is sent to OpenAI’s ChatGPT, which generates a natural response.
4. **Text → My Voice** – The response is converted into audio using Eleven Labs with my cloned voice.
5. **You listen** – The app plays the answer in my own voice.

---

## ⚙️ Setup Instructions
### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/voicegpt.git
cd voicegpt
```


### 2. Install Dependencies
Make sure you have Python 3.9+ installed, then:
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file and add:
```
OPENAI_API_KEY=your_openai_api_key
ELEVEN_LABS_API_KEY=your_eleven_labs_api_key
```

### 4. Run the Backend
```bash
uvicorn main:app --reload
```

### 5. Open Frontend
Open `index.html` in your browser, or serve it with any static server.

---

## 📂 Project Structure
```
voicegpt/
│
├── main.py            # FastAPI backend
├── templates/         # HTML frontend
├── static/            # CSS and JS files
├── models/            # Faster Whisper model files
├── uploads/           # Recorded audio files
└── requirements.txt   # Python dependencies
```

---

## 🎯 Goals & Vision
This project started as a fun experiment to **combine AI chat with personalized voice synthesis**.  
I wanted something that feels like a conversation with me — not just text on a screen.

---

## 🧠 What I Learned
- Integrating multiple APIs (OpenAI + Eleven Labs).
- Building a real-time voice pipeline: **Record → Transcribe → Respond → Synthesize → Play**.
- Using FastAPI for fast and clean backend architecture.
- Handling audio in Python and optimizing STT with Faster Whisper.

