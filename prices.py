import pandas as pd
import matplotlib.pyplot as plt

def analyze_extremes(file_path):
    try:
        # 1. Load the cleaned data
        df = pd.read_csv(file_path)
        df['Date'] = pd.to_datetime(df['Date'])
        
        # 2. Find the Absolute Highest Price
        # We look at the 'High' column to see the peak reached during the day
        hi_idx = df['High'].idxmax()
        highest_row = df.iloc[hi_idx]
        
        # 3. Find the Absolute Lowest Price
        # We look at the 'Low' column to see the bottom
        lo_idx = df['Low'].idxmin()
        lowest_row = df.iloc[lo_idx]
        
        # 4. Calculate Total Growth (%)
        growth = ((highest_row['High'] - lowest_row['Low']) / lowest_row['Low']) * 100

        print("🏆 --- GOLD PRICE EXTREMES REPORT ---")
        print(f"All-Time High: ${highest_row['High']:,.2f} (Reached on {highest_row['Date'].date()})")
        print(f"All-Time Low:  ${lowest_row['Low']:,.2f} (Reached on {lowest_row['Date'].date()})")
        print(f"Total Growth:  {growth:,.2f}% from bottom to top")
        print("-" * 38)

        # 5. Visualizing the Extremes
        plt.figure(figsize=(12, 6))
        plt.plot(df['Date'], df['Close'], color='gold', label='Gold Price', alpha=0.5)
        
        # Mark the high point in Green
        plt.scatter(highest_row['Date'], highest_row['High'], color='green', s=100, label='Record High', zorder=5)
        
        # Mark the low point in Red
        plt.scatter(lowest_row['Date'], lowest_row['Low'], color='red', s=100, label='Record Low', zorder=5)
        
        plt.title('Gold Price Extremes (2000-2026)', fontsize=14)
        plt.ylabel('Price (USD)')
        plt.legend()
        plt.grid(True, alpha=0.2)
        plt.show()

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    analyze_extremes('gold_prices_cleaned.csv')
    import pandas as pd
import matplotlib.pyplot as plt

def analyze_volatility_by_year(file_path):
    try:
        # 1. Load the cleaned data
        df = pd.read_csv(file_path)
        df['Date'] = pd.to_datetime(df['Date'])
        
        # 2. Extract the Year
        df['Year'] = df['Date'].dt.year
        
        # 3. Calculate Yearly Volatility
        # We find the difference between the highest and lowest price within each year
        yearly_stats = df.groupby('Year')['Close'].agg(['max', 'min'])
        yearly_stats['Yearly_Swing'] = yearly_stats['max'] - yearly_stats['min']
        yearly_stats['Swing_Percentage'] = (yearly_stats['Yearly_Swing'] / yearly_stats['min']) * 100
        
        # 4. Find the Winner
        wildest_year = yearly_stats['Yearly_Swing'].idxmax()
        wildest_value = yearly_stats.loc[wildest_year, 'Yearly_Swing']
        wildest_pct = yearly_stats.loc[wildest_year, 'Swing_Percentage']

        print(f"🌪️ --- VOLATILITY ANALYSIS ---")
        print(f"The 'Wildest' Year in Gold History: {wildest_year}")
        print(f"Price Swing that year: ${wildest_value:,.2f}")
        print(f"Percentage Fluctuated:  {wildest_pct:.2f}%")
        print("-" * 30)

        # 5. Visualizing the Volatility
        plt.figure(figsize=(12, 6))
        yearly_stats['Yearly_Swing'].plot(kind='bar', color='skyblue', edgecolor='black')
        
        plt.title('Total Price Swing per Year ($)', fontsize=14)
        plt.ylabel('Dollar Difference (Max - Min)')
        plt.xlabel('Year')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.show()

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    analyze_volatility_by_year('gold_prices_cleaned.csv')