# AI Career Matcher

AI Career Matcher is a full-stack application that leverages **AI and machine learning** to help job seekers find the best-matched job opportunities based on their resumes. Users can upload their resumes in PDF or DOCX format and get job recommendations with match scores, skills, and company details. The system also allows searching jobs from the dataset with intelligent ranking.

---

## 🌟 Features

- **AI-Powered Resume Matching**  
  Automatically analyzes uploaded resumes and matches them to the best-fit job opportunities.

- **Smart Match Score**  
  Scores each job based on how well the candidate's skills align with job requirements.

- **Job Search**  
  Search jobs interactively from the dataset using keywords.

- **Responsive Design**  
  Modern UI for both desktop and mobile devices.

- **Data-Driven Recommendations**  
  Uses vector similarity search with FAISS for fast and accurate recommendations.

---

## 🛠️ Tech Stack

### Frontend
- React.js
- CSS / Tailwind (customizable)
- Axios for API requests

### Backend
- Python 3.11+
- FastAPI (REST API)
- FAISS (Vector Search)
- NumPy / Pandas
- JWT Authentication (Optional for user login)

### Database / Storage
- Local CSV / JSON dataset for jobs
- FAISS index for vector search

---

## 📂 Project Structure

ai-career-matcher/
│
├── backend/
│ ├── api/ # API helper files
│ ├── data/ # Job dataset and embeddings (ignored in git)
│ ├── models/ # Preprocessing / ML models
│ ├── notebooks/ # Notebooks for FAISS index building/testing
│ ├── routes/ # FastAPI routes
│ ├── utils/ # Utility scripts
│ └── main.py # FastAPI entrypoint
│
├── frontend/
│ ├── public/ # Public assets
│ ├── src/
│ │ ├── api/ # API calls (resumeApi.js)
│ │ ├── components/ # React components
│ │ └── App.js # Main app component
│ ├── package.json
│ └── package-lock.json
│
└── .gitignore


---

## 🚀 Installation

### Backend

1. Navigate to backend:

cd backend
Create virtual environment:

python -m venv venv
Activate environment:

Windows:
venv\Scripts\activate

Linux / MacOS:
source venv/bin/activate

Install dependencies:
pip install -r requirements.txt

Start FastAPI server:
uvicorn main:app --reload
Server will run at http://127.0.0.1:8080

Frontend
Navigate to frontend:
cd frontend
Install dependencies:
npm install

Start React app:
npm start
App will run at http://localhost:3000

📄 Usage
Open the frontend in your browser (http://localhost:3000).
Upload a resume (PDF) on the Resume Matching page.

View top matched jobs with:
Job Title
Company
Location
Skills
Description
Match Score

Use the Search Jobs page to search for jobs interactively by keyword.

⚙️ Notes
Large datasets (job_meta.jsonl, jobs.csv, job_embeddings.faiss) are ignored in Git due to size.
The project uses FAISS to perform fast vector similarity search for job matching.
Ensure that the dataset is placed in backend/data/ to enable search and matching functionality.

Copy code
npm start
App will run at http://localhost:3000