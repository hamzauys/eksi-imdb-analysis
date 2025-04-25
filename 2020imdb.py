import pandas as pd

# 1. Read the files
basics = pd.read_csv("data/title.basics.tsv", sep="\t", dtype=str, compression="gzip")
ratings = pd.read_csv("data/title.ratings.tsv", sep="\t", dtype=str, compression="gzip")

# 2. Just get movies
basics = basics[basics["titleType"] == "movie"]

# 3. Take the necessary columns: title + year
basics = basics[["tconst", "primaryTitle", "startYear"]].rename(
    columns={"primaryTitle": "title"}
)

# 4. Take the necessary columns for IMDB scores
ratings = ratings[["tconst", "averageRating"]]

# 5. Films to be matched and Years
films = [
    {"title": "Oppenheimer", "year": "2023"},
    {"title": "Dune: Part Two", "year": "2024"},
    {"title": "Barbie", "year": "2023"},
    {"title": "Poor Things", "year": "2023"},
    {"title": "Triangle of Sadness", "year": "2022"},
    {"title": "Don't Look Up", "year": "2021"},
    {"title": "The Banshees of Inisherin", "year": "2022"},
    {"title": "About Dry Grasses", "year": "2023"},
    {"title": "Inside Out 2", "year": "2024"},
    {"title": "Monkey Man", "year": "2024"},
    {"title": "Ordinary Angels", "year": "2024"},
    {"title": "Anora", "year": "2024"},
    {"title": "Killers of the Flower Moon", "year": "2023"},
     {"title": "Spider-Man: No Way Home",  "year": "2021"},
    {"title": "Top Gun: Maverick", "year": "2022"},
    {"title": "Avatar: The Way of Water",   "year": "2022"},
    {"title": "John Wick: Chapter 4","year": "2023"},
    {"title": "A Quiet Place Part II", "year": "2020"},
    {"title": "Doctor Strange in the Multiverse of Madness", "year": "2022"},
     {"title": "Day Shift", "year": "2022"},
    {"title": "Bad Boys for Life", "year": "2020"},
    {"title": "The Northman", "year": "2022"},
    {"title": "The Devil All the Time", "year": "2020"},
    {"title": "Poor Things", "year": "2023"},
    {"title": "The Matrix Resurrections", "year": "2021"},
    {"title": "Morbius", "year": "2022"},
    {"title": "Interceptor", "year": "2022"},
    {"title": "The Invisible Man", "year": "2020"},
    {"title": "Free Guy", "year": "2021"},
    {"title": "Don't Look Up", "year": "2021"},
    {"title": "Tenet", "year": "2020"},
    {"title": "The Batman", "year": "2022"}
]

# 6. Match Film Name + Year
conds = [
    (basics["title"] == f["title"]) & (basics["startYear"] == f["year"])
    for f in films
]
subset = basics[pd.concat(conds, axis=1).any(axis=1)]

# 7. Combine with Ratings
merged = subset.merge(ratings, on="tconst")
merged = merged[["title", "startYear", "averageRating"]].rename(
    columns={"averageRating": "imdb_score"}
)
merged["imdb_score"] = merged["imdb_score"].astype(float)

# 8. Save as CSV
merged.to_csv("data/imdb_scores.csv", index=False)
print("IMDB scores recorded → data/imdb_scores.csv")
print(merged)
