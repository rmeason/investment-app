import schedule
import time
import fetch_stock_data
import fetch_crypto_data
import news_sentiment_analysis
import logging
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@retry(stop_max_attempt_number=3, wait_fixed=2000)
def fetch_data():
    """Fetch stock, crypto, and news sentiment data."""
    logging.info("Fetching stock, crypto data, and sentiment...")

    stock_symbols = ['AAPL', 'TSLA', 'AMZN']
    for symbol in stock_symbols:
        try:
            stock_data = fetch_stock_data.get_stock_data(symbol)
            fetch_stock_data.save_stock_data(symbol, stock_data)
            logging.info(f"Fetched stock data for {symbol}: {stock_data}")
        except Exception as e:
            logging.error(f"Failed to fetch or save stock data for {symbol}: {e}")

    crypto_symbols = ['bitcoin', 'ethereum', 'dogecoin']
    for symbol in crypto_symbols:
        try:
            crypto_data = fetch_crypto_data.get_crypto_data(symbol)
            fetch_crypto_data.save_crypto_data(symbol, crypto_data)
            logging.info(f"Fetched crypto data for {symbol}: {crypto_data}")
        except Exception as e:
            logging.error(f"Failed to fetch or save crypto data for {symbol}: {e}")

    news_queries = ['stocks', 'crypto', 'Tesla']
    news_texts = news_sentiment_analysis.fetch_news(news_queries)

    for query, news_text in news_texts.items():
        if news_text:  # Only analyze if news text is not empty
            try:
                news_sentiment = news_sentiment_analysis.get_news_sentiment(news_text)
                logging.info(f"NewsAPI Sentiment for {query}: {news_sentiment}")
                news_sentiment_analysis.save_news_sentiment_to_db(query, news_sentiment)
            except Exception as e:
                logging.error(f"Failed to analyze sentiment for {query}: {e}")

def job():
    """Job to fetch data at scheduled intervals."""
    fetch_data()

# Schedule the job
schedule.every(5).minutes.do(job)

# Run the job initially and continue indefinitely
if __name__ == "__main__":
    logging.info("Starting the data fetching job...")
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)  # Sleep to prevent busy waiting
    except KeyboardInterrupt:
        logging.info("\nData fetching stopped by user.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
