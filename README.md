# Hotel Booking System

## Setup
1. Clone the repo: `git clone <repo-url>`
2. Install dependencies: `pip install -r requirements.txt`
3. Preprocess data: `python src/preprocess.py`
4. Run the API: `python src/api.py`

## Usage
- Analytics: `curl -X POST http://localhost:8000/analytics`
- Ask a question: `curl -X POST -d '{"question": "Show me total revenue for July 2017"}' http://localhost:8000/ask`
