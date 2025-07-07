import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style('whitegrid')
plt.style.use("fivethirtyeight")

plot_num = 1  # To name plots as week4_plotX.png

# 1. Load the Netflix dataset
netflix_data = pd.read_csv('netflix_content_2023.csv')

# 2. Clean 'Hours Viewed' column by removing commas and converting to numeric
netflix_data['Hours Viewed'] = netflix_data['Hours Viewed'].replace(',', '', regex=True)
netflix_data['Hours Viewed'] = pd.to_numeric(netflix_data['Hours Viewed'], errors='coerce')

# 3. Analyze trends in content type (Shows vs Movies)
content_type_viewership = netflix_data.groupby('Content Type')['Hours Viewed'].sum()
content_type_viewership.plot(kind='bar', color=['#1f77b4', '#ff7f0e'])
plt.title('Total Viewership Hours by Content Type')
plt.ylabel('Total Hours Viewed')
plt.xlabel('Content Type')
plt.tight_layout()
plt.savefig(f'week4_plot{plot_num}.png')
plt.close()
plot_num += 1

# 4. Aggregate viewership hours by language
language_viewership = netflix_data.groupby('Language Indicator')['Hours Viewed'].sum().sort_values(ascending=False)
language_viewership.head(10).plot(kind='bar')
plt.title('Top 10 Languages by Total Viewership Hours')
plt.ylabel('Total Hours Viewed')
plt.xlabel('Language')
plt.tight_layout()
plt.savefig(f'week4_plot{plot_num}.png')
plt.close()
plot_num += 1

# 5. Convert "Release Date" to datetime and extract month
netflix_data['Release Date'] = pd.to_datetime(netflix_data['Release Date'], errors='coerce')
netflix_data['Release Month'] = netflix_data['Release Date'].dt.month

# 6. Aggregate viewership hours by release month
monthly_viewership = netflix_data.groupby('Release Month')['Hours Viewed'].sum()
monthly_viewership.plot(kind='line', marker='o')
plt.title('Total Viewership Hours by Release Month')
plt.ylabel('Total Hours Viewed')
plt.xlabel('Release Month')
plt.tight_layout()
plt.savefig(f'week4_plot{plot_num}.png')
plt.close()
plot_num += 1

# 7. Extract top 5 titles based on viewership hours
top_5_titles = netflix_data.sort_values('Hours Viewed', ascending=False).head(5)
print("Top 5 Most-Watched Titles:")
print(top_5_titles[['Title', 'Hours Viewed', 'Language Indicator', 'Content Type', 'Release Date']])

# 8. Viewership trend by content type and release month
monthly_viewership_by_type = netflix_data.pivot_table(
    index='Release Month', columns='Content Type', values='Hours Viewed', aggfunc='sum'
)
monthly_viewership_by_type.plot()
plt.title('Monthly Viewership Hours by Content Type')
plt.ylabel('Total Hours Viewed')
plt.xlabel('Release Month')
plt.tight_layout()
plt.savefig(f'week4_plot{plot_num}.png')
plt.close()
plot_num += 1

# 9. Analyze seasonal viewership trends
def get_season(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Fall'

netflix_data['Release Season'] = netflix_data['Release Month'].apply(get_season)
seasonal_viewership = netflix_data.groupby('Release Season')['Hours Viewed'].sum()
seasons_order = ['Winter', 'Spring', 'Summer', 'Fall']
seasonal_viewership = seasonal_viewership.reindex(seasons_order)
seasonal_viewership.plot(kind='bar', color=['#bde0fe', '#a3cef1', '#5390d9', '#00296b'])
plt.title('Seasonal Viewership Trends')
plt.ylabel('Total Hours Viewed')
plt.xlabel('Season')
plt.tight_layout()
plt.savefig(f'week4_plot{plot_num}.png')
plt.close()
plot_num += 1

# 10. Monthly release patterns and viewership
monthly_releases = netflix_data['Release Month'].value_counts().sort_index()
monthly_viewership = netflix_data.groupby('Release Month')['Hours Viewed'].sum()
fig, ax1 = plt.subplots(figsize=(10,6))
ax1.bar(monthly_releases.index, monthly_releases.values, color='skyblue', alpha=0.7, label='Releases (count)')
ax1.set_xlabel('Release Month')
ax1.set_ylabel('Number of Releases', color='blue')
ax2 = ax1.twinx()
ax2.plot(monthly_viewership.index, monthly_viewership.values, 'o-', color='darkred', label='Total Viewership Hours')
ax2.set_ylabel('Total Hours Viewed', color='darkred')
plt.title('Monthly Release Count and Total Viewership Hours')
plt.tight_layout()
plt.savefig(f'week4_plot{plot_num}.png')
plt.close()
plot_num += 1

# 11. Analyze weekly release patterns and viewership
netflix_data['Release Day'] = netflix_data['Release Date'].dt.day_name()
weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
weekday_releases = netflix_data['Release Day'].value_counts().reindex(weekday_order)
weekday_viewership = netflix_data.groupby('Release Day')['Hours Viewed'].sum().reindex(weekday_order)
fig, ax1 = plt.subplots(figsize=(10,6))
ax1.bar(weekday_releases.index, weekday_releases.values, color='lightgreen', alpha=0.7, label='Releases (count)')
ax1.set_xlabel('Day of Week')
ax1.set_ylabel('Number of Releases', color='green')
ax2 = ax1.twinx()
ax2.plot(weekday_viewership.index, weekday_viewership.values, 'o-', color='purple', label='Total Viewership Hours')
ax2.set_ylabel('Total Hours Viewed', color='purple')
plt.title('Weekly Release Count and Total Viewership Hours')
plt.tight_layout()
plt.savefig(f'week4_plot{plot_num}.png')
plt.close()
plot_num += 1

# 12. Identify releases near significant holidays/events in 2023
important_dates = [
    '2023-01-01',  # New Year's Day
    '2023-02-14',  # Valentine's Day
    '2023-07-04',  # Independence Day (US)
    '2023-10-31',  # Halloween
    '2023-12-25'   # Christmas Day
]
important_dates = pd.to_datetime(important_dates)
holiday_releases = netflix_data[netflix_data['Release Date'].apply(
    lambda x: any((x - date).days in range(-3, 4) for date in important_dates)
)]
holiday_viewership = holiday_releases.groupby('Release Date')['Hours Viewed'].sum()
print("Holiday Releases Near Major Dates:")
print(holiday_releases[['Title', 'Release Date', 'Hours Viewed']])



