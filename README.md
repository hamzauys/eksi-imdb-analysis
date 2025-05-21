# Project Overview

This project analyzes the relationship between the number of entries in **Ekşi Sözlük** (a popular Turkish online forum) about a film and the film's **IMDb score**. The goal is to determine whether discussion volume on Ekşi Sözlük can be an indicator of a film's quality as measured by IMDb ratings.

## Key Research Questions
- Does a higher number of Ekşi Sözlük entries correlate with higher IMDb scores?
- Are there differences based on release year?
- Can we use Ekşi Sözlük entry data to predict IMDb ratings?

## Methods and Techniques
- **Web Scraping** (to collect entry counts from Ekşi Sözlük)
- **Data Cleaning and Preprocessing** (handling missing values, formatting data)
- **Exploratory Data Analysis (EDA)**
- **Statistical Analysis** (correlation tests, hypothesis testing)
- **Pearson Correlation Test** (to measure linear relationship between entry counts and IMDb ratings)
- **Hypothesis Testing (P-value Analysis)** (to assess statistical significance of the observed correlations)

## Dataset
The data includes a curated list of over 130 films released between **2008 and 2024**, selected to span a wide range of genres, popularity levels, and discussion volumes.

For each film:
- **Slug**: Unique identifier used for scraping Ekşi Sözlük entries
- **IMDb Score**: Extracted from IMDb public datasets
- **Entry Count**: Estimated total entries from Ekşi Sözlük at the time of analysis

## Statistical Results

### 2008–2011

- **Pearson Correlation**: `0.346`
- **P-value**: `0.0489`

This indicates a **moderate positive correlation** between the number of Ekşi Sözlük entries and IMDb scores, and the relationship is **statistically significant** at the 0.05 level.

> *Note: Other release windows (e.g., 2016–2019, 2020–2024) were also tested, and results varied. The final result is available in the report document .*

## Machine Learning Models
To explore whether Ekşi Sözlük entry counts can predict IMDb scores, we applied basic machine learning models to each year’s dataset. The models used were:

**Linear Regression** (assumes a direct linear relationship)

**K-Nearest Neighbors** (KNN) Regressor (captures local patterns without assuming linearity)

Each model was evaluated using Mean Squared Error (MSE) and R² score.
While results varied across years, KNN performed better in 2016-2019 period, whereas Linear Regression remained more stable across all years.
These findings suggest that the relationship between public discussion volume and film ratings can differ significantly depending on the release period.

## Visualization
The scatter plot below visualizes the relationship between Ekşi entry count and IMDb score between **2008-2011** period. A trend line from simple linear regression is included to highlight the overall trend.
![2008](https://github.com/user-attachments/assets/b88aa180-6177-4d82-b6a9-780d7e79b60d)

```text
dsa210-project/
├── code/
│   ├── shared/
│   │   └── analyze_combined_data.py  # joint analysis
│   │   └── ml_model_comparison.py  # ML's models application
│   ├── 2008/
│   │   ├── scraping_2008.py
│   │   ├── imdb_2008.py
│   │   ├── eksi_entry_counts.csv
│   │   ├── imdb_scores.csv
│   │   └── entry_vs_imdb.png
│   ├── 2012/
│   │   ├── scraping_2012.py
│   │   ├── imdb_2012.py
│   │   ├── eksi_entry_counts.csv
│   │   ├── imdb_scores.csv
│   │   └── entry_vs_imdb.png
│   ├── 2016/
│   │   ├── scraping_2016.py
│   │   ├── imdb_2016.py
│   │   ├── eksi_entry_counts.csv
│   │   ├── imdb_scores.csv
│   │   └── entry_vs_imdb.png
│   ├── 2020/
│   │   ├── scraping_2020.py
│   │   ├── imdb_2020.py
│   │   ├── eksi_entry_counts.csv
│   │   ├── imdb_scores.csv
│   │   └── entry_vs_imdb.png
├── README.md
└── report.docx
```



##  How to Run the Code

This project analyzes the relationship between IMDb ratings and Ekşi Sözlük entries across different years.  
Each year (2008, 2012, 2016, 2020) is processed **independently** with its own scripts and data files.

---

###  The Steps to Run (Repeat for Each Period)

#### 1. Run the Ekşi Sözlük scraping script
This collects the number of Ekşi Sözlük entries for that year.
```bash
python code/<year>/<year>.py
Example: python code/2008/2008.py
```

#### 2. Run the IMDb rating extractor
This fetches IMDb scores for the same movies.

```bash
python code/<year>/<year>imdb.py
Example:python code/2008/2008imdb.py
```

#### 3. Run the analysis and visualization
```bash
python analyze_combined_data.py
```
#### 4. Run the ML Methods
```bash
python ml_model_comparison.py
```

## This will generate:

- 2008eksi_entry_counts.csv

- 2008imdb_scores.csv

- 2008.png (a visual plot of entry count vs IMDb score)

- The result of ML methods which are linear regression and KNN regressor (k=3).




