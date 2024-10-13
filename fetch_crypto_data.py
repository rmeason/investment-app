import requests
import sqlite3
import logging

COINGECKO_URL = 'https://api.coingecko.com/api/v3/simple/price'

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_crypto_data(crypto):
    params = {
        'ids': crypto,
        'vs_currencies': 'usd'
    }
    
    try:
        response = requests.get(COINGECKO_URL, params=params)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching crypto data for {crypto}: {e}")
        return None

def save_crypto_data(crypto, data):
    if data is None or crypto not in data:
        logging.warning(f"No valid data to save for {crypto}.")
        return
    
    conn = sqlite3.connect('investment.db')
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS crypto
                      (name TEXT, time TEXT, price REAL)''')

    # Insert crypto data
    price = data[crypto]['usd']
    cursor.execute("INSERT INTO crypto (name, time, price) VALUES (?, datetime('now'), ?)",
                   (crypto, price))

    conn.commit()
    conn.close()
    logging.info(f"Crypto data for {crypto} saved successfully.")

if __name__ == "__main__":
    crypto_symbols = ['bitcoin', 'ethereum', 'dogecoin']  # BTC, ETH, DOGE
    for symbol in crypto_symbols:
        crypto_data = get_crypto_data(symbol)
        save_crypto_data(symbol, crypto_data)
