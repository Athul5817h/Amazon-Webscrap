
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import argparse
from datetime import datetime
import urllib.parse

# A small rotation of user agents to reduce immediate blocking
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15"
]

BASE_SEARCH = "https://www.amazon.in/s"

def get_search_html(search_term, page=1, timeout=15):
    """
    Fetch HTML for the search page for `search_term` and `page`.
    """
    params = {"k": search_term, "page": page}
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-IN,en;q=0.9"
    }
    url = BASE_SEARCH + "?" + urllib.parse.urlencode(params)
    resp = requests.get(url, headers=headers, timeout=timeout)
    resp.raise_for_status()
    return resp.text

def parse_search_results(html):
    """
    Parse products from Amazon search HTML and return a list of dicts.
    """
    soup = BeautifulSoup(html, "lxml")
    items = []

    # Each product container on Amazon search usually has attribute data-asin
    for card in soup.select("div[data-asin]"):
        asin = card.get("data-asin", "").strip()
        if not asin:
            continue

        # Title and product url
        title_tag = card.select_one("h2 a.a-link-normal.a-text-normal, h2 a.a-link-normal span")
        title = title_tag.get_text(strip=True) if title_tag else None
        product_url = None
        a_tag = card.select_one("h2 a.a-link-normal") or card.select_one("a.a-link-normal.s-no-outline")
        if a_tag and a_tag.get("href"):
            product_url = urllib.parse.urljoin("https://www.amazon.in", a_tag.get("href"))

        # Image
        img_tag = card.select_one("img.s-image")
        image = img_tag.get("src") if img_tag and img_tag.get("src") else None

        # Price - try several selectors
        price = None
        # preferred: offscreen price that includes currency symbol
        offscreen = card.select_one("span.a-price span.a-offscreen")
        if offscreen:
            price = offscreen.get_text(strip=True)
        else:
            whole = card.select_one(".a-price .a-price-whole")
            frac = card.select_one(".a-price .a-price-fraction")
            if whole:
                price = whole.get_text(strip=True) + (frac.get_text(strip=True) if frac else "")

        # Rating
        rating = None
        rating_tag = card.select_one("i.a-icon-star-small span, i span.a-icon-alt, span.a-icon-alt")
        if rating_tag:
            rating = rating_tag.get_text(strip=True)

        # Ad / Organic: look for sponsored labels within the card
        ad_flag = False
        # Common indicators: "Sponsored", "Ad", "Sponsored by"
        sponsored_labels = card.select("span.s-sponsored-label-text, span.s-label-popover-default")
        if sponsored_labels:
            ad_flag = True
        # fallback check in text
        if "Sponsored" in (card.get_text() or ""):
            ad_flag = True

        items.append({
            "asin": asin,
            "title": title,
            "price": price,
            "rating": rating,
            "image": image,
            "product_url": product_url,
            "ad_or_organic": "Ad" if ad_flag else "Organic"
        })

    return items

def scrape(search_term="laptop", pages=3, delay_range=(1.5, 3.5)):
    all_items = []
    for p in range(1, pages+1):
        try:
            print(f"[+] Fetching page {p} for '{search_term}' ...")
            html = get_search_html(search_term, page=p)
            items = parse_search_results(html)
            if not items:
                print("[-] No items found on this page — Amazon layout may have changed or content blocked.")
                break
            all_items.extend(items)
            # polite random delay
            time.sleep(random.uniform(*delay_range))
        except requests.HTTPError as e:
            print(f"HTTP error on page {p}: {e}")
            break
        except Exception as e:
            print(f"Error on page {p}: {e}")
            break

    # Save to CSV with timestamp
    if all_items:
        df = pd.DataFrame(all_items)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"amazon_laptops_{search_term.replace(' ','_')}_{ts}.csv"
        df.to_csv(filename, index=False, encoding="utf-8")
        print(f"[+] Saved {len(df)} rows to {filename}")
        return filename
    else:
        print("[-] No data scraped.")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Amazon.in laptop scraper")
    parser.add_argument("--query", type=str, default="laptop", help="Search query (default: laptop)")
    parser.add_argument("--pages", type=int, default=3, help="Number of search result pages to scrape")
    args = parser.parse_args()

    scrape(search_term=args.query, pages=args.pages)
