# backend/api/search_api.py
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import faiss
import json
import numpy as np

# ----------------------------
# Initialize FastAPI app
# ----------------------------
app = FastAPI(title="AI Career Matcher API")

# ----------------------------
# Load FAISS index and metadata
# ----------------------------
INDEX_PATH = "backend/data/job_embeddings.faiss"
META_PATH = "backend/data/job_meta.jsonl"

print("🔹 Loading FAISS index and metadata...")

# Load FAISS index
index = faiss.read_index(INDEX_PATH)

# Load job metadata
jobs = []
with open(META_PATH, "r", encoding="utf-8") as f:
    for line in f:
        jobs.append(json.loads(line))

print(f"✅ Loaded {len(jobs)} job entries")

# ----------------------------
# Load SentenceTransformer model
# ----------------------------
print("🔹 Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("✅ Model ready")


# ----------------------------
# Define request model
# ----------------------------
class SearchRequest(BaseModel):
    query: str
    top_k: int = 5


# ----------------------------
# API endpoint for job search
# ----------------------------
@app.post("/search")
def search_jobs(request: SearchRequest):
    query = request.query
    top_k = request.top_k

    # Convert query to vector
    query_vec = model.encode([query])
    query_vec = np.array(query_vec).astype("float32")

    # Search FAISS
    D, I = index.search(query_vec, top_k)

    results = []
    for idx, score in zip(I[0], D[0]):
        if idx < len(jobs):
            job = jobs[idx]
            results.append({
                "job_title": job.get("jobtitle", "N/A"),
                "company": job.get("company", "N/A"),
                "location": job.get("joblocation_address", "N/A"),
                "employment_type": job.get("employmenttype_jobstatus", "N/A"),
                "skills": job.get("skills", "N/A"),
                "description": job.get("jobdescription", "N/A")[:350] + "...",
                "site": job.get("site_name", "N/A"),
                "post_date": job.get("postdate", "N/A"),
                "advertiser_url": job.get("advertiserurl", "N/A"),
                "shift": job.get("shift", "N/A"),
                "match_score": round(float(score), 3)
            })

    return {
        "query": query,
        "results_found": len(results),
        "results": results
    }
