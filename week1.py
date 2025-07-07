import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
# Note: The columns are: "Position (in January)","Name","ELO","Date","Age"
df = pd.read_csv('chess.csv')

# Clean column names (remove spaces, make lowercase)
df.columns = df.columns.str.strip().str.lower()

# Rename columns for easier access
# 'elo' instead of 'ELO', 'name', 'date', 'age'
df = df.rename(columns={'elo': 'elo', 'name': 'name', 'date': 'date', 'age': 'age'})

# Extract year from 'date' column (e.g., '2021 Jan' -> 2021)
df['year'] = df['date'].str.extract(r'(\d{4})').astype(int)

# 1. Highest Elo
highest_elo_player = df.loc[df['elo'].idxmax()]
print("Player with highest Elo:")
print(highest_elo_player[['name', 'elo', 'year']])

# 2. Top 10 Players With Highest Elo
top10 = df.sort_values('elo', ascending=False).drop_duplicates('name').head(10)
print("\nTop 10 players with highest Elo:")
print(top10[['name', 'elo', 'year']])

# 3. Time Trend of Top 10's Average Elo Each Year
avg_elo_per_year = []
years = sorted(df['year'].dropna().unique())
for y in years:
    year_df = df[df['year'] == y].sort_values('elo', ascending=False).drop_duplicates('name').head(10)
    avg_elo = year_df['elo'].mean()
    avg_elo_per_year.append({'year': y, 'avg_elo': avg_elo})
avg_elo_df = pd.DataFrame(avg_elo_per_year)
plt.figure(figsize=(10,5))
plt.plot(avg_elo_df['year'], avg_elo_df['avg_elo'], marker='o')
plt.title("Average Elo of Top 10 Players Each Year")
plt.xlabel("Year")
plt.ylabel("Average Elo")
plt.grid(True)
plt.tight_layout()
plt.savefig('week1_plot1.png')
plt.close()

# 4. Time Trend for Number of Players Above 2750 Elo
players_above_2750 = df[df['elo'] > 2750]
count_above_2750 = players_above_2750.groupby('year')['name'].nunique()
plt.figure(figsize=(10,5))
plt.plot(count_above_2750.index, count_above_2750.values, marker='o', color='red')
plt.title("Number of Players Above 2750 Elo Each Year")
plt.xlabel("Year")
plt.ylabel("Number of Players")
plt.grid(True)
plt.tight_layout()
plt.savefig('week1_plot2.png', bbox_inches='tight', dpi=150)
plt.close()

# 5. Time Trend of Top 10's Average Age Each Year
if 'age' in df.columns:
    avg_age_per_year = []
    for y in years:
        year_df = df[df['year'] == y].sort_values('elo', ascending=False).drop_duplicates('name').head(10)
        avg_age = year_df['age'].mean()
        avg_age_per_year.append({'year': y, 'avg_age': avg_age})
    avg_age_df = pd.DataFrame(avg_age_per_year)
    plt.figure(figsize=(10,5))
    plt.plot(avg_age_df['year'], avg_age_df['avg_age'], marker='o', color='green')
    plt.title("Average Age of Top 10 Players Each Year")
    plt.xlabel("Year")
    plt.ylabel("Average Age")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('week1_plot3.png', bbox_inches='tight', dpi=150)
    plt.close()

# 6. Time Trend for Number of Players Under 25 Years Old in Top 10
if 'age' in df.columns:
    under25_per_year = []
    for y in years:
        year_df = df[df['year'] == y].sort_values('elo', ascending=False).drop_duplicates('name').head(10)
        under25 = (year_df['age'] < 25).sum()
        under25_per_year.append({'year': y, 'under25': under25})
    under25_df = pd.DataFrame(under25_per_year)
    plt.figure(figsize=(10,5))
    plt.plot(under25_df['year'], under25_df['under25'], marker='o', color='purple')
    plt.title("Number of Top 10 Players Under 25 Each Year")
    plt.xlabel("Year")
    plt.ylabel("Number Under 25")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('week1_plot4.png', bbox_inches='tight', dpi=150)
    plt.close()

# 7. Time Trend of Magnus Carlsen's Elo
carlsen_df = df[df['name'].str.lower().str.contains('carlsen')]
plt.figure(figsize=(10,5))
plt.plot(carlsen_df['year'], carlsen_df['elo'], marker='o', color='orange')
plt.title("Magnus Carlsen's Elo Over Time")
plt.xlabel("Year")
plt.ylabel("Elo")
plt.grid(True)
plt.tight_layout()
plt.savefig('week1_plot5.png', bbox_inches='tight', dpi=150)
plt.close()