import pandas as pd
import matplotlib.pyplot as plt

# 1. Load the Dataset
df = pd.read_csv('GlobalLandTemperaturesByCountry.csv')

# 2. Display the first 10 rows and dataset info
print(df.head(10))
df.info()
print(df.describe())

# 3. Check for missing values
missing = df.isnull().sum()
print("Missing values per column:\n", missing)

# 4. Drop rows with missing AverageTemperature (main variable of interest)
df_clean = df.dropna(subset=['AverageTemperature']).copy()
print("Rows after dropping missing temperatures:", len(df_clean))

# 5. Convert 'dt' to datetime BEFORE using .dt accessor
df_clean['dt'] = pd.to_datetime(df_clean['dt'], errors='coerce')
print("dtypes after datetime conversion:\n", df_clean.dtypes)

# 6. Create 'Year' and 'Month' columns (now safe)
df_clean['Year'] = df_clean['dt'].dt.year
df_clean['Month'] = df_clean['dt'].dt.month

# 7. Check for negative or extreme values
print("Temperature range:", df_clean['AverageTemperature'].min(), "to", df_clean['AverageTemperature'].max())
print("Uncertainty range:", df_clean['AverageTemperatureUncertainty'].min(), "to", df_clean['AverageTemperatureUncertainty'].max())

# 8. Filter based on a reasonable uncertainty threshold
threshold = 2.0
df_filtered = df_clean[df_clean['AverageTemperatureUncertainty'] <= threshold].copy()
print("Original dataset size:", len(df_clean))
print("Filtered dataset size:", len(df_filtered))
print(f"Rows removed due to uncertainty > {threshold}: {len(df_clean) - len(df_filtered)}")

# 9. Group by Year for trend analysis (mean temp and uncertainty)
yearly = df_filtered.groupby('Year').agg({
    'AverageTemperature': 'mean',
    'AverageTemperatureUncertainty': 'mean'
}).reset_index()

# 10. Plot average temperature trend with error bars for uncertainty
plt.figure(figsize=(12,6))
plt.errorbar(
    yearly['Year'], 
    yearly['AverageTemperature'], 
    yerr=yearly['AverageTemperatureUncertainty'], 
    fmt='-o', ecolor='gray', capsize=3, label='Avg Temp ± Uncertainty'
)
plt.title('Average Land Temperature by Year (with Uncertainty)')
plt.xlabel('Year')
plt.ylabel('Average Temperature (°C)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('week2_plot1.png')
plt.close()

# 11. Plot trend of AverageTemperatureUncertainty over time
plt.figure(figsize=(12,6))
plt.plot(yearly['Year'], yearly['AverageTemperatureUncertainty'], '-o', color='red')
plt.title('Trend of Average Temperature Uncertainty Over Time')
plt.xlabel('Year')
plt.ylabel('Average Temperature Uncertainty (°C)')
plt.grid(True)
plt.tight_layout()
plt.savefig('week2_plot2.png', bbox_inches='tight', dpi=150)
plt.close()

# 12. Identify years with high mean uncertainty
high_uncertainty_years = yearly[yearly['AverageTemperatureUncertainty'] > threshold]
print("Years with high mean uncertainty (> 2.0):")
print(high_uncertainty_years[['Year', 'AverageTemperatureUncertainty']])

# 13. Identify years with large temperature fluctuations (outliers)
temp_std = df_filtered.groupby('Year')['AverageTemperature'].std().reset_index()
temp_std_mean = temp_std['AverageTemperature'].mean()
temp_std_std = temp_std['AverageTemperature'].std()
outlier_years = temp_std[
    temp_std['AverageTemperature'] > temp_std_mean + 2*temp_std_std
]
print("Years with large temperature fluctuations:")
print(outlier_years)

# 14. Export the cleaned dataset
df_filtered.to_csv('cleaned_temperatures.csv', index=False)
print("Cleaned data exported to cleaned_temperatures.csv")
