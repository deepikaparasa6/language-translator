# Language Translator Application

**Subtitle:** *A Simple Web-Based Multi-Language Text Translation System*  
**Author:** 3rd-Year B.Tech Computer Science & Engineering  
**Project Category:** Web Application / External API Integration / Internship Project  

---

## 📌 Project Overview

The **Language Translator Application** is a clean, responsive, and robust web application developed in Python. It provides instant translation of text between over 130 human languages.

Designed specifically for an internship and classroom presentation, the project emphasizes **practical software engineering principles**:
- Clean separation of UI and business logic (modular architecture)
- Robust input validation and defensive exception handling
- Real-time third-party service integration via `deep-translator` and Google Translate
- Modern light glassmorphism SaaS user interface built with Gradio

> **Important Note:** This project does not claim to have trained an internal machine learning model. Instead, it demonstrates how to integrate, wrap, and error-handle external cloud translation services in a user-friendly application.

---

## 🏗️ System Architecture

The workflow follows a clean linear pipeline:

```text
[User]
   │
   ▼
[Gradio Web Interface] (app.py)
   │
   ▼
[Translation Handler & Validation] (translator.py)
   │
   ▼
[Deep Translator Wrapper (GoogleTranslator)]
   │
   ▼
[Google Translate Service]
   │
   ▼
[Translated Text Result]
   │
   ▼
[Gradio Output Display & Copy Action]
```

---

## ✨ Features

- **Multi-Language Support:** Supports over 130 languages fetched dynamically from the translation service, with fallback support if offline.
- **Auto Language Detection:** Automatically detects the source language when `Auto Detect` is selected.
- **Modern Glassmorphism SaaS UI:** Soft gradient background, blur-filtered translucent panels, smooth hover animations, and elegant typography.
- **Defensive Error Handling:**
  - Empty or whitespace-only inputs prompt the user with a friendly notice.
  - Identical source and target selections are handled gracefully without unnecessary network calls.
  - Rate limits (HTTP 429) or network interruptions fall back to resilient endpoints or display user-friendly notices without exposing raw Python tracebacks.
- **Interactive Convenience Controls:**
  - **✨ Translate:** Primary action with a subtle gradient shine.
  - **⇄ Swap Languages:** Easily flips source and target languages.
  - **📋 Copy Translation:** One-click clipboard copy with immediate toast confirmation.
  - **Clear:** Resets both input and output fields.

---

## 🛠️ Technologies Used

| Technology | Role |
|---|---|
| **Python 3.10+** | Core programming language |
| **Gradio (v6.x)** | Web UI framework and component event handling |
| **Deep Translator** | Translation service abstraction layer (`GoogleTranslator`) |
| **Google Translate Service** | Real-time multi-language neural translation backend |
| **Requests** | HTTP client for resilient endpoint fallback |

---

## 📂 Project Structure

```text
language-translator/
│
├── app.py              # Gradio web interface, glassmorphism CSS, and event handlers
├── translator.py       # Core translation logic, language code mapping, and validation
├── test_app.py         # Automated test suite verifying translation cases and edge cases
├── requirements.txt    # Project dependencies
└── README.md           # Project documentation and presentation guide
```

### File Details:
- **`app.py`**: Builds the Gradio Blocks layout, applies modern CSS styles, manages language dropdowns, and wires up event listeners for translation, swapping, copying, and clearing.
- **`translator.py`**: Encapsulates all translation business logic, queries dynamic language lists, validates text inputs, converts friendly language names to ISO codes, and invokes `GoogleTranslator`.
- **`test_app.py`**: Automated unit tests checking English to Hindi, French, Spanish, empty inputs, identical languages, and language retrieval.
- **`requirements.txt`**: Minimal, production-tested package requirements.

---

## 🚀 Installation & Setup (Windows)

Follow these steps to run the application on your local machine:

### 1. Open Terminal or PowerShell
Navigate to the project directory:


### 2. (Optional) Create and Activate a Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python app.py
```

### 5. Access the Web Interface
Open your web browser and go to:
```text
http://127.0.0.1:7860
```

---

## 🧪 Automated Testing

A complete test suite is included to demonstrate reliability during your internship viva:

```bash
python test_app.py
```

### Test Cases Covered:
1. **English → Hindi**: `"Good morning, how are you?"` ➔ `"सुप्रभात आप कैसे हैं?"`
2. **English → French**: `"Welcome to my project."` ➔ `"Bienvenue dans mon projet."`
3. **English → Spanish**: `"I am learning Python."` ➔ `"Estoy aprendiendo Python."`
4. **Empty Input**: Returns `"Please enter some text to translate."`
5. **Same Language**: Detects identical source/target and handles cleanly without crashing.
6. **Auto Detect**: Correctly detects input language and translates to target.
7. **Supported Languages Count**: Validates that 130+ languages are dynamically loaded.

---

## 🔮 Future Enhancements

The following features can be added in future versions:
- **Speech-to-Text (Voice Input):** Allow users to speak their input using Web Speech API or Whisper.
- **Text-to-Speech (TTS):** Add an audio pronunciation button to hear the translated output.
- **Translation History:** Persist previous translations in a local SQLite database or browser storage.
- **Document / File Translation:** Support uploading `.txt`, `.docx`, or `.pdf` files for bulk translation.
- **Cloud Deployment:** Deploy to Hugging Face Spaces or Render for public 24/7 access.
