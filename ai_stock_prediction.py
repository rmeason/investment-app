import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# Fetch historical stock data from SQLite database
def fetch_data(symbol):
    conn = sqlite3.connect('investment.db')
    query = f"SELECT time, price FROM stocks WHERE symbol = '{symbol}'"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Prepare the features and target for Linear Regression
def prepare_data(df):
    df['time'] = pd.to_datetime(df['time'])
    df['time_numeric'] = df['time'].apply(lambda x: x.timestamp())
    
    # Ensure price is numeric
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df = df.dropna()  # Drop rows with NaN values

    X = df[['time_numeric']]
    y = df['price']
    
    return train_test_split(X, y, test_size=0.2, random_state=42)

# Train the Linear Regression model
def train_model(X_train, y_train):
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model

# Evaluate the model and visualize the results
def evaluate_model(model, X_test, y_test):
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    print(f"Mean Squared Error: {mse}")
    
    # Plot the test data vs predictions
    plt.scatter(X_test, y_test, color='black', label='Actual Prices')
    plt.plot(X_test, predictions, color='blue', linewidth=2, label='Predicted Prices')
    plt.title('Stock Price Prediction')
    plt.xlabel('Time (Numeric)')
    plt.ylabel('Stock Price')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    # Fetch data for a stock symbol (e.g., 'AAPL')
    df = fetch_data('AAPL')
    if df.empty:
        print("No data found for the specified stock symbol.")
    else:
        X_train, X_test, y_train, y_test = prepare_data(df)
        model = train_model(X_train, y_train)
        evaluate_model(model, X_test, y_test)
