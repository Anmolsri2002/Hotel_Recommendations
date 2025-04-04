import sqlite3
import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class RAGSystem:
    def __init__(self, db_file: str = "hotel_bookings.db"):
        self.db_file = db_file
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = self._build_index()

    def _build_index(self):
        conn = sqlite3.connect(self.db_file)
        df = pd.read_sql_query("SELECT * FROM bookings", conn)
        conn.close()

        # Create text representations of each booking
        texts = df.apply(lambda row: f"Hotel: {row['hotel']}, Canceled: {row['is_canceled']}, "
                                     f"Revenue: {row['adr'] * row['total_stay']}, Country: {row['country']}, "
                                     f"Month: {row['arrival_date_month']}, Year: {row['arrival_date_year']}", axis=1)
        
        # Generate embeddings
        embeddings = self.model.encode(texts.tolist(), show_progress_bar=True)
        d = embeddings.shape[1]
        index = faiss.IndexFlatL2(d)
        index.add(embeddings)
        return index

    def query(self, question: str):
        # Encode the question
        q_embedding = self.model.encode([question])[0]

        # Search FAISS index
        D, I = self.index.search(np.array([q_embedding]), k=5)
        conn = sqlite3.connect(self.db_file)
        df = pd.read_sql_query("SELECT * FROM bookings", conn)
        conn.close()

        # Retrieve relevant rows
        relevant_data = df.iloc[I[0]]

        # Simulate LLM response (replace with actual LLM)
        if "total revenue" in question.lower() and "july 2017" in question.lower():
            july_2017 = relevant_data[(relevant_data['arrival_date_month'] == 'July') & 
                                      (relevant_data['arrival_date_year'] == 2017)]
            total = (july_2017['adr'] * july_2017['total_stay']).sum()
            return f"Total revenue for July 2017: ${total:.2f}"
        elif "highest booking cancellations" in question.lower():
            cancels = relevant_data[relevant_data['is_canceled'] == 1]['country'].value_counts()
            top = cancels.idxmax()
            return f"Location with highest cancellations: {top}"
        elif "average price" in question.lower():
            avg = relevant_data['adr'].mean()
            return f"Average price of a hotel booking: ${avg:.2f}"
        else:
            return "Sorry, I can't answer that question yet."

if __name__ == "__main__":
    rag = RAGSystem()
    print(rag.query("Show me total revenue for July 2017"))
    print(rag.query("Which locations had the highest booking cancellations?"))
    print(rag.query("What is the average price of a hotel booking?"))