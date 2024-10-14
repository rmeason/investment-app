import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor  # Using Random Forest for better performance
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler  # For normalization
import matplotlib.pyplot as plt

# Fetch historical crypto data from SQLite database
def fetch_data():
    conn = sqlite3.connect('investment.db')
    query = "SELECT time, price, sentiment_score FROM crypto"
    df = pd.read_sql(query, conn)
    conn.close()

    # Convert time to datetime
    df['time'] = pd.to_datetime(df['time'])
    print(f"Fetched {len(df)} rows of data.")
    return df

# Prepare the features and target for prediction
def prepare_data(df):
    # Convert time to datetime and create a numeric representation
    df['time'] = pd.to_datetime(df['time'])
    df['time_numeric'] = df['time'].apply(lambda x: x.timestamp())
    
    # Feature engineering
    # Adding a moving average as a new feature with a smaller window size
    df['moving_average'] = df['price'].rolling(window=3).mean()  # Reduced to 3-period moving average

    # Check for NaN values in each column
    print("NaN values before handling:")
    print(df.isna().sum())
    
    # Handling NaN values
    # Fill NaN sentiment scores with 0 (or you can use any other strategy)
    df['sentiment_score'] = df['sentiment_score'].fillna(0)
    
    # Drop rows with NaN values in moving average
    df = df.dropna(subset=['moving_average'])

    # Features and target
    X = df[['time_numeric', 'sentiment_score', 'moving_average']]
    y = df['price']
    
    # Check the shape of X
    print(f"Shape of features after handling NaNs: {X.shape}")
    
    # Ensure we have enough data to proceed
    if X.shape[0] < 1:
        raise ValueError("Feature set is empty. Cannot proceed with training.")

    # Normalize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Split data into train and test sets
    return train_test_split(X_scaled, y, test_size=0.2, random_state=42)


# Train the Random Forest model
def train_model(X_train, y_train):
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

# Evaluate the model and visualize the results
def evaluate_model(model, X_test, y_test):
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    print(f"Mean Squared Error: {mse}")
    
    # Plot the test data vs predictions
    plt.scatter(y_test, predictions, color='black')
    plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='blue', linewidth=2)  # Ideal prediction line
    plt.xlabel('Actual Prices')
    plt.ylabel('Predicted Prices')
    plt.title('Actual vs Predicted Crypto Prices')
    plt.show()

if __name__ == "__main__":
    # Fetch data for crypto
    df = fetch_data()
    
    if df.empty:
        print("No data found in the crypto table.")
    else:
        X_train, X_test, y_train, y_test = prepare_data(df)
        
        # Train the model and evaluate it
        model = train_model(X_train, y_train)
        evaluate_model(model, X_test, y_test)
