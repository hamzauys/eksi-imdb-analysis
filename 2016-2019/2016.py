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
        {"title": "La La Land", "slug": "la-la-land--5268807", "release": "2016-12-09"},
    {"title": "Arrival", "slug": "arrival--5230023", "release": "2016-11-11"},
    {"title": "Deadpool", "slug": "deadpool--4551102", "release": "2016-02-12"},
    {"title": "Manchester by the Sea", "slug": "manchester-by-the-sea--5311510", "release": "2016-11-18"},
    {"title": "Moonlight", "slug": "moonlight--5213803", "release": "2016-10-21"},
    {"title": "Parasite", "slug": "parasite--6052039", "release": "2019-05-30"},
    {"title": "Marriage Story", "slug": "marriage-story--6630151", "release": "2019-11-06"},
    {"title": "Ford v Ferrari", "slug": "ford-v-ferrari--6421567", "release": "2019-11-15"},
    {"title": "Knives Out", "slug": "knives-out--6525433", "release": "2019-11-27"},
    {"title": "The Irishman", "slug": "the-irishman--6630367", "release": "2019-11-01"},
    {"title": "1917", "slug": "1917--6691192", "release": "2019-12-25"},
    {"title": "Portrait of a Lady on Fire", "slug": "portrait-of-a-lady-on-fire--6073330", "release": "2019-09-18"},
    {"title": "The Handmaiden", "slug": "the-handmaiden--5363673", "release": "2016-10-14"},
    {"title": "Get Out", "slug": "get-out--5879101", "release": "2017-02-24"},
    {"title": "Dunkirk", "slug": "dunkirk--5993612", "release": "2017-07-21"},
    {"title": "The Shape of Water", "slug": "the-shape-of-water--6037814", "release": "2017-12-01"},
    {"title": "Roma", "slug": "roma-alfonso-cuaron-filmi--5876819", "release": "2018-08-30"},
    {"title": "Spider-Man: Into the Spider-Verse", "slug": "spider-man-into-the-spider-verse--6703670", "release": "2018-12-14"},
    {"title": "Ghostbusters", "slug": "ghostbusters--5067037", "release": "2016-07-15"},
    {"title": "Suicide Squad", "slug": "suicide-squad--4551596", "release": "2016-08-05"},
    {"title": "Bohemian Rhapsody", "slug": "bohemian-rhapsody--6477824", "release": "2018-10-24"},
    {"title": "Little Italy", "slug": "little-italy--6597786", "release": "2018-09-21"},
    {"title": "Avengers: Endgame", "slug": "avengers-endgame--6660294", "release": "2019-04-26"},
    {"title": "Foxtrot", "slug": "foxtrot--6246532", "release": "2017-09-21"},
    {"title": "Thelma", "slug": "thelma--6386438", "release": "2017-11-10"},
    {"title": "Climax", "slug": "climax--6744082", "release": "2018-09-19"},
    {"title": "The Guilty", "slug": "the-guilty--6678868", "release": "2018-06-28"},
    {"title": "Once Upon a Time in Hollywood", "slug": "once-upon-a-time-in-hollywood--6614205", "release": "2019-07-26"},
    {"title": "Monos", "slug": "monos--6768578", "release": "2019-08-15"}


]
    scrape_eksi_pages(films)
