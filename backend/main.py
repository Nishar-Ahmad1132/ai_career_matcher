from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.resume_routes import router as resume_router
from backend.routes.job_routes import router as job_router  # <-- import your new job_routes

app = FastAPI(title="AI Career Matcher API")

# Include routers
app.include_router(resume_router, prefix="/resume", tags=["Resume Matching"])
app.include_router(job_router, prefix="/jobs", tags=["Job Search"])  # <-- include the new router

# ---------------- Enable CORS ----------------
origins = [
    "http://localhost:3000",  # Your frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
