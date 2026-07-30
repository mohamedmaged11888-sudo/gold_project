import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from sklearn.linear_model import LinearRegression
import datetime

# --- SETTINGS & STYLE ---
# 1. Added Gold Coin 🪙 to the Browser Tab (favicon)
st.set_page_config(page_title="Gold Investment AI", page_icon="🪙", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stButton>button { background-color: #ffd700; color: black; font-weight: bold; width: 100%; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- DATA ENGINE ---
@st.cache_data(ttl=3600)
def get_live_data():
    file_name = 'gold_prices_cleaned.csv'
    df = pd.read_csv(file_name)
    df['Date'] = pd.to_datetime(df['Date'])
    
    try:
        gold_ticker = yf.Ticker("GC=F")
        df_new = gold_ticker.history(period="1mo")
        if not df_new.empty:
            df_new = df_new.reset_index()
            df_new['Date'] = df_new['Date'].dt.tz_localize(None)
            df_new = df_new[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
            df = pd.concat([df, df_new]).drop_duplicates(subset=['Date'], keep='last')
            df.to_csv(file_name, index=False)
    except Exception as e:
        st.sidebar.warning("Live sync unavailable. Using cached data.")
    
    df = df.sort_values('Date')
    df['MA_7'] = df['Close'].rolling(window=7).mean()
    df['MA_30'] = df['Close'].rolling(window=30).mean()
    return df

def train_model(df):
    df_train = df.copy().dropna()
    df_train['Target'] = df_train['Close'].shift(-1)
    df_train = df_train.dropna()
    features = ['Close', 'Open', 'High', 'Low', 'MA_7', 'MA_30']
    model = LinearRegression()
    model.fit(df_train[features], df_train['Target'])
    return model

full_df = get_live_data()
model = train_model(full_df)
last_price = full_df['Close'].iloc[-1]

# --- SIDEBAR: USER INPUTS ---
# 2. Added Money Emoji 💰 behind "Investment Planner"
st.sidebar.header("💰 Investment Planner")
invest_amount = st.sidebar.number_input("Amount to Invest ($)", min_value=10.0, value=1000.0, step=100.0)
duration_months = st.sidebar.slider("Investment Duration (Months)", 1, 36, 12)

st.sidebar.divider()
st.sidebar.subheader("🎨 Chart Design")
hist_color = st.sidebar.color_picker("History Line Color", "#FFD700")
actual_color = st.sidebar.color_picker("Actual Price Color", "#2c3e50")
pred_color = st.sidebar.color_picker("AI Prediction Color", "#FF0000")

# --- CALCULATIONS ---
recent_data = full_df.tail(365)
avg_daily_return = recent_data['Close'].pct_change().mean()
monthly_growth = avg_daily_return * 21 
expected_return_pct = ((1 + monthly_growth) ** duration_months) - 1
final_value = invest_amount * (1 + expected_return_pct)

# --- MAIN DASHBOARD ---
st.title("💰 Gold Investment AI Predictor")
st.info(f"Live Gold Price: **${last_price:,.2f}** | Last Data Sync: {full_df['Date'].max().strftime('%Y-%m-%d')}")

m1, m2, m3 = st.columns(3)
m1.metric("Initial Capital", f"${invest_amount:,.0f}")
m2.metric("Projected Value", f"${final_value:,.2f}", delta=f"{(expected_return_pct*100):.2f}%")
m3.metric("Estimated Profit", f"${(final_value - invest_amount):,.2f}")

# --- CHART 1: FUTURE PROJECTION ---
st.divider()
st.subheader(f"📈 Projected Wealth Growth ({duration_months} Months)")
dates = pd.date_range(start=datetime.datetime.now(), periods=duration_months + 1, freq='ME')
values = [invest_amount * ((1 + monthly_growth) ** i) for i in range(duration_months + 1)]
projection_df = pd.DataFrame({'Month': dates, 'Value': values})
st.line_chart(projection_df.set_index('Month'), color=pred_color)

# --- CHARTS 2 & 3: VALIDATION & HISTORY ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🎯 Model Accuracy (Last 30 Days)")
    test_df = full_df.tail(30).copy()
    features_list = ['Close', 'Open', 'High', 'Low', 'MA_7', 'MA_30']
    test_df['AI Prediction'] = model.predict(test_df[features_list])
    test_df = test_df.rename(columns={'Close': 'Actual Price'})
    st.line_chart(test_df.set_index('Date')[['Actual Price', 'AI Prediction']], color=[actual_color, pred_color])

with col_right:
    st.subheader("📜 Long-term Market History")
    st.line_chart(full_df.tail(500).set_index('Date')['Close'], color=hist_color)

st.divider()
st.caption("⚠️ Disclaimer: Linear Regression predictions are based on historical trends. Use as a guide, not a guarantee.")
