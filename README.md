# INTVL FAQ Semantic Search

This project provides a **free, local, semantic search Q&A system** using:
- **SentenceTransformers** for embeddings
- **FAISS** for fast vector search
- **Exact duplicate caching**
- Logging of all questions and unanswered questions

---

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Build the search index:**
   ```bash
   python build_embeddings.py
   ```

3. **Start using the system:**
   ```bash
   python answer_questions.py
   ```

---

## Dependencies

Install the required packages:

```bash
pip install -r requirements.txt
```

**Required packages:**
- `sentence-transformers` - For generating text embeddings
- `faiss-cpu` - For fast vector similarity search
- `numpy` - For numerical operations
- Standard library: `json`, `os`, `datetime` (included with Python)

---

## Features

- Reads `intvl_faq.json` in format:
  ```json
  [
    {"question": "How is my country calculated?", "answer": "The country that you have done most of your runs in will become your country you represent for Terra!"},
    {"question": "Can I import my Strava runs to Terra?", "answer": "Strava don't allow runs to be sent from their platform to other platforms like INTVL. The Strava integration we have only allows us to send INTVL runs to Strava."}
  ]

- Reads `intvl_background.md` for extra information
- Answers user queries semantically
- Caches exact duplicates (cache.json)
- Logs:
    - all_questions.log → all queries
    - unanswered.log → questions needing manual review
- Fully free and runs locally (no OpenAI API costs)

---

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd INTVL
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare your data files:**
   - Use the existing `intvl_faq.json` with your FAQ data
   - Use the existing `intvl_background.md` with additional context
   - Or modify these files with your own content

4. **Build the search index:**
   ```bash
   python build_embeddings.py
   ```

---

## Usage

### Interactive Mode
Run the Q&A system interactively:
```bash
python answer_questions.py
```

### Programmatic Usage
```python
from answer_questions import get_answer

# Get answer with default threshold (0.6)
answer = get_answer("How is my country calculated?")

# Customize threshold and number of results
answer = get_answer("Can I import Strava runs?", threshold=0.5, top_k=3)
```

### Testing Thresholds
Test different similarity thresholds:
```bash
python test_threshold.py
```

---

## File Structure

```
INTVL/
├── README.md               # This documentation
├── requirements.txt        # Python dependencies
├── answer_questions.py     # Main Q&A interface
├── build_embeddings.py     # Build search index from FAQ/background
├── test_threshold.py       # Test similarity thresholds
├── intvl_faq.json         # FAQ data (questions & answers)
├── intvl_background.md     # Additional context information
├── faq.index              # FAISS vector index (generated)
├── metadata.json          # Index metadata (generated)
├── cache.json             # Question cache (generated)
├── all_questions.log      # All questions log
└── unanswered.log         # Unanswered questions log
```

---

## Configuration

### Similarity Threshold
- **Default**: 0.6 (lower = more strict matching)
- **Adjust**: Modify the `threshold` parameter in `get_answer()`
- **Test**: Use `test_threshold.py` to find optimal values

### Model
- **Default**: `all-MiniLM-L6-v2` (fast, good quality)
- **Change**: Modify the model name in the Python files

---

## Troubleshooting

**Common Issues:**
- **Index not found**: Run `python build_embeddings.py` first
- **Poor answers**: Lower the similarity threshold
- **Slow performance**: The first run downloads the model (~90MB)

**Logs:**
- Check `all_questions.log` for all interactions
- Check `unanswered.log` for questions needing review