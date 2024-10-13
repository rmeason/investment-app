import schedule
import time
import fetch_stock_data
import fetch_crypto_data
import news_sentiment_analysis
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def job():
    logging.info("Fetching stock, crypto data, and sentiment...")

    stock_symbols = ['AAPL', 'TSLA', 'AMZN']
    for symbol in stock_symbols:
        stock_data = fetch_stock_data.get_stock_data(symbol)
        fetch_stock_data.save_stock_data(symbol, stock_data)

    crypto_symbols = ['bitcoin', 'ethereum', 'dogecoin']
    for symbol in crypto_symbols:
        crypto_data = fetch_crypto_data.get_crypto_data(symbol)
        fetch_crypto_data.save_crypto_data(symbol, crypto_data)

    news_queries = ['stocks', 'crypto', 'Tesla']
    news_texts = news_sentiment_analysis.fetch_news(news_queries)

    for query, news_text in news_texts.items():
        if news_text:  # Only analyze if news text is not empty
            news_sentiment = news_sentiment_analysis.get_news_sentiment(news_text)
            logging.info(f"NewsAPI Sentiment for {query}: {news_sentiment}")
            news_sentiment_analysis.save_news_sentiment_to_db(query, news_sentiment)

# Run the job initially and continue indefinitely
try:
    for _ in range(1):  # Change to a number for multiple iterations
        job()
        time.sleep(300)  # Wait for 5 minutes (300 seconds) before the next fetch
except KeyboardInterrupt:
    logging.info("\nData fetching stopped by user.")
