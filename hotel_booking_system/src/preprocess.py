import pandas as pd
import sqlite3
from pathlib import Path

def preprocess_data(input_file: str, db_file: str = "hotel_bookings.db"):
    # Load the dataset
    df = pd.read_csv(input_file)

    # Handle missing values
    df['children'] = df['children'].fillna(0).astype(int)
    df['babies'] = df['babies'].fillna(0).astype(int)
    df['country'] = df['country'].fillna('Unknown')
    df['agent'] = df['agent'].fillna(0).astype(int)
    df['company'] = df['company'].fillna(0).astype(int)

    # Convert date columns
    df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'], format='%d-%m-%y', errors='coerce')

    # Create a total stay column
    df['total_stay'] = df['stays_in_weekend_nights'] + df['stays_in_week_nights']

    # Store in SQLite database
    conn = sqlite3.connect(db_file)
    df.to_sql('bookings', conn, if_exists='replace', index=False)
    conn.close()

    return df

if __name__ == "__main__":
    input_file = Path("data/hotel_bookings.csv")
    preprocess_data(input_file)