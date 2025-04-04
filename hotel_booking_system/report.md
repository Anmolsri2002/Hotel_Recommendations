# Implementation Report

## Choices
- **Database**: SQLite for simplicity and lightweight storage.
- **Vector Store**: FAISS for fast similarity search.
- **API**: FastAPI for async support and ease of use.
- **LLM**: Simulated responses (replace with Llama 2 for production).

## Challenges
- Handling large datasets in FAISS required memory optimization.
- Date parsing inconsistencies in `reservation_status_date`.
- Limited LLM integration due to simulation; real LLM needs GPU support.