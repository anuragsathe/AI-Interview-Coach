# 🤖 AI Interview Coach

AI Interview Coach is a state-of-the-art, full-stack mock interview application designed to help job seekers prepare for technical and behavioral interviews. Powered by **FastAPI**, **Streamlit**, and **Groq (LLaMA 3 70B)**, it provides realistic, role-specific questions and real-time actionable feedback.

---

## ✨ Key Features

- **🎯 Role-Based Simulation**: Select from multiple job roles (e.g., Software Engineer, Data Scientist, Product Manager) for a tailored interview experience.
- **🧠 Intelligent Question Generation**: Dynamically generates non-generic, high-quality questions based on your chosen career path.
- **⚡ Real-time AI Evaluation**: Get instant, strict, and fair scoring for every answer you provide.
- **📊 Comprehensive Performance Report**: Receive a detailed breakdown of your performance from an "AI Career Coach," including study suggestions and areas for improvement.
- **🗄️ Session Persistence**: Interview data is stored securely in a PostgreSQL database for review.

---

## 🛠️ Technology Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend** | Streamlit (Python-based UI) |
| **Backend** | FastAPI (Performance-focused Python framework) |
| **AI Model** | Groq (LLaMA 3 70B via API) |
| **Database** | PostgreSQL |
| **ORM** | SQLAlchemy |

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.8 or higher
- PostgreSQL installed and running
- A [Groq API Key](https://console.groq.com/) (Free)

### 2. Installation
Clone the repository and install the required dependencies:
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
Create or open the `.env` file in the root directory and configure your credentials:
```env
GROQ_API_KEY=your_actual_groq_api_key_here
DATABASE_URL=postgresql://username:password@localhost:5432/interview_db
```
*Note: Ensure you have created the `interview_db` database in pgAdmin or your preferred SQL client before starting.*

---

## 🏃 How to Run

You will need to run the **Backend** and **Frontend** simultaneously in separate terminals.

### Terminal 1: Start the Backend (FastAPI)
```bash
uvicorn backend.main:app --reload
```
- The API will be live at `http://localhost:8000`.
- **Automatic Migration**: The backend will automatically initialize the database schema on its first run.

### Terminal 2: Start the Frontend (Streamlit)
```bash
streamlit run frontend/app.py
```
- The application will open automatically in your browser at `http://localhost:8501`.

---

## 📂 Project Structure

```bash
├── backend/            # FastAPI routes and AI integration logic
│   ├── routes/         # API endpoints (Evaluate, Generate)
│   ├── services/       # Core AI client (Groq)
│   └── main.py         # Backend entry point & DB initialization
├── database/           # SQLAlchemy models and schema definitions
├── frontend/           # Streamlit application UI and state management
├── .env                # Environment variables (API keys, DB URLs)
└── requirements.txt    # Project dependencies
```

---

## ☁️ Infrastructure & Deployment

The project is configured for automated deployment to AWS using **Terraform** and **GitHub Actions**.

### 🏗️ Infrastructure as Code (Terraform)
The infrastructure is defined in the `terraform/` directory. It provisions:
- An **AWS EC2** instance (`t2.micro`) in `ap-south-1`.
- Automatic installation of dependencies and application startup via `user_data`.

### 🚀 CI/CD Pipeline (GitHub Actions)
The deployment is automated via `.github/workflows/deploy.yml`. 
- **Trigger**: Every push to the `main` branch.
- **Workflow**:
  1. Sets up Terraform.
  2. Configures AWS credentials.
  3. Runs `terraform init` and `terraform apply`.

### 🔐 Setup Requirements
To use the CI/CD pipeline, you must:
1.  **Add Secrets**: Go to your GitHub repository **Settings > Secrets and variables > Actions** and add:
    - `AWS_ACCESS_KEY_ID`: Your AWS Access Key.
    - `AWS_SECRET_ACCESS_KEY`: Your AWS Secret Key.
2.  **EC2 Key Pair**: Ensure you have an EC2 Key Pair named `ai-key` in the `ap-south-1` region.
3.  **Security Groups**: After the first deployment, ensure port `8000` is open in the EC2 Security Group to allow traffic to the FastAPI backend.

---

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request or open an issue for any bugs or feature requests.

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
