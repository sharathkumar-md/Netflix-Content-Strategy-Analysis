# Netflix Content Strategy Analysis

This project dives deep into Netflix's content release patterns in 2023 to understand how content type, language, release timing (monthly, weekly, seasonal), and proximity to holidays influence audience engagement measured through total viewership hours. By analyzing trends using Python, we uncover actionable insights into what makes content successful on a global streaming platform like Netflix.

The analysis combines data cleaning, exploratory data analysis (EDA), and visualization to decode Netflix’s strategic decisions in content production and release planning.

---

## Objective

To explore and analyze the Netflix 2023 content dataset and answer key business questions such as:
- Do shows outperform movies in terms of viewership?
- Which languages attract the most viewers?
- How does release timing (month, weekday, season) affect total watch hours?
- Do holiday releases result in higher viewership?

---

## Dataset

- **Source:** Netflix 2023 Content Dataset
- **Key Columns Used:**
  - `Title`
  - `Content Type` – Movie or Show
  - `Language Indicator`
  - `Hours Viewed` – Total hours watched globally
  - `Release Date` – Original release date

---

## Key Insights

### Content Type Performance
- **Shows** significantly outperform **movies** in total global viewership.

### Language Distribution
- **English-language** content dominates overall viewership.
- Other top-performing languages include **Korean**, **Japanese**, and **Non-English regional** content.

### Monthly Trends
- **December** records the highest viewership across the year.
- Additional peaks in **June** and **October**, indicating seasonal viewer engagement.

### Seasonal Trends
- **Fall** stands out as the most engaging season for Netflix releases.

### Day-of-Week Strategy
- **Friday** is the prime release day with the highest number of new titles and viewership, supporting the weekend binge-watch model.

### Holiday Impact
- Content released within **±3 days of major holidays** tends to perform better, indicating the strategic timing of key releases.

---

## Visualizations

All analysis charts are saved locally as `.png` files:

| File Name         | Description                                  |
|-------------------|----------------------------------------------|
| `week4_plot1.png` | Total Viewership by Content Type             |
| `week4_plot2.png` | Top 10 Languages by Viewership               |
| `week4_plot3.png` | Monthly Viewership Trend                     |
| `week4_plot4.png` | Monthly Viewership by Content Type           |
| `week4_plot5.png` | Seasonal Viewership Patterns                 |
| `week4_plot6.png` | Monthly Releases vs Total Viewership         |
| `week4_plot7.png` | Weekly Releases vs Total Viewership          |

---

## Top 5 Most Watched Titles (2023)

| Title                            | Hours Viewed | Type  |
|---------------------------------|--------------|-------|
| The Night Agent: Season 1       | 812M         | Show  |
| Ginny & Georgia: Season 2       | 665M         | Show  |
| King the Land                   | 630M         | Movie |
| The Glory: Season 1             | 623M         | Show  |
| ONE PIECE: Season 1             | 542M         | Show  |

---

## Tech Stack

- **Python 3**
- **Pandas** for data wrangling
- **Matplotlib** and **Seaborn** for visualizations
