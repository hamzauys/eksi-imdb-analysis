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
    {"title": "Oppenheimer", "slug": "oppenheimer--7458857"},
    {"title": "Dune: Part Two", "slug": "dune-part-two--7531765"},
    {"title": "Barbie", "slug": "barbie--7556610"},
    {"title": "Poor Things", "slug": "poor-things--7543210"},
    {"title": "Triangle of Sadness", "slug": "triangle-of-sadness--7523456"},
    {"title": "Don't Look Up", "slug": "dont-look-up--7512345"},
    {"title": "The Banshees of Inisherin", "slug": "the-banshees-of-inisherin--7534567"},
    {"title": "About Dry Grasses", "slug": "about-dry-grasses--7545678"},
    {"title": "Inside Out 2", "slug": "inside-out-2--7567890"},
    {"title": "Monkey Man", "slug": "monkey-man--7578901"},
    {"title": "Ordinary Angels", "slug": "ordinary-angels--7589012"},
    {"title": "Anora", "slug": "anora--7601234"},
    {"title": "Killers of the Flower Moon", "slug": "killers-of-the-flower-moon--5407845"},
    {"title": "Spider-Man: No Way Home","slug": "spider-man-no-way-home--6711021"},
    {"title": "Top Gun: Maverick", "slug": "top-gun-maverick--6625758"},
    {"title": "Avatar: The Way of Water","slug": "avatar-the-way-of-water--6970717"},
    {"title": "John Wick: Chapter 4","slug": "john-wick-chapter-4--7082450"},
    {"title": "A Quiet Place Part II", "slug": "a-quiet-place-part-ii--5745586"},
    {"title": "Doctor Strange in the Multiverse of Madness","slug": "doctor-strange-in-the-multiverse-of-madness--6711019"},
    {"title": "Day Shift", "slug": "day-shift--7399487", "release": "2022-08-12"},
    {"title": "Bad Boys for Life", "slug": "bad-boys-for-life--6209913", "release": "2020-01-17"},
    {"title": "The Northman", "slug": "the-northman--7335014", "release": "2022-04-22"},
    {"title": "The Devil All the Time", "slug": "the-devil-all-the-time--6375077", "release": "2020-09-16"},
    {"title": "Poor Things", "slug": "poor-things--7543210", "release": "2023-09-01"},
    {"title": "The Matrix Resurrections", "slug": "the-matrix-resurrections--6987643", "release": "2021-12-22"},
    {"title": "Morbius", "slug": "morbius-film--5966105", "release": "2022-04-01"},
    {"title": "Interceptor", "slug": "interceptor--7534343", "release": "2022-06-03"},
    {"title": "The Invisible Man", "slug": "the-invisible-man--6314523", "release": "2020-02-28"},
    {"title": "Free Guy", "slug": "free-guy--6563567", "release": "2021-08-13"},
    {"title": "Tenet", "slug": "tenet--6185248", "release": "2020-08-26"},
    {"title": "The Batman", "slug": "the-batman--7011009", "release": "2022-03-04"}



]
    scrape_eksi_pages(films)
