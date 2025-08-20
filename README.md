# INTVL FAQ Semantic Search

This project provides a **free, local, semantic search Q&A system** using:
- **SentenceTransformers** for embeddings
- **FAISS** for fast vector search
- **Exact duplicate caching**
- Logging of all questions and unanswered questions

---

## Quick Start

### 🌐 **Web App (Recommended)**
```bash
pip install -r requirements.txt
streamlit run app.py
```
Then open your browser to the provided URL!

### 💻 **Command Line**
1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Build the search index:**
   ```bash
   python src/build_embeddings.py
   ```

3. **Start using the system:**
   ```bash
   python src/answer_questions.py
   ```

**Or use the launcher script:**
```bash
python run.py
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

### 🌐 **Web Interface**
- **Beautiful Streamlit web app** with clean, modern UI
- **Real-time Q&A** - Type questions and get instant answers
- **Adjustable threshold slider** - Fine-tune answer strictness
- **Smart caching** - Only caches successful answers (no cache bloat)
- **Responsive design** - Works on desktop and mobile

### 🔍 **Core Functionality**
- Reads `intvl_faq.json` in format:
  ```json
  [
    {"question": "How is my country calculated?", "answer": "The country that you have done most of your runs in will become your country you represent for Terra!"},
    {"question": "Can I import my Strava runs to Terra?", "answer": "Strava don't allow runs to be sent from their platform to other platforms like INTVL. The Strava integration we have only allows us to send INTVL runs to Strava."}
  ]
- Reads `intvl_background.md` for extra information
- **Semantic search** using SentenceTransformers
- **Fast vector search** with FAISS
- **Smart logging** - Tracks all questions and unanswered ones
- **Fully free** and runs locally (no OpenAI API costs)

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

### 🌐 **Web App (Recommended)**
Launch the beautiful Streamlit web interface:
```bash
streamlit run app.py
```
- **Ask questions** in the text input
- **Adjust threshold** with the slider
- **Get instant answers** with real-time feedback

### 💻 **Command Line**
#### Interactive Mode
Run the Q&A system interactively:
```bash
python src/answer_questions.py
```

#### Programmatic Usage
```python
from answer_questions import get_answer

# Get answer with default threshold (0.7)
answer = get_answer("How is my country calculated?")

# Customize threshold and number of results
answer = get_answer("Can I import Strava runs?", threshold=0.5, top_k=3)
```

#### Testing Thresholds
Test different similarity thresholds:
```bash
python src/test_threshold.py
```

---

## File Structure

```
INTVL/
├── README.md               # This documentation
├── requirements.txt        # Python dependencies
├── app.py                  # 🌐 Streamlit web application
├── run.py                  # 💻 Command line launcher script
├── src/                    # Source code
│   ├── answer_questions.py # Main Q&A interface
│   ├── build_embeddings.py # Build search index
│   └── test_threshold.py   # Test similarity thresholds
├── data/                   # Input data files
│   ├── intvl_faq.json     # FAQ data (questions & answers)
│   └── intvl_background.md # Additional context information
├── generated/              # Auto-generated files
│   ├── faq.index          # FAISS vector index
│   ├── metadata.json      # Index metadata
│   └── cache.json         # Question cache
└── logs/                   # Log files
    ├── all_questions.log   # All questions log
    └── unanswered.log      # Unanswered questions log
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

## 🚀 **Deployment**

### **Streamlit Cloud (Free)**
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Deploy with one click!

### **Local Development**
```bash
# Install dependencies
pip install -r requirements.txt

# Run web app
streamlit run app.py

# Or run command line version
python run.py
```

---

## Troubleshooting

**Common Issues:**
- **Index not found**: Run `python src/build_embeddings.py` first
- **Poor answers**: Lower the similarity threshold
- **Slow performance**: The first run downloads the model (~90MB)
- **Web app not loading**: Make sure Streamlit is installed (`pip install streamlit`)

**Logs:**
- Check `logs/all_questions.log` for all interactions
- Check `logs/unanswered.log` for questions needing review