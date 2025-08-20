import json
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# File to help tune threshold

FAQ_PATH = "intvl_faq.json"  # Fixed: match build_embeddings.py
BG_PATH = "intvl_background.md"  # Fixed: match build_embeddings.py
INDEX_PATH = "faq.index"
META_PATH = "metadata.json"

def test_thresholds():
    """Test different similarity thresholds with sample questions"""
    
    # Load model
    print("Loading model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    
    # Load FAQ
    try:
        with open(FAQ_PATH, "r") as f:
            faq_data = json.load(f)
    except Exception as e:
        print(f"Error loading {FAQ_PATH}: {e}")
        faq_data = []

    # Load background
    try:
        with open(BG_PATH, "r") as f:
            background_text = f.read()
    except Exception as e:
        print(f"Error loading {BG_PATH}: {e}")
        background_text = ""

    # Prepare entries
    entries = []
    metadata = []

    # Add FAQ Q&A
    for item in faq_data:
        q = item.get("question", "").strip()
        a = item.get("answer", "").strip()
        if q and a:
            entries.append(q + " " + a)
            metadata.append({"type": "faq", "question": q, "answer": a})

    # Add background as one entry
    if background_text.strip():
        entries.append(background_text.strip())
        metadata.append({"type": "background", "content": background_text.strip()})

    if not entries:
        print("No entries to embed. Exiting.")
        return

    # Embed all entries
    print("Embedding entries...")
    embeddings = model.encode(entries, convert_to_numpy=True)

    # Build FAISS index
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    # Save index and metadata
    try:
        faiss.write_index(index, INDEX_PATH)
        with open(META_PATH, "w") as f:
            json.dump(metadata, f)
        print(f"Index built and saved with {len(entries)} entries.")
    except Exception as e:
        print(f"Error saving index or metadata: {e}")
        return

    # Test different thresholds
    print("\n" + "="*50)
    print("TESTING DIFFERENT THRESHOLDS")
    print("="*50)
    
    test_questions = [
        "How is my country calculated?",
        "Can I import my Strava runs?",
        "What is Terra?",
        "How does the platform work?",
        "I can't add my run from garmin to strava",
        "How to add run from garmin to strava",
        "add run garmin strava",
        "how to add run to strava?",
        "how to add run from strava?",
        "What is INTVL?",
        "Why are my runs not showing up?",
        "Why are my runs not uploading?"
    ]
    
    thresholds = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
    
    for question in test_questions:
        print(f"\nQuestion: {question}")
        print("-" * 40)
        
        # Embed the question
        q_vec = model.encode([question], convert_to_numpy=True)
        D, I = index.search(q_vec, 1)
        best_idx = I[0][0]
        best_distance = D[0][0]
        
        print(f"Best match distance: {best_distance:.4f}")
        
        for threshold in thresholds:
            if best_distance < threshold:
                entry = metadata[best_idx]
                if entry["type"] == "faq":
                    answer = entry.get("answer", "No answer found.")
                else:
                    answer = entry.get("content", "(From background) No answer found.")[:100] + "..."
                print(f"  Threshold {threshold}: ANSWERED - {answer}")
            else:
                print(f"  Threshold {threshold}: UNANSWERED")

if __name__ == "__main__":
    test_thresholds()
