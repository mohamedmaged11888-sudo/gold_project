import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, r2_score

def train_and_compare(file_path):
    # 1. Load Data
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')

    # 2. Feature Engineering (The "clues" for the ML)
    # We want to predict tomorrow's price using today's data
    df['Target'] = df['Close'].shift(-1) # Move price up by 1 row
    
    # Use features that actually affect price
    features = ['Close', 'Open', 'High', 'Low', 'Volume', 'MA_7', 'MA_30']
    X = df[features][:-1] # Everything except the last row
    y = df['Target'][:-1]

    # 3. Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 4. The Competition
    models = {
        "Linear Regression": LinearRegression(),
        "Random Forest": RandomForestRegressor(n_estimators=100),
        "XGBoost": XGBRegressor()
    }

    results = {}
    print("🤖 --- MODEL TRAINING COMPETITION ---")
    for name, model in models.items():
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        score = r2_score(y_test, predictions)
        results[name] = score
        print(f"{name} Accuracy (R2 Score): {score:.4f}")

    best_model_name = max(results, key=results.get)
    print(f"\n🏆 WINNER: {best_model_name}")
    return models[best_model_name], features

if __name__ == "__main__":
    best_model, feature_list = train_and_compare('gold_prices_cleaned.csv')