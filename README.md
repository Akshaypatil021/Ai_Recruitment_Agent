# FairHire AI – Bias-Free AI Recruitment & Skill Assessment System  

🚀 **FairHire AI** is an AI/ML-driven candidate evaluation platform designed to remove bias from hiring, analyze resumes, generate interview questions, and help candidates upskill.

This project was built for a hackathon challenge focused on **ethical AI hiring solutions** and end-to-end talent evaluation.

---

## ⭐ Key Features

✔️ Upload resume (PDF / DOCX / DOC)  
✔️ Resume parsing using NLP  
✔️ Domain skill extraction  
✔️ ML-powered selection / rejection prediction  
✔️ Dynamic skill improvement suggestions  
✔️ Live AI interview question generation using Ollama (Llama3)  
✔️ HR Dashboard with analytics  
✔️ Bias removal before screening  
✔️ Per-candidate reports & scoring

---

## 🧠 System Architecture

Candidate → Upload Resume → Backend ML Pipeline
↓
Skill Mapping + Domain Evaluation
↓
AI Question Generation (Ollama Llama3)
↓
Candidate Report + HR Dashboard Integration


---

## 💡 Tech Stack

### Frontend  
- HTML  
- CSS  
- JavaScript  

### Backend
- Flask (Python)

### AI / ML
- Sentence Transformers  
- Scikit-Learn  
- Logistic Regression classifier  
- Ollama Llama3 model (real-time interview questions)

### Parsing Libraries
- PyPDF2  
- python-docx  

### Other
- Matplotlib (Recruiter dashboard charts)  
- UUID based candidate tracking  

---

## 📌 Project Modules

### 🔹 1. Candidate Portal

- Resume Upload
- Domain Selection
- Resume Parsing
- Candidate Skill Report
- Personalized AI Interview Questions

### 🔹 2. HR / Recruiter Portal

- Candidate List View
- Selection Status
- Score & Domain Metrics
- Domain-wise Bar Graph

---

## ⚙️ How it Works (Flow)

### ✔ 1) Candidate uploads resume  
→ Flask extracts text  
→ Skills detected using ML + rule based parsing  

### ✔ 2) ML Model Classifies  
Model predicts `selected / rejected` using trained classifier

### ✔ 3) Candidate receives  
- Strengths
- Improvement Recommendations
- Learning Paths
- **AI interview questions (generated live)**

### ✔ 4) HR Dashboard View  
Only shortlisted candidates appear for recruiters with score, name, domain etc.

---

## 🧩 AI Components

### 🔹 Resume Classifier  
A Logistic Regression model trained on labeled resumes data.

### 🔹 Skill Extractor  
Maps resume text with domain skill list.

### 🔹 Personality Traits & Profile Type  
Basic NLP rule-based heuristics.

### 🔹 Interview Question Generator  
Uses **Ollama Llama3** to generate  
dynamic, contextual questions based on resume + domain.

---

## 📂 Project Structure

/project
│── app.py # Flask backend
│── model_inference.py # ML model + prediction pipeline
│── train_model.py # Resume classifier training
│── /templates # Frontend UI pages
│ ├─ index.html
│ ├─ skills.html
│ ├─ questions.html
│ └─ reports.html
│── /uploads # Uploaded resumes
│── requirements.txt
│── README.md


---

## 🔧 Installation & Setup

```bash
git clone <repo-url>
cd FairHire-AI
pip install -r requirements.txt
python app.py


ollama run llama3


| Endpoint                          | Description                  |
| --------------------------------- | ---------------------------- |
| `/api/analyze_resume`             | Upload & analyze resume      |
| `/api/skill_report?candidate_id=` | Fetch skill data             |
| `/api/questions?candidate_id=`    | Fetch AI interview questions |
| `/api/candidates`                 | HR candidate list            |
| `/upload_bulk`                    | Bulk resume processing       |


📈 HR Dashboard Features

✔ Shortlisted candidate table
✔ Domain-wise charts
✔ Score visualization

🛡 Fairness & Bias Reduction

Before AI scoring:

Name masked

Email anonymized

Contact removed

This enables capability-focused evaluation.

🎯 Why this Project Matters?

Traditional hiring suffers from:

❌ Human bias
❌ Manual screening load
❌ No personalized improvement feedback

✔ FairHire AI solves this using AI + Ethics to create a merit-first hiring pipeline.

📌 Future Enhancements

🔹 Voice interview questions
🔹 Adaptive learning suggestions
🔹 Multi-language support
🔹 ATS integrations

🙌 Contributors

👤 Akshay Patil  (Lead Developer, AI Engineer)
💡 Designed, Developed, Trained ML Models, Developed UI, Implemented AI Questioning System.
