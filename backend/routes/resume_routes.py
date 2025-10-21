from fastapi import APIRouter, UploadFile, File, HTTPException
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import json
from io import BytesIO
from PyPDF2 import PdfReader
import docx
from backend.models.preprocess import clean_text

router = APIRouter()

# ---------------- Load model and FAISS index ----------------
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
INDEX_PATH = "backend/data/job_embeddings.faiss"
META_PATH = "backend/data/job_meta.jsonl"

try:
    model = SentenceTransformer(MODEL_NAME)
    index = faiss.read_index(INDEX_PATH)
    print("✅ Model and FAISS index loaded successfully")
except Exception as e:
    print("❌ Error loading model or FAISS index:", e)
    raise e

# Load job metadata
jobs = []
try:
    with open(META_PATH, "r", encoding="utf-8") as f:
        for line in f:
            jobs.append(json.loads(line))
    print(f"✅ Loaded {len(jobs)} job entries from metadata")
except Exception as e:
    print("❌ Error loading job metadata:", e)
    raise e

# ---------------- PDF Extraction ----------------
def extract_text_from_pdf(file_bytes):
    try:
        pdf_file = BytesIO(file_bytes)
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        if not text.strip():
            raise ValueError("No extractable text found in PDF.")
        return text
    except Exception as e:
        raise ValueError(f"Failed to extract text from PDF: {e}")

# ---------------- DOCX Extraction ----------------
def extract_text_from_docx(file_bytes):
    try:
        doc = docx.Document(BytesIO(file_bytes))
        text = ""
        for para in doc.paragraphs:
            if para.text.strip():
                text += para.text + "\n"
        if not text.strip():
            raise ValueError("No extractable text found in DOCX.")
        return text
    except Exception as e:
        raise ValueError(f"Failed to extract text from DOCX: {e}")

# ---------------- Resume Matching ----------------
@router.post("/match_resume")
async def match_resume(resume: UploadFile = File(...), top_k: int = 5):
    try:
        # Step 1: Read file bytes
        file_content = await resume.read()
        filename = resume.filename.lower()

        # Step 2: Extract text depending on file type
        if filename.endswith(".pdf"):
            text = extract_text_from_pdf(file_content)
        elif filename.endswith(".docx"):
            text = extract_text_from_docx(file_content)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type. Use PDF or DOCX.")

        # Step 3: Preprocess text
        text = clean_text(text)

        # Step 4: Embed resume
        query_vec = model.encode([text])
        query_vec = np.array(query_vec).astype("float32")

        # Step 5: Query FAISS
        D, I = index.search(query_vec, top_k)

        # Step 6: Prepare results
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

        return {"matches": results}

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        print("❌ Error in match_resume:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
