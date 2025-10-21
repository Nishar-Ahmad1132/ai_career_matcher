from fastapi import APIRouter, Query
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import json

router = APIRouter()

# Load model, index, and jobs metadata (same as before)
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
INDEX_PATH = "backend/data/job_embeddings.faiss"
META_PATH = "backend/data/job_meta.jsonl"

model = SentenceTransformer(MODEL_NAME)
index = faiss.read_index(INDEX_PATH)

jobs = []
with open(META_PATH, "r", encoding="utf-8") as f:
    for line in f:
        jobs.append(json.loads(line))

@router.get("/search_jobs")
async def search_jobs(
    query: str = Query(..., description="Search keywords"),
    top_k: int = 10
):
    """Search jobs based on a keyword or skills"""
    if not query.strip():
        return {"matches": []}

    # Embed the query
    query_vec = model.encode([query])
    query_vec = np.array(query_vec).astype("float32")

    # Search in FAISS
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
                "description": job.get("jobdescription", "N/A")[:400] + "...",
                "site": job.get("site_name", "N/A"),
                "post_date": job.get("postdate", "N/A"),
                "advertiser_url": job.get("advertiserurl", "N/A"),
                "shift": job.get("shift", "N/A"),
                "match_score": round(float(score), 3)
            })

    return {"matches": results}
