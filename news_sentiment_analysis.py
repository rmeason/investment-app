from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from newsapi import NewsApiClient
import sqlite3
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Initialize NewsAPI client (replace with your API key)
newsapi = NewsApiClient(api_key='c60befc2419f4dac9ab56e49da4ffaa1')

def get_news_sentiment(news_text):
    sentiment = analyzer.polarity_scores(news_text)
    return sentiment

def fetch_news(queries):
    news_texts = {}
    for query in queries:
        logging.info(f"Fetching news for: {query}")
        try:
            news = newsapi.get_everything(q=query, language='en', sort_by='relevancy', page_size=5)
            articles = news['articles']
            news_text = ''.join(f"{article['title']}: {article['description']}\n" for article in articles)
            news_texts[query] = news_text
        except Exception as e:
            logging.error(f"Error fetching news for {query}: {e}")
            news_texts[query] = ''
    
    return news_texts

def save_news_sentiment_to_db(query, sentiment):
    conn = sqlite3.connect('investment.db')
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS news_sentiments
                      (query TEXT, sentiment_score REAL, time TEXT)''')

    sentiment_score = sentiment['compound']
    cursor.execute("INSERT INTO news_sentiments (query, sentiment_score, time) VALUES (?, ?, datetime('now'))",
                   (query, sentiment_score))

    conn.commit()
    conn.close()
    logging.info(f"Sentiment for {query} saved successfully.")

if __name__ == "__main__":
    news_queries = ['stocks', 'crypto', 'Tesla']
    news_texts = fetch_news(news_queries)
    
    for query, news_text in news_texts.items():
        if news_text:  # Only analyze if news text is not empty
            sentiment_score = get_news_sentiment(news_text)
            logging.info(f"Sentiment score for {query}: {sentiment_score}")
            save_news_sentiment_to_db(query, sentiment_score)
        else:
            logging.warning(f"No news text available for sentiment analysis for {query}.")
