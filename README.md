# 🚀 AI Career Connect

Welcome to **AI Career Connect**! This is an AI-powered web application designed to help you navigate your career path. You can chat with an AI Career Advisor, practice interview questions, get suggestions on your resume, and even use voice commands to ask career questions.

This project is built with beginner-friendly structures, using **Flask** (Python) for the backend and clean **HTML/CSS/JS** with **Bootstrap** for the frontend.

---

## 🌟 Key Features

1. **💬 Chat with AI Career Advisor**: Talk with an AI counselor to get personalized career advice, roadmap suggestions, and skill development recommendations.
2. **🎙️ Voice Q&A**: Ask career questions using your microphone (Speech-to-Text) and hear answers spoken back to you (Text-to-Speech).
3. **📄 Resume Suggestions**: Paste your resume text and get constructive feedback, strength analysis, and tips for improvement.
4. **🧠 Mock Interviews**: Select a job role and difficulty level, and the AI will generate realistic interview questions with sample answer tips.
5. **📊 Admin Dashboard**: See analytics on how many chats, messages, and users are registered in the application.
6. **💾 Database Storage**: Automatically saves all chat conversations to a local SQLite database so you never lose your history.

---

## 🛠️ Tech Stack (The Technologies Used)

*   **Backend Framework**: [Flask](https://flask.palletsprojects.com/) (A simple and lightweight Python web framework).
*   **Database (Database & ORM)**: [SQLite](https://sqlite.org/) (a file-based local database) with [SQLAlchemy](https://www.sqlalchemy.org/) (allows database operations using Python code instead of raw SQL).
*   **AI Engine**: [Mistral AI API](https://mistral.ai/) (generates smart answers for career chats, resume analysis, and interview questions).
*   **Speech System**: [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) (captures microphone input) and offline text-to-speech with [pyttsx3](https://pypi.org/project/pyttsx3/).
*   **Frontend**: HTML, JavaScript, and [Bootstrap CSS](https://getbootstrap.com/) (for beautiful, responsive layouts).

---

## 📂 Project Structure Guide

For beginners, here is a simple directory map showing where everything is located:

```text
ai-career-connect/
│
├── app/                         # All Python backend code lives here
│   ├── __init__.py              # Sets up and starts the Flask application
│   ├── extensions.py            # Sets up database connection tools
│   ├── models.py                # Defines database tables (User, Conversation, Message, Resume)
│   │
│   ├── routes/                  # Maps URLs (web addresses) to Python functions
│   │   ├── main.py              # Main landing page route
│   │   ├── chat.py              # Handles AI chat requests and history
│   │   ├── resume.py            # Handles resume upload and review request
│   │   ├── interview.py         # Handles generating mock interview questions
│   │   ├── speech.py            # Handles Speech-to-Text and Text-to-Speech commands
│   │   └── dashboard.py         # Handles dashboard pages and stats retrieval
│   │
│   └── services/                # Functions that communicate with external tools/database
│       ├── ai_service.py        # Communicates with the Mistral AI API
│       ├── db_service.py        # Performs database operations (saving messages, fetching stats)
│       └── speech_service.py    # Converts speech to text and text to speech
│
├── instance/                    # Local folder (created automatically) where SQLite database is stored
├── static/                      # CSS styling files and client-side JavaScript files
├── templates/                   # HTML files that make up the visual website pages
├── tests/                       # Unit tests to verify that the app works correctly
│
├── .env.example                 # Example configuration template file
├── .env                         # Your private API keys (never commit this to git!)
├── config.py                    # Reads configurations (like debug modes and secret keys)
├── requirements.txt             # List of Python libraries needed to run the app
└── run.py                       # The entry point script to launch the application
```

---

## 🚀 How to Set Up and Run the Project

Follow these steps to run the application on your computer:

### Step 1: Install Python
Make sure you have **Python 3.10 or higher** installed on your system. You can check by running this command in your terminal or Command Prompt:
```bash
python --version
```

### Step 2: Set Up Virtual Environment (Recommended)
A virtual environment keeps the project's dependencies isolated from the rest of your computer.
```bash
# Create a virtual environment named "env"
python -m venv env

# Activate it:
# On Windows (Command Prompt):
env\Scripts\activate
# On Windows (PowerShell):
.\env\Scripts\Activate.ps1
# On macOS / Linux:
source env/bin/activate
```

### Step 3: Install Required Packages
Install all libraries listed in the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

### Step 4: Configure Your Environment Variables
1. Copy the `.env.example` file and rename the new copy to `.env`.
2. Open the `.env` file and insert your **Mistral AI API Key**:
   ```env
   SECRET_KEY=some-random-secret-key-string
   MISTRAL_API_KEY=your_actual_mistral_api_key_here
   MISTRAL_MODEL=mistral-large-latest
   TTS_ENGINE=pyttsx3
   ```
   *(Note: You can get a free Mistral API key from the [Mistral Console](https://console.mistral.ai/)).*

### Step 5: Start the Application
Run the entry point script:
```bash
python run.py
```
After running, open your web browser and navigate to:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 📖 Beginners' Guide: Where to Make Changes

*   **Want to change the design/layout?**
    Go to `templates/` and edit the HTML files. The main styling framework is Bootstrap, which is linked inside `templates/base.html`.
*   **Want to change what the AI says or how it acts?**
    Open `app/services/ai_service.py` and modify the system prompts (`CAREER_SYSTEM_PROMPT`, `RESUME_SYSTEM_PROMPT`, etc.).
*   **Want to add a new page or route?**
    Create a new route function in `app/routes/` and register it inside `app/__init__.py`.
*   **Want to add new columns to the database?**
    Update the models in `app/models.py`, then delete the existing database file under `instance/` to let Flask recreate it automatically.
