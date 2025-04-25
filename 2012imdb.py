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
    {"title": "Django Unchained", "year": "2012"},
    {"title": "12 Years a Slave", "year": "2013"},
    {"title": "Boyhood", "year": "2014"},
    {"title": "Mad Max: Fury Road", "year": "2015"},
    {"title": "The Revenant", "year": "2015"},
    {"title": "Birdman", "year": "2014"},
    {"title": "Her", "year": "2013"},
    {"title": "The Wolf of Wall Street", "year": "2013"},
    {"title": "Inside Llewyn Davis", "year": "2013"},
    {"title": "Gravity", "year": "2013"},
    {"title": "The Grand Budapest Hotel", "year": "2014"},
    {"title": "Whiplash", "year": "2014"},
    {"title": "The Theory of Everything", "year": "2014"},
    {"title": "Nightcrawler", "year": "2014"},
    {"title": "Room", "year": "2015"},
    {"title": "Spotlight", "year": "2015"},
    {"title": "Inside Out", "year": "2015"},
    {"title": "The Martian", "year": "2015"},
    {"title": "Brooklyn", "year": "2015"},
    {"title": "The Big Short", "year": "2015"},
    {"title": "Carol", "year": "2015"},
    {"title": "Ex Machina", "year": "2015"},
    {"title": "Interstellar", "year": "2014"},
    {"title": "Transformers: Age of Extinction", "year": "2014"},
    {"title": "Fifty Shades of Grey", "year": "2015"},
    {"title": "Teenage Mutant Ninja Turtles", "year": "2014"},
    {"title": "Ida", "year": "2013"},
    {"title": "Timbuktu", "year": "2014"},
    {"title": "The Dark Knight Rises", "year": "2012"},
    {"title": "The Twilight Saga: Breaking Dawn - Part 2", "year": "2012"},
    {"title": "The Hunt", "year": "2012"},
    {"title": "Snow White and the Huntsman", "year": "2012"}
    {"title": "Maleficent", "year": "2014"},
    {"title": "The Amazing Spider-Man 2", "year": "2014"},
    {"title": "Pacific Rim", "year": "2013"},
    {"title": "World War Z", "year": "2013"},


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
