import json
import os
import datetime
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Updated paths for new folder structure
INDEX_PATH = "generated/faq.index"
META_PATH = "generated/metadata.json"
CACHE_PATH = "generated/cache.json"
ALL_LOG = "logs/all_questions.log"
UNANSWERED_LOG = "logs/unanswered.log"

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load FAISS index
try:
    index = faiss.read_index(INDEX_PATH)
except Exception as e:
    print(f"Error loading index: {e}")
    exit()

# Load metadata
try:
    with open(META_PATH, "r") as f:
        metadata = json.load(f)
except Exception as e:
    print(f"Error loading metadata: {e}")
    metadata = []

# Load or initialize cache
if os.path.exists(CACHE_PATH):
    try:
        with open(CACHE_PATH, "r") as f:
            cache = json.load(f)
    except Exception:
        cache = {}
else:
    cache = {}

# Logging helper
def log_question(question, answer, status):
    # Fixed: Use timezone-aware UTC time instead of deprecated utcnow()
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    try:
        with open(ALL_LOG, "a") as f:
            f.write(f"{timestamp} | Q: {question} | A: {answer} | Status: {status}\n")
    except Exception as e:
        print(f"Error logging question: {e}")
    if status == "unanswered":
        try:
            with open(UNANSWERED_LOG, "a") as f:
                f.write(f"{timestamp} | {question}\n")
        except Exception as e:
            print(f"Error logging unanswered question: {e}")

# Main answer function
def get_answer(user_q, threshold=0.7, top_k=1):
    user_q = user_q.strip()
    if not user_q:
        return "Please ask a non-empty question."

    # Check exact duplicate cache
    if user_q in cache:
        answer = cache[user_q]
        log_question(user_q, answer, "cache")
        return answer

    # Check if metadata is available
    if not metadata:
        return "Error: No FAQ data available. Please run build_embeddings.py first."

    # Embed query
    q_vec = model.encode([user_q], convert_to_numpy=True)
    D, I = index.search(q_vec, top_k)
    best_idx = I[0][0]
    best_distance = D[0][0]

    # Decide answer based on distance threshold
    if best_distance < threshold:
        # Fixed: Add bounds checking for metadata access
        if best_idx < len(metadata):
            entry = metadata[best_idx]
            if entry["type"] == "faq":
                answer = entry.get("answer", "No answer found.")
            else:
                answer = entry.get("content", "(From background) No answer found.")[:300]
            status = "answered"
        else:
            answer = "Error: Invalid metadata index. Please rebuild embeddings."
            status = "error"
    else:
        answer = "I'm not sure about that. We'll forward your question to the team."
        status = "unanswered"

    # Update cache only for answered questions
    if status == "answered":
        cache[user_q] = answer
        try:
            with open(CACHE_PATH, "w") as f:
                json.dump(cache, f)
        except Exception as e:
            print(f"Error updating cache: {e}")

    # Log
    log_question(user_q, answer, status)
    return answer

# Interactive loop
if __name__ == "__main__":
    print("Ready. Type 'quit' to exit.")
    while True:
        q = input("Ask a question: ")
        if q.lower() == "quit":
            break
        print("Answer:", get_answer(q))
