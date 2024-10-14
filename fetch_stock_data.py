import requests
import sqlite3
import logging

API_KEY = 'QJOE9YZYRIIWP7YT'
BASE_URL = 'https://www.alphavantage.co/query'

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_stock_data(symbol):
    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval': '5min',
        'apikey': API_KEY
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching stock data for {symbol}: {e}")
        return None

def save_stock_data(symbol, data, sentiment_score=None):
    if data is None or 'Time Series (5min)' not in data:
        logging.warning(f"No valid data to save for {symbol}.")
        return
    
    conn = sqlite3.connect('investment.db')
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS stocks
                      (symbol TEXT, time TEXT, price REAL, sentiment_score REAL)''')

    # Insert stock data
    for timestamp, values in data['Time Series (5min)'].items():
        price = values['1. open']
        cursor.execute("INSERT INTO stocks (symbol, time, price, sentiment_score) VALUES (?, ?, ?, ?)",
                       (symbol, timestamp, price, sentiment_score))

    conn.commit()
    conn.close()
    logging.info(f"Stock data for {symbol} saved successfully.")

if __name__ == "__main__":
    stock_symbols = ['AAPL', 'TSLA', 'AMZN']  # Apple, Tesla, Amazon
    sentiment_scores = {}  # Dictionary to hold sentiment scores for each symbol

    # Here you could fetch sentiment scores from your sentiment analysis script
    for symbol in stock_symbols:
        stock_data = get_stock_data(symbol)
        sentiment_score = sentiment_scores.get(symbol)  # Assume this comes from news sentiment analysis
        save_stock_data(symbol, stock_data, sentiment_score)
