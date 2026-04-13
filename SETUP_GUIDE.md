# AI Interview Coach - Setup Guide

This project is a full-stack AI-powered mock interview application using FastAPI (Backend), Streamlit (Frontend), and Groq (LLaMA 3 70B) for AI evaluations.

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have Python 3.8+ installed.

### 2. Install Dependencies
Open your terminal and run:
```bash
pip install -r requirements.txt
```

### 3. Environment Setup
1. Open the `.env` file in the root directory.
2. Replace `your_groq_api_key_here` with your actual Groq API Key.
   - You can get one for free at [console.groq.com](https://console.groq.com/).

### 4. Running the Application

You will need two terminal windows:

#### **Terminal 1: Start the Backend (FastAPI)**
```bash
uvicorn backend.main:app --reload
```
The backend will run on `http://localhost:8000`. It will automatically create the required tables in your PostgreSQL database (ensure you have created the database in pgAdmin first) on first run.

#### **Terminal 2: Start the Frontend (Streamlit)**
```bash
streamlit run frontend/app.py
```
The frontend will open in your browser at `http://localhost:8501`.

---

## 🛠️ Project Structure

- `backend/`: Fast API routes and AI logic.
- `frontend/`: Streamlit UI and state management.
- `database/`: SQLAlchemy models and PostgreSQL database setup.

## ✨ Features
- **Role Selection:** Mix multiple job roles for a hybrid interview experience.
- **AI Question Generation:** Realistic, non-generic questions tailored to your roles.
- **Real-time Evaluation:** Strict and fair scoring with actionable feedback for every answer.
- **Comprehensive Report:** A final overview from an "AI Career Coach" with study suggestions.
