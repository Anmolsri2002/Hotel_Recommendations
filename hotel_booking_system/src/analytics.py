import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from pathlib import Path

def load_data(db_file: str = "hotel_bookings.db"):
    conn = sqlite3.connect(db_file)
    df = pd.read_sql_query("SELECT * FROM bookings", conn)
    conn.close()
    return df

def revenue_trends(df):
    df['arrival_date'] = pd.to_datetime(df['arrival_date_year'].astype(str) + '-' + 
                                        df['arrival_date_month'] + '-01')
    df['revenue'] = df['adr'] * df['total_stay']
    monthly_revenue = df.groupby(df['arrival_date'].dt.to_period('M'))['revenue'].sum()
    
    plt.figure(figsize=(10, 6))
    monthly_revenue.plot()
    plt.title('Revenue Trends Over Time')
    plt.xlabel('Month')
    plt.ylabel('Revenue')
    plt.savefig('revenue_trends.png')
    return monthly_revenue.to_dict()

def cancellation_rate(df):
    total_bookings = len(df)
    cancellations = df['is_canceled'].sum()
    rate = (cancellations / total_bookings) * 100
    return {"cancellation_rate": rate, "total_bookings": total_bookings, "cancellations": cancellations}

def geographical_distribution(df):
    country_counts = df['country'].value_counts().head(10)
    return country_counts.to_dict()

def lead_time_distribution(df):
    lead_time_stats = df['lead_time'].describe().to_dict()
    plt.figure(figsize=(10, 6))
    df['lead_time'].hist(bins=50)
    plt.title('Lead Time Distribution')
    plt.xlabel('Lead Time (days)')
    plt.ylabel('Frequency')
    plt.savefig('lead_time_distribution.png')
    return lead_time_stats

def generate_analytics():
    df = load_data()
    analytics = {
        "revenue_trends": revenue_trends(df),
        "cancellation_rate": cancellation_rate(df),
        "geographical_distribution": geographical_distribution(df),
        "lead_time_distribution": lead_time_distribution(df)
    }
    return analytics

if __name__ == "__main__":
    analytics = generate_analytics()
    print(analytics)