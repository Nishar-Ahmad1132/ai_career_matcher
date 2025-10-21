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