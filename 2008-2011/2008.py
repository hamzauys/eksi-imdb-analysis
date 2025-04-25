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
    {"title": "Slumdog Millionaire", "slug": "slumdog-millionaire--3006935", "release": "2008-11-12"},
    {"title": "The Curious Case of Benjamin Button", "slug": "the-curious-case-of-benjamin-button--3067382", "release": "2008-12-25"},
    {"title": "The Hurt Locker", "slug": "the-hurt-locker--3309422", "release": "2009-06-26"},
    {"title": "Avatar", "slug": "avatar--3238275", "release": "2009-12-18"},
    {"title": "Inglourious Basterds", "slug": "inglourious-basterds--3300782", "release": "2009-08-21"},
    {"title": "The King's Speech", "slug": "the-kings-speech--2517014", "release": "2010-12-24"},
    {"title": "Black Swan", "slug": "black-swan--3506541", "release": "2010-12-17"},
    {"title": "The Social Network", "slug": "the-social-network--3439999", "release": "2010-10-01"},
    {"title": "The Artist", "slug": "the-artist--4047640", "release": "2011-11-25"},
    {"title": "Drive", "slug": "drive--3849324", "release": "2011-09-16"},
    {"title": "Midnight in Paris", "slug": "midnight-in-paris--3720789", "release": "2011-06-10"},
    {"title": "The Help", "slug": "the-help--3700044", "release": "2011-08-10"},
    {"title": "Moneyball", "slug": "moneyball--3754496", "release": "2011-09-23"},
    {"title": "A Separation", "slug": "a-separation--3798712", "release": "2011-03-16"},
    {"title": "The Dark Knight", "slug": "the-dark-knight--3117563", "release": "2008-07-18"},
    {"title": "Inception", "slug": "inception--3372705", "release": "2010-07-16"},
    {"title": "Transformers: Revenge of the Fallen", "slug": "transformers-revenge-of-the-fallen--3290465", "release": "2009-06-24"},
    {"title": "Twilight", "slug": "twilight--3095796", "release": "2008-11-21"},
    {"title": "The Last Airbender", "slug": "the-last-airbender--3591947", "release": "2010-07-01"},
    {"title": "A Prophet", "slug": "a-prophet--3305575", "release": "2009-08-26"},
    {"title": "Fish Tank", "slug": "fish-tank--3448792", "release": "2009-09-11"},
    {"title": "Incendies", "slug": "incendies--3533803", "release": "2010-09-04"},
    {"title": "Cars 2", "slug": "cars-2--4304622", "release": "2011-06-24"},
    {"title": "Fast Five", "slug": "fast-five--4958406", "release": "2011-04-29"},
    {"title": "Fast & Furious", "slug": "fast-furious--285961", "release": "2009-04-03"},
    {"title": "Pirates of the Caribbean: On Stranger Tides", "slug": "pirates-of-the-caribbean-on-stranger-tides--4732001", "release": "2011-05-20"},
    {"title": "Shutter Island", "slug": "shutter-island--4898803", "release": "2010-02-19"},
    {"title": "Harry Potter and the Deathly Hallows: Part 2", "slug": "harry-potter-and-the-deathly-hallows-part-2--4468093", "release": "2011-07-15"},
    {"title": "Toy Story 3", "slug": "toy-story-3--4468809", "release": "2010-06-18"},
    {"title": "How to Train Your Dragon", "slug": "how-to-train-your-dragon--4207592", "release": "2010-03-26"},
    {"title": "3 Idiots", "slug": "3-idiots--4653921", "release": "2009-12-25"},
    {"title": "Hachi: A Dog's Tale", "slug": "hachi-a-dogs-tale--3228500", "release": "2009-06-13"},
    {"title": "WALL·E", "slug": "wall-e--1646008", "release": "2008-06-27"}

]
    scrape_eksi_pages(films)
