import os
import pandas as pd
import numpy as np

# Automatically resolve the path to the CSV relative to this file's folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CSV_PATH = os.path.join(BASE_DIR, 'gold_prices.csv')


def run_pre_eda_analysis(file_path):
    """Loads data, applies feature engineering, and prints statistical summary."""
    try:
        # 1. LOAD DATA
        df = pd.read_csv(file_path)
        df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
        df = df.sort_values('Date').reset_index(drop=True)

        # 2. FEATURE ENGINEERING (Adding Analysis Columns)
        df['Daily_Return_Pct'] = df['Close'].pct_change() * 100
        df['Daily_Range'] = df['High'] - df['Low']
        df['Is_Gain'] = df['Close'] > df['Open']

        # 3. STATISTICAL SUMMARY
        print("--- GOLD DATASET ANALYSIS SUMMARY ---")
        print(f"Time Horizon:        {df['Date'].min().date()} to {df['Date'].max().date()}")
        print(f"Total Trading Days:  {len(df)}")
        
        print("\n--- VOLATILITY STATS ---")
        print(f"Average Daily Return:    {df['Daily_Return_Pct'].mean():.4f}%")
        print(f"Maximum Single Day Gain: {df['Daily_Return_Pct'].max():.2f}%")
        print(f"Maximum Single Day Drop: {df['Daily_Return_Pct'].min():.2f}%")
        
        print("\n--- MARKET SENTIMENT ---")
        total_gains = df['Is_Gain'].sum()
        print(f"Days Finished Green: {total_gains} ({(total_gains / len(df)) * 100:.1f}%)")
        print(f"Days Finished Red:   {len(df) - total_gains} ({((len(df) - total_gains) / len(df)) * 100:.1f}%)")

        return df

    except Exception as e:
        print(f"❌ Analysis Error: {e}")
        return None


def check_data_quality(file_path):
    """Checks for missing values, zero prices, and duplicate rows in the dataset."""
    try:
        df = pd.read_csv(file_path)
        
        print("\n🔍 --- DATA QUALITY HEALTH CHECK ---")
        
        # 1. Count actual Null/NaN values
        missing_counts = df.isnull().sum()
        
        # 2. Check for zeros in Price columns
        cols_to_check = ['Open', 'High', 'Low', 'Close']
        zero_counts = (df[cols_to_check] == 0).sum()

        # 3. Report Results
        if missing_counts.sum() == 0 and zero_counts.sum() == 0:
            print("✅ Perfect! No missing or zero-value data found.")
        else:
            print("⚠️ Issues found:")
            if missing_counts.sum() > 0:
                print("\nMissing Values (NaN) per column:")
                print(missing_counts[missing_counts > 0])
            
            if zero_counts.sum() > 0:
                print("\nImpossible Zero-Values found:")
                print(zero_counts[zero_counts > 0])

        # 4. Check for Duplicate Rows
        duplicates = df.duplicated().sum()
        print(f"Duplicate Rows: {duplicates}")

    except Exception as e:
        print(f"❌ Error during check: {e}")


def clean_gold_data(file_path):
    """Repairs missing dataset values using forward and backward filling, then saves a cleaned CSV."""
    try:
        df = pd.read_csv(file_path)
        
        print("\n🛠️ Starting Data Repair...")
        
        # Apply forward fill then backward fill
        df_filled = df.ffill()
        df_final = df_filled.bfill()

        # Verify the fix
        remaining_missing = df_final.isnull().sum().sum()
        
        if remaining_missing == 0:
            print("✅ All missing values filled successfully!")
            output_path = os.path.join(BASE_DIR, 'gold_prices_cleaned.csv')
            df_final.to_csv(output_path, index=False)
            print(f"💾 Saved as '{output_path}'")
        else:
            print(f"⚠️ Warning: Still {remaining_missing} missing values left.")

        return df_final

    except Exception as e:
        print(f"❌ Cleaning Error: {e}")
        return None


# --- MAIN EXECUTION BLOCK ---
if __name__ == "__main__":
    # 1. Run Data Quality Check
    check_data_quality(DEFAULT_CSV_PATH)

    # 2. Clean Data and Save Cleaned Version
    clean_df = clean_gold_data(DEFAULT_CSV_PATH)

    # 3. Run Analysis on the dataset
    gold_df = run_pre_eda_analysis(DEFAULT_CSV_PATH)
    
    if gold_df is not None:
        print("\n--- ANALYTICAL HEAD (First 5 Rows) ---")
        print(gold_df[['Date', 'Close', 'Daily_Return_Pct', 'Is_Gain']].head())