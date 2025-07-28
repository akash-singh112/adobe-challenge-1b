# Adobe Challenge - Document Analysis System

A sophisticated document analysis system that uses semantic similarity to extract and rank relevant content from PDF documents based on user personas and tasks.

## Important note:

The model is too large for GitHub. So it is required to download the relevant model for classification, from this drive link:

https://drive.google.com/drive/folders/1dsqwooYBVYgPWuWJOVcF2c8ML2julN7m?usp=drive_link

and place it at the root of the project.

## 🚀 Features

- **PDF Text Extraction**: Intelligent extraction with header/footer removal
- **Semantic Analysis**: Uses sentence transformers for content relevance ranking
- **Multi-document Processing**: Handles multiple PDFs simultaneously
- **Persona-based Filtering**: Tailors content selection based on user roles and objectives
- **Dockerized Deployment**: Fully containerized with offline model support

## 📁 Project Structure

```
adobe-challenge/
├── semantic_heading_ranker/          # Pre-trained model directory
├── input_1b_pdfs/                   # Input PDF files
├── input_1b_json/                   # Input configuration files
├── headings_classified/              # Extracted headings and structure
├── output/                          # Generated analysis results
├── temp/                            # Temporary processing files
├── app.py                           # Main application logic
├── hf.py                            # PDF processing and text extraction
├── utils.py                         # Utility functions
├── Dockerfile                       # Docker configuration
├── requirements-docker.txt          # Docker dependencies
└── requirements.txt                 # Full dependencies

### Docker Deployment

1. **Build the Docker image**

   ```bash
   docker build -t adobe-challenge .
   ```

2. **Run the container**
   ```bash
   docker run -d --name adobe-challenge-work -v "%cd%\input_1b_pdfs":/app/input_1b_pdfs -v "%cd%\input_1b_json":/app/input_1b_json -v "%cd%\output":/app/output -v "%cd%\headings_classified":/app/headings_classified adobe-challenge sleep infinity
   ```

## 🎯 Usage

### Input Format

**PDF Documents**: Place your PDF files in `input_1b_pdfs`

**Output of 1a**: Place the output of 1a in `headings_classified`

**Configuration JSON**: Create input files in `input_1b_json` with this structure:

```json
{
  "challenge_info": {
    "challenge_id": "round_1b_002",
    "test_case_name": "travel_planner",
    "description": "France Travel"
  },
  "documents": [
    {
      "filename": "document1.pdf",
      "title": "Document 1 Title"
    }
  ],
  "persona": {
    "role": "Travel Planner"
  },
  "job_to_be_done": {
    "task": "Plan a trip of 4 days for a group of 10 college friends."
  }
}
```

### Running the Analysis (Inside docker container)

1. **Process PDFs and extract structure**

   ```bash
   docker exec adobe-challenge-work python hf.py
   ```

2. **Run semantic analysis**

   ```bash
   docker exec adobe-challenge-work python app.py
   ```

3. **Check results** in `output/output.json`

### Output Format

The system generates structured output with:

- **Metadata**: Input documents, persona, task, and timestamp
- **Extracted Sections**: Top-ranked sections with importance rankings
- **Subsection Analysis**: Refined text content with page numbers

Example output:

```json
{
  "metadata": {
    "input_documents": ["document1.pdf"],
    "persona": "Travel Planner",
    "job_to_be_done": "Plan a trip of 4 days for a group of 10 college friends.",
    "processing_timestamp": "2025-01-27T15:31:22.632389"
  },
  "extracted_sections": [
    {
      "document": "document1.pdf",
      "section_title": "Coastal Adventures",
      "importance_rank": 1,
      "page_number": 2
    }
  ],
  "subsection_analysis": [
    {
      "document": "document1.pdf",
      "refined_text": "Content text here...",
      "page_number": 2
    }
  ]
}
```

## 🔧 Configuration

### Model Configuration

The system uses `semantic_heading_ranker` - a sentence transformer model for semantic similarity. You can customize by:

1. Using different models in `app.py`:

   ```python
   model = SentenceTransformer('your-model-name')
   ```

2. Adjusting the number of top results:
   ```python
   k = 5  # Number of top-ranked sections to return
   ```

### Docker Configuration

Key environment variables in `Dockerfile`:

- `TRANSFORMERS_OFFLINE=1`: Use offline models only
- `HF_DATASETS_OFFLINE=1`: Prevent online dataset downloads
- `PYTHONUNBUFFERED=1`: Enable real-time logging

## 🧪 Sample Data

The repository includes sample data for the South of France travel planning scenario:

- **Sample Input**: `sample_input.json`
- **Sample Output**: `sample_output.json`
- **Test PDFs**: Various South of France travel guides

## 🏗 Architecture

### Core Components

1. **PDF Processing** (`hf.py`)

   - Text extraction with pdfplumber
   - Header/footer removal
   - Heading structure analysis

2. **Semantic Analysis** (`app.py`)

   - Sentence transformer embeddings
   - Cosine similarity ranking
   - Top-k content selection

3. **Utilities** (`utils.py`)
   - Content mapping and organization
   - Output formatting
   - Data structure helpers

### Technology Stack

- **Python 3.11**: Core runtime
- **sentence-transformers**: Semantic similarity
- **pdfplumber**: PDF text extraction
- **Docker**: Containerization
- **PyTorch**: Neural network backend

## 🚀 Performance

- **Processing Speed**: ~2-5 seconds per document analysis
- **Memory Usage**: ~500MB

## 📝 License

This project is part of the Adobe Challenge submission.

---

\*\*Built with ❤️ for Adobe
