import os
import pandas as pd
import matplotlib.pyplot as plt

# Get the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, 'gold_prices.csv')

def main():
    try:
        # 1. Load and Prepare
        df = pd.read_csv(FILE_PATH)
        df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
        df = df.sort_values('Date').reset_index(drop=True)

        # 2. INSPECTION: Head and Tail
        print("\n" + "="*50)
        print("FIRST 5 ROWS (The Beginning - Year 2000s)")
        print("="*50)
        print(df.head())

        print("\n" + "="*50)
        print("LAST 5 ROWS (The Present - Year 2026)")
        print("="*50)
        print(df.tail())
        print("="*50 + "\n")

        # 3. Quick Visual Trend
        plt.figure(figsize=(10, 5))
        plt.plot(df['Date'], df['Close'], color='gold', linewidth=2)
        plt.title('Gold Historical View: Head to Tail')
        plt.grid(True, alpha=0.3)
        plt.show()

    except Exception as e:
        print(f"❌ Error: {e}")

# Fixed: main() is now properly indented on a new line
if __name__ == "__main__":
    main()