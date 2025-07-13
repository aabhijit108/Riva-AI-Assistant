# 💫 Riva - AI Female Desktop Assistant
Riva is a powerful, customizable, multilingual AI voice assistant for Windows. Inspired by Jarvis and ChatGPT, Riva combines voice interaction, smart automation, and real-time AI integration to help you manage your PC and tasks with ease.

✨ Features
🎙️ Voice Interaction
Talk to Riva like a human! She listens, speaks, and executes commands in real time.

💬 Ask Anything (ChatGPT-Style)
Powered by OpenRouter API with models like GPT-4 and DeepSeek to answer any question.

📄 Read PDFs and Word Docs Aloud
Just say the name of your file and Riva will read it out loud using text-to-speech.

🌍 Multilingual Support
Speak in English, Hindi, Spanish, Chinese, and more – live voice translation support coming soon.

🧠 Remembers You
Riva learns your preferences and can remember habits or commands for future use.

🖥️ System Control
Open applications, manage files, organize directories, or control web browsers with voice.

🛠️ Code Generation & Execution
Ask Riva to generate login pages, calculators, APIs, or scripts. She will write the code and save it to your PC.

📂 Automatic File Finder
No need for full paths. Say “read resume” and Riva will find your file on Desktop, Downloads, or D drive.

📸 Webcam Capture (Coming Soon)
Capture photos from your webcam on command.

🌐 Web Automation (Coming Soon)
Auto-fill forms, browse websites, or scrape data via Selenium.

🎙️ Voice-to-Voice Translation (Coming Soon)
Speak in one language, hear in another.

🖼️ GUI Highlights (Tkinter)
Live logs of interaction

Smart code generation box with copy-to-clipboard

Status indicators (Idle, Listening, Speaking)

Clean modern dark-themed UI

🛠️ Technologies Used
Python 3.10+

SpeechRecognition, pyttsx3, OpenRouter API

Tkinter for GUI

PyPDF2, python-docx for document reading

Selenium, OpenCV (planned)

gTTS, googletrans (planned for voice translation)

📦 Installation

bash Copy Edit

git clone https://github.com/aabhijit108/Riva-AI-Assistant.git
cd Riva-AI-Assistant
pip install -r requirements.txt
python riva_gui.py
⚠️ Make sure to set your OpenRouter API key in config.py or .env.

📂 Project Structure

graphql Copy Edit

├── riva_gui.py            # Main GUI launcher
├── riva_assistant.py      # Core logic
├── pdf_reader.py          # File reader module
├── config.py              # API keys and configs
├── assets/                # Sounds, logos (optional)
└── README.md

🙋‍♂️ Author
Developed by Abhijit Adhikari
