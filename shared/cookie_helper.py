# cookie_helper.py
import pickle, os

TXT = "eksi_cookies.txt"
PKL = "eksi_cookies.pkl"

def txt_to_pkl():
    cookies = []
    with open(TXT, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) >= 7:
                cookies.append({
                    "domain": parts[0],
                    "path":  parts[2],
                    "secure": parts[3].lower() == "true",
                    "name":  parts[5],
                    "value": parts[6]
                })
    pickle.dump(cookies, open(PKL, "wb"))
    print("✅ Cookie’ler pickle’a aktarıldı →", PKL)

if __name__ == "__main__":
    txt_to_pkl()
