import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

plot_num = 1  # Counter for plot file names

# 1. Load Data and Overview
df = pd.read_csv('AB_NYC_2019.csv')
print("Rows, Columns:", df.shape)
print(df.dtypes)
categorical = df.select_dtypes(include='object').columns.tolist()
numerical = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
print("Categorical columns:", categorical)
print("Numerical columns:", numerical)

# 2. Visualize Key Variables
plt.figure(figsize=(15,4))
plt.subplot(1,3,1)
sns.histplot(df['price'], bins=50, kde=True)
plt.title('Price Distribution')
plt.subplot(1,3,2)
sns.histplot(df['number_of_reviews'], bins=50, kde=True)
plt.title('Reviews Distribution')
plt.subplot(1,3,3)
sns.histplot(df['availability_365'], bins=50, kde=True)
plt.title('Availability Distribution')
plt.tight_layout()
plt.savefig(f'week3_plot{plot_num}.png')
plt.close()
plot_num += 1

# 3. Data Cleaning: Missing Values
print("\nMissing values per column:\n", df.isnull().sum())
df['reviews_per_month'] = df['reviews_per_month'].fillna(0)
df['last_review'] = df['last_review'].fillna('2000-01-01')  # Placeholder for missing dates

# Handle Duplicates
print("Duplicate rows:", df.duplicated().sum())
df = df.drop_duplicates()

# 4. Categorical Data Processing
plt.figure(figsize=(10,4))
plt.subplot(1,2,1)
df['neighbourhood_group'].value_counts().plot(kind='bar', title='By Neighbourhood Group')
plt.subplot(1,2,2)
df['room_type'].value_counts().plot(kind='bar', title='By Room Type')
plt.tight_layout()
plt.savefig(f'week3_plot{plot_num}.png')
plt.close()
plot_num += 1

# One-hot encoding for 'room_type', label encoding for 'neighbourhood_group'
df = pd.get_dummies(df, columns=['room_type'], prefix='room')
df['neighbourhood_group_enc'] = df['neighbourhood_group'].astype('category').cat.codes

# Room Type Popularity Across Neighborhoods
ctab = pd.crosstab(df['neighbourhood_group'], df.filter(like="room_").idxmax(axis=1))
ctab.plot(kind='bar', stacked=True)
plt.title('Room Type by Neighbourhood Group')
plt.ylabel('Count')
plt.savefig(f'week3_plot{plot_num}.png')
plt.close()
plot_num += 1

# 5. Outlier Detection and Handling
plt.figure(figsize=(7,3))
sns.boxplot(x=df['price'])
plt.title("Price Boxplot Before Outlier Removal")
plt.savefig(f'week3_plot{plot_num}.png')
plt.close()
plot_num += 1

Q1, Q3 = df['price'].quantile([0.25, 0.75])
IQR = Q3 - Q1
price_upper = Q3 + 1.5 * IQR
print("Price Outlier Threshold:", price_upper)
df = df[df['price'] <= price_upper]  # Remove outliers

plt.figure(figsize=(7,3))
sns.boxplot(x=df['price'])
plt.title("Price Boxplot After Outlier Removal")
plt.savefig(f'week3_plot{plot_num}.png')
plt.close()
plot_num += 1

# Optional: log-transform
df['price_log'] = np.log1p(df['price'])
plt.figure(figsize=(6,3))
sns.histplot(df['price_log'], bins=50, kde=True)
plt.title('Log Price Distribution')
plt.savefig(f'week3_plot{plot_num}.png')
plt.close()
plot_num += 1

# 6. Date Transformation and Time Analysis
df['last_review'] = pd.to_datetime(df['last_review'], errors='coerce')
df['review_year'] = df['last_review'].dt.year
df['review_month'] = df['last_review'].dt.month

annual_reviews = df.groupby('review_year')['number_of_reviews'].sum()
plt.figure()
annual_reviews.plot(kind='bar', title="Total Reviews Per Year")
plt.ylabel('Number of Reviews')
plt.tight_layout()
plt.savefig(f'week3_plot{plot_num}.png')
plt.close()
plot_num += 1

monthly_reviews = df.groupby('review_month')['number_of_reviews'].sum()
plt.figure()
monthly_reviews.plot(kind='bar', title="Total Reviews Per Month")
plt.ylabel('Number of Reviews')
plt.tight_layout()
plt.savefig(f'week3_plot{plot_num}.png')
plt.close()
plot_num += 1

# 7. Advanced Analysis: Simple Price Prediction
features = df.drop(['id', 'price', 'name', 'host_name', 'last_review', 'neighbourhood_group', 'neighbourhood'], axis=1)
features = features.fillna(0)
target = df['price']
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=1)
model = RandomForestRegressor(n_estimators=50, random_state=1)
model.fit(X_train, y_train)
preds = model.predict(X_test)
print("\nRandomForestRegressor RMSE:", round(np.sqrt(mean_squared_error(y_test, preds)), 2))

# Feature importance plot (optional)
importances = pd.Series(model.feature_importances_, index=features.columns)
importances.sort_values(ascending=False)[:10].plot(kind='bar', title='Top 10 Feature Importances')
plt.savefig(f'week3_plot{plot_num}.png')
plt.close()
plot_num += 1
