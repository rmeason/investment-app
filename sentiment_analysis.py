from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import requests


analyzer = SentimentIntensityAnalyzer()

def get_news_sentiment(news_text):
    sentiment = analyzer.polarity_scores(news_text)
    return sentiment

def fetch_news():
    # Fetch news from an API (replace with a real news API)
    return "Stocks are up today due to positive earnings reports!"

if __name__ == "__main__":
    news_text = fetch_news()
    sentiment_score = get_news_sentiment(news_text)
    print(f"Sentiment score for the news: {sentiment_score}")
