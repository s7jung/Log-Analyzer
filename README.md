# Log Root Cause Analyzer

Python 3.10+ recommended.

## Setup

```bash
# From project root
python3 -m venv .venv
source .venv/bin/activate 

# Install dependencies
pip install -r requirements.txt
```

## Run

**Always run from the project root** so the `app` package is found:

```bash
uvicorn app.main:app --reload
```

- API: http://127.0.0.1:8000  
- Health: http://127.0.0.1:8000/api/v1/health  
- Docs: http://127.0.0.1:8000/docs  
