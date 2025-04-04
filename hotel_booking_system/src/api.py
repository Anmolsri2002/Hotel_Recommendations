from fastapi import FastAPI
from pydantic import BaseModel
from analytics import generate_analytics
from rag import RAGSystem
from preprocess import preprocess_data
from pathlib import Path

app = FastAPI()

# Preprocess data on startup
preprocess_data(Path("data/hotel_bookings.csv"))
rag_system = RAGSystem()

class Question(BaseModel):
    question: str

@app.post("/analytics")
async def get_analytics():
    return generate_analytics()

@app.post("/ask")
async def ask_question(q: Question):
    response = rag_system.query(q.question)
    return {"answer": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)