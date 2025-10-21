# notebooks/test_search.py
import faiss, numpy as np, json
from sentence_transformers import SentenceTransformer
from preprocess import clean_text

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
INDEX_PATH = "backend/data/job_embeddings.faiss"
META_PATH = "backend/data/job_meta.jsonl"

model = SentenceTransformer(MODEL_NAME)
index = faiss.read_index(INDEX_PATH)

# load meta
meta = []
with open(META_PATH, "r", encoding="utf8") as f:
    for line in f:
        meta.append(json.loads(line))

def normalize(v):
    import numpy as np
    v = v.astype("float32")
    n = np.linalg.norm(v)
    if n==0: 
        return v
    return v / n

def query(text, topk=5):
    text = clean_text(text)
    v = model.encode([text], convert_to_numpy=True)
    v = normalize(v)
    D, I = index.search(v, topk)
    results = []
    for score, idx in zip(D[0], I[0]):
        results.append({"score": float(score), "meta": meta[int(idx)]})
    return results

if __name__ == "__main__":
    q = "MERN developer with Node.js, Express, MongoDB, React, experience in REST APIs"
    res = query(q, topk=5)
    import pprint; pprint.pprint(res)
