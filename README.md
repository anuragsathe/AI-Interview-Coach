# AI Persona Coach | Interview Mastery 🤖

A sophisticated, AI-driven interview preparation platform designed to help candidates land their dream roles. Powered by the incredibly fast **Groq API** and built with a scalable **FastAPI** + **Streamlit** architecture, the app provides real-time, personalized, role-specific interview simulations with deep analytics and actionable feedback.

![Project Status](https://img.shields.io/badge/Status-Active-success)
![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue)
![Database](https://img.shields.io/badge/Database-PostgreSQL-blue)
![Cloud](https://img.shields.io/badge/Deployed-AWS_EC2-orange)

## 🚀 Key Features

*   **Role-Specific Simulations**: Choose your specific path (Banking, IT, Data Science, AI Engineer, Teaching, Sales, etc.) and difficulty rigor (Graduate to Executive).
*   **Intelligent Assessment**: Powered by the Groq API to generate highly relevant technical and behavioral questions, providing nuanced, benchmarked evaluation.
*   **Comprehensive Analytics Dashboard**: Get a detailed breakdown of your performance, including key strengths, growth areas, and an overall job-readiness rank.
*   **Strategic Growth Roadmap**: Receive actionable pro tips and highly recommended study topics tailored exactly to your weaknesses.
*   **Beautiful UI/UX**: A modern, glassmorphism-inspired UI designed to feel like a premium career coaching platform.
*   **Enterprise-Grade Infrastructure**: Deployed on AWS EC2 using Infrastructure as Code (Terraform) and seamless CI/CD via GitHub Actions.

## 🛠️ Technology Stack

*   **Frontend**: Streamlit (Python) with custom CSS styling for premium aesthetics.
*   **Backend**: FastAPI for lightning-fast, asynchronous REST API routes.
*   **Database**: PostgreSQL using SQLAlchemy ORM to manage interview sessions, questions, and granular evaluations.
*   **AI Engine**: Groq API to serve Large Language Model functionalities at extreme speeds.
*   **DevOps & Cloud**: Terraform, AWS EC2, GitHub Actions.

## 📁 Project Structure

```text
AI-Interview-Coach/
├── backend/          # FastAPI application (generation & evaluation routes)
├── frontend/         # Streamlit User Interface (app.py)
├── database/         # SQLAlchemy models and PostgreSQL connection logic
├── terraform/        # Infrastructure as Code (main.tf) for AWS deployment
├── requirements.txt  # Python package dependencies
└── README.md         # Project documentation
```

## ⚙️ Local Setup and Installation

### Prerequisites

*   Python 3.9+
*   PostgreSQL running locally or remotely
*   A valid [Groq API Key](https://console.groq.com/)

### 1. Clone the repository

```bash
git clone https://github.com/your-username/AI-Interview-Coach.git
cd AI-Interview-Coach
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Variables

Create a `.env` file in the root directory and add your configuration details:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/interview_db
GROQ_API_KEY=your_groq_api_key_here
```
*(Make sure to replace the placeholder values with your actual Postgres credentials and Groq API key)*

### 4. Run the Backend (FastAPI)

Open a new terminal and start the Uvicorn server:

```bash
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```
* The API will be available at: `http://localhost:8000`
* Interactive API Docs (Swagger UI): `http://localhost:8000/docs`

### 5. Run the Frontend (Streamlit)

Open another terminal session:

```bash
streamlit run frontend/app.py
```
* The UI should automatically launch in your browser at `http://localhost:8501`

## ☁️ Deployment

This project uses **Terraform** for automated infrastructure deployment on AWS.
To provision or update the infrastructure, navigate to the `terraform` directory:

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

Deployment is further streamlined via **GitHub Actions** which securely utilizes GitHub Secrets to update the EC2 instance upon pushing code changes to the repository.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

---
*Built to empower the next generation of professionals to master their career journey.*
