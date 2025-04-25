# =============================================================
# Sour Dictionary - Withdrawing the number of pages in movie titles
# FULL AUTOMATIC SOLUTION - COOKIE EXPLANATION + SELENUM + CSV output
# =============================================================
"""
Sequence of use:

1) Login with your sour dictionary account in the browser.
2) All on the same tab as 'get cookies.txt' extension (or similar)   
   Download cookies to this folder as 'minus_cookies.txt'.
3) Once `python cookie_helper.py` `Once.  
   This converts the TXT content into a pickle (minus_cookies.pkl).
4) Then `python scraping.py` - Film Slug list no matter how long
   as a user has made the number of pages as a user and
   Writes to Data/ENSİ_Entry_Counts.csv file.
"""

# --------------------------- cookie_helper.py ---------------------------
import pickle, os

TXT = "eksi_cookies.txt"
PKL = "eksi_cookies.pkl"

def txt_to_pkl():
    """Cookies.txt → Pickle downloaded from Chrome extension"""
    cookies = []
    with open(TXT, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) >= 7:
                cookies.append({
                    "domain": parts[0],
                    "path":   parts[2],
                    "secure": parts[3].lower() == "true",
                    "name":   parts[5],
                    "value":  parts[6]
                })
    pickle.dump(cookies, open(PKL, "wb"))
    print("Cookies transferred to Pickle →", PKL)

if __name__ == "__main__":
    if not os.path.exists(TXT):
        print(f"{TXT} not found. You need to download cookie.txt from the browser.")
    else:
        txt_to_pkl()

# ------------------------------ scraping.py -----------------------------
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pickle, re, time, os, pandas as pd

COOKIE_PKL = "eksi_cookies.pkl"

def get_page_count(slug: str) -> int | None:
    url = f"https://eksisozluk.com/{slug}"
    opts = Options()
# Close the headless use if you want    # opts.add_argument("--headless")
    driver = webdriver.Chrome(options=opts)

    driver.get("https://eksisozluk.com")
    for c in pickle.load(open(COOKIE_PKL, "rb")):
        driver.add_cookie(c)

    driver.get(url)
    time.sleep(3)  # We increased waiting

    try:
        # Print the whole page html for debug
        print("DEBUG: The page is loading...")
        html = driver.page_source
        with open("debug_output.html", "w", encoding="utf-8") as f:
            f.write(html)

        # A more general approach instead of the old css selector:
        pager_text = driver.find_element(By.CSS_SELECTOR, "div[class*='pager'],nav[class*='pager']").text
        pages = int(re.search(r"/\s*(\d+)", pager_text).group(1))
    except Exception as e:
        print(f" Error (Page not found): {slug} → {e}")
        pages = None

    driver.quit()
    return pages


def scrape_eksi_pages(film_list: list[dict]):
    if not os.path.exists("data"): os.makedirs("data")
    rows = []
    for film in film_list:
        print("🔍", film["title"])
        pages = get_page_count(film["slug"])
        rows.append({
            "title": film["title"],
            "slug": film["slug"],
            "page_count": pages,
            "estimated_entry_count": None if pages is None else pages * 10
        })
        time.sleep(1)
    pd.DataFrame(rows).to_csv("data/eksi_entry_counts.csv", index=False)
    print(" data/eksi_entry_counts.csv written")

if __name__ == "__main__":
    films = [
        {"title": "Django Unchained", "slug": "django-unchained--4529294", "release": "2012-12-25"},
        {"title": "12 Years a Slave", "slug": "12-years-a-slave--4703809", "release": "2013-10-18"},
        {"title": "Boyhood", "slug": "boyhood--5299977", "release": "2014-07-11"},
        {"title": "Mad Max: Fury Road", "slug": "mad-max-fury-road--5528391", "release": "2015-05-15"},
        {"title": "The Revenant", "slug": "the-revenant--5735060", "release": "2015-12-25"},
        {"title": "Birdman", "slug": "birdman--5564037", "release": "2014-10-17"},
        {"title": "Her", "slug": "her--5239932", "release": "2013-12-18"},
        {"title": "The Wolf of Wall Street", "slug": "the-wolf-of-wall-street--5219353", "release": "2013-12-25"},
        {"title": "Inside Llewyn Davis", "slug": "inside-llewyn-davis--5253797", "release": "2013-12-06"},
        {"title": "Gravity", "slug": "gravity--5154216", "release": "2013-10-04"},
        {"title": "The Grand Budapest Hotel", "slug": "the-grand-budapest-hotel--5829929", "release": "2014-03-28"},
        {"title": "Whiplash", "slug": "whiplash--5730417", "release": "2014-10-10"},
        {"title": "The Theory of Everything", "slug": "the-theory-of-everything--5892856", "release": "2014-11-07"},
        {"title": "Nightcrawler", "slug": "nightcrawler--5710792", "release": "2014-10-31"},
        {"title": "Room", "slug": "room--6020467", "release": "2015-10-16"},
        {"title": "Spotlight", "slug": "spotlight--6120437", "release": "2015-11-06"},
        {"title": "Inside Out", "slug": "inside-out--6145206", "release": "2015-06-19"},
        {"title": "The Martian", "slug": "the-martian--6176851", "release": "2015-10-02"},
        {"title": "Brooklyn", "slug": "brooklyn--6234001", "release": "2015-11-04"},
        {"title": "The Big Short", "slug": "the-big-short--6167200", "release": "2015-12-11"},
        {"title": "Carol", "slug": "carol--6120422", "release": "2015-11-20"},
        {"title": "Ex Machina", "slug": "ex-machina--6080300", "release": "2015-04-10"},
        {"title": "Interstellar", "slug": "interstellar--5829727", "release": "2014-11-07"},
        {"title": "Transformers: Age of Extinction", "slug": "transformers-age-of-extinction--5792875", "release": "2014-06-27"},
        {"title": "Fifty Shades of Grey", "slug": "fifty-shades-of-grey--5955203", "release": "2015-02-13"},
        {"title": "Teenage Mutant Ninja Turtles", "slug": "teenage-mutant-ninja-turtles--5770141", "release": "2014-08-08"},
        {"title": "Ida", "slug": "ida--5263215", "release": "2013-10-11"},
        {"title": "Timbuktu", "slug": "timbuktu--6129629", "release": "2014-12-10"},
        {"title": "The Dark Knight Rises", "slug": "the-dark-knight-rises--4898291", "release": "2012-07-20"},
        {"title": "The Twilight Saga: Breaking Dawn - Part 2", "slug": "the-twilight-saga-breaking-dawn-part-2--3061489", "release": "2012-11-16"},
        {"title": "The Hunt", "slug": "the-hunt--5322463", "release": "2012-10-25"},
        {"title": "Snow White and the Huntsman", "slug": "snow-white-and-the-huntsman--2571907", "release": "2012-05-30"},
        {"title": "Maleficent", "slug": "maleficent--114115", "release": "2014-05-28"},
        {"title": "The Amazing Spider-Man 2", "slug": "the-amazing-spider-man-2--2970660", "release": "2014-03-31"},
        {"title": "Pacific Rim", "slug": "pacific-rim--857093", "release": "2013-07-19"},
        {"title": "World War Z", "slug": "world-war-z--1615578", "release": "2013-06-21"}

]
    scrape_eksi_pages(films)
