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
    {"title": "Slumdog Millionaire", "year": "2008"},
    {"title": "The Curious Case of Benjamin Button", "year": "2008"},
    {"title": "The Hurt Locker", "year": "2009"},
    {"title": "Avatar", "year": "2009"},
    {"title": "Inglourious Basterds", "year": "2009"},
    {"title": "The King's Speech", "year": "2010"},
    {"title": "Black Swan", "year": "2010"},
    {"title": "The Social Network", "year": "2010"},
    {"title": "The Artist", "year": "2011"},
    {"title": "Drive", "year": "2011"},
    {"title": "Midnight in Paris", "year": "2011"},
    {"title": "The Help", "year": "2011"},
    {"title": "Moneyball", "year": "2011"},
    {"title": "A Separation", "year": "2011"},
    {"title": "The Dark Knight", "year": "2008"},
    {"title": "Inception", "year": "2010"},
    {"title": "Transformers: Revenge of the Fallen", "year": "2009"},
    {"title": "Twilight", "year": "2008"},
    {"title": "The Last Airbender", "year": "2010"},
    {"title": "A Prophet", "year": "2009"},
    {"title": "Fish Tank", "year": "2009"},
    {"title": "Incendies", "year": "2010"},
    {"title": "Cars 2", "year": "2011"},
    {"title": "Fast Five", "year": "2011"},
    {"title": "Fast & Furious", "year": "2009"},
    {"title": "Pirates of the Caribbean: On Stranger Tides", "year": "2011"},
    {"title": "Shutter Island", "year": "2010"},
    {"title": "Harry Potter and the Deathly Hallows: Part 2", "year": "2011"},
    {"title": "Toy Story 3", "year": "2010"},
    {"title": "How to Train Your Dragon", "year": "2010"},
    {"title": "3 Idiots", "year": "2009"},
    {"title": "Hachi: A Dog's Tale", "year": "2009"},
    {"title": "WALL·E", "year": "2008"}
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
