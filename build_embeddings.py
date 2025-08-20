import json
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

FAQ_PATH = "intvl_faq.json"
BG_PATH = "intvl_background.md"
INDEX_PATH = "faq.index"
META_PATH = "metadata.json"

def build_embeddings():
    """Build FAISS index from FAQ and background data"""
    
    # Load model
    print("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Load FAQ
    try:
        with open(FAQ_PATH, "r") as f:
            faq_data = json.load(f)
        print(f"Loaded {len(faq_data)} FAQ entries from {FAQ_PATH}")
    except Exception as e:
        print(f"Error loading {FAQ_PATH}: {e}")
        faq_data = []

    # Load background
    try:
        with open(BG_PATH, "r") as f:
            background_text = f.read()
        print(f"Loaded background from {BG_PATH}")
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
        return False

    # Embed all entries
    print(f"Embedding {len(entries)} entries...")
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
        print(f"Index saved to {INDEX_PATH}")
        print(f"Metadata saved to {META_PATH}")
        return True
    except Exception as e:
        print(f"Error saving index or metadata: {e}")
        return False

if __name__ == "__main__":
    success = build_embeddings()
    if success:
        print("\nEmbeddings built successfully!")
        print("You can now run: python answer_questions.py")
    else:
        print("\nFailed to build embeddings. Check the errors above.")
