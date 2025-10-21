# notebooks/build_faiss_index.py
import os
import json
import numpy as np
import pandas as pd
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
import faiss
import re
import html

# ==== CONFIG ====
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
DATA_PATH = "backend/data/jobs.csv"  # <-- path to your Kaggle file
OUT_DIR = "backend/data/"
FAISS_INDEX_PATH = os.path.join(OUT_DIR, "job_embeddings.faiss")
META_PATH = os.path.join(OUT_DIR, "job_meta.jsonl")
IDS_PATH = os.path.join(OUT_DIR, "job_ids.npy")



os.makedirs(OUT_DIR, exist_ok=True)

# ==== HELPERS ====
def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = html.unescape(text)
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

# ==== 1) LOAD DATA ====
df = pd.read_csv(DATA_PATH)
df = df.fillna("")

# Rename for simplicity
df.rename(columns={
    "jobtitle": "title",
    "company": "company",
    "jobdescription": "description",
    "skills": "skills"
}, inplace=True)

print("Columns:", df.columns.tolist())
print(f"Loaded {len(df)} job postings")

# ==== 2) CREATE TEXT FIELD ====
def make_text(row):
    parts = []
    if row.get("title"):
        parts.append(str(row["title"]))
    if row.get("company"):
        parts.append("Company: " + str(row["company"]))
    if row.get("description"):
        parts.append(row["description"])
    if row.get("skills"):
        parts.append("Skills: " + str(row["skills"]))
    if row.get("joblocation_address"):
        parts.append("Location: " + str(row["joblocation_address"]))
    return " | ".join(parts)

df["text"] = df.apply(make_text, axis=1)
df["text"] = df["text"].apply(clean_text)

# Optional: reduce data if huge
# df = df.sample(n=50000, random_state=42)

# ==== 3) LOAD MODEL ====
model = SentenceTransformer(MODEL_NAME)
embed_dim = model.get_sentence_embedding_dimension()
print("Embedding dimension:", embed_dim)

# ==== 4) ENCODE TEXT ====
BATCH = 64
embeddings = np.zeros((len(df), embed_dim), dtype="float32")
for i in tqdm(range(0, len(df), BATCH)):
    texts = df["text"].iloc[i:i+BATCH].tolist()
    embs = model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
    embeddings[i:i+BATCH] = embs

# ==== 5) NORMALIZE (cosine similarity via inner product) ====
def normalize_rows(x):
    norms = np.linalg.norm(x, axis=1, keepdims=True)
    norms[norms==0] = 1.0
    return x / norms

embeddings = normalize_rows(embeddings)

# ==== 6) BUILD FAISS INDEX ====
index = faiss.IndexFlatIP(embed_dim)
index.add(embeddings)

# ==== 7) SAVE EVERYTHING ====
faiss.write_index(index, FAISS_INDEX_PATH)
np.save(IDS_PATH, np.arange(len(df)))

with open(META_PATH, "w", encoding="utf8") as fout:
    for i, row in df.iterrows():
        meta = {
            "idx": int(i),
            "advertiserurl": row.get("advertiserurl", ""),
            "company": row.get("company", ""),
            "employmenttype_jobstatus": row.get("employmenttype_jobstatus", ""),
            "jobdescription": row.get("description", ""),
            "jobid": row.get("jobid", ""),
            "joblocation_address": row.get("joblocation_address", ""),
            "jobtitle": row.get("title", ""),
            "postdate": row.get("postdate", ""),
            "shift": row.get("shift", ""),
            "site_name": row.get("site_name", ""),
            "skills": row.get("skills", ""),
            "uniq_id": row.get("uniq_id", ""),
            "text": row.get("text", "")
        }
        fout.write(json.dumps(meta, ensure_ascii=False) + "\n")


print(f"✅ Saved index to {FAISS_INDEX_PATH}")
print(f"✅ Saved metadata to {META_PATH}")
