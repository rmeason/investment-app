import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt

# Fetch sentiment data from SQLite database
def fetch_data():
    conn = sqlite3.connect('investment.db')
    query = "SELECT query, sentiment_score FROM news_sentiments"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Prepare the features and target for Logistic Regression
def prepare_data(df):
    X = df[['sentiment_score']]
    y = (df['sentiment_score'] > 0).astype(int)  # 1 if positive sentiment, 0 otherwise
    return train_test_split(X, y, test_size=0.2, random_state=42)

# Train the Logistic Regression model
def train_model(X_train, y_train):
    model = LogisticRegression()
    model.fit(X_train, y_train)
    return model

# Evaluate the model
def evaluate_model(model, X_test, y_test):
    predictions = model.predict(X_test)
    print(classification_report(y_test, predictions))

if __name__ == "__main__":
    # Fetch sentiment data
    df = fetch_data()
    
    # Check if the DataFrame is empty
    if df.empty:
        print("No data found in the news_sentiments table.")
    else:
        # Print fetched data for debugging
        print("Fetched Data:\n", df.head())
        
        X_train, X_test, y_train, y_test = prepare_data(df)
        
        # Train the model and evaluate it
        model = train_model(X_train, y_train)
        evaluate_model(model, X_test, y_test)
