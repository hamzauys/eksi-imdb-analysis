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
 
    {"title": "La La Land", "year": "2016"},
    {"title": "Arrival", "year": "2016"},
    {"title": "Deadpool", "year": "2016"},
    {"title": "Manchester by the Sea", "year": "2016"},
    {"title": "Moonlight", "year": "2016"},
    {"title": "Parasite", "year": "2019"},
    {"title": "Marriage Story", "year": "2019"},
    {"title": "Ford v Ferrari", "year": "2019"},
    {"title": "Knives Out", "year": "2019"},
    {"title": "The Irishman", "year": "2019"},
    {"title": "1917", "year": "2019"},
    {"title": "Portrait of a Lady on Fire", "year": "2019"},
    {"title": "The Handmaiden", "year": "2016"},
    {"title": "Get Out", "year": "2017"},
    {"title": "Dunkirk", "year": "2017"},
    {"title": "The Shape of Water", "year": "2017"},
    {"title": "Roma", "year": "2018"},
    {"title": "Spider-Man: Into the Spider-Verse", "year": "2018"},
    {"title": "Ghostbusters", "year": "2016"},
    {"title": "Suicide Squad", "year": "2016"},
    {"title": "Bohemian Rhapsody", "year": "2018"},
    {"title": "Little Italy", "year": "2018"},
    {"title": "Avengers: Endgame", "year": "2019"},
    {"title": "Thelma", "year": "2017"},
    {"title": "Climax", "year": "2018"},
    {"title": "The Guilty", "year": "2018"},
    {"title": "Monos", "year": "2019"},
    {"title": "Once Upon a Time in Hollywood", "year": "2019"}

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
