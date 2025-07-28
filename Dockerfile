FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download models with error handling
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')" || exit 1
RUN python -c "from transformers import pipeline, AutoTokenizer; pipeline('summarization', model='t5-small'); AutoTokenizer.from_pretrained('t5-small')" || exit 1

COPY . .

CMD ["python", "run.py"]