Amazon.in Laptop Scraper


📘 Overview
This project is a simple Python web scraper that collects laptop listings from Amazon.in search results and saves them into a CSV file.
The script automatically extracts key product details, such as image, title, rating, price, and whether the item is an Ad (sponsored) or Organic result.

🧠 What the Script Does
When executed, the script:

Sends a request to the Amazon search results page for a keyword (default: laptop).

Parses the HTML using BeautifulSoup.

Extracts information for each product:

🖼 Image URL

🏷 Title

⭐ Rating

💰 Price

🔗 Product URL

📦 ASIN (Amazon Product ID)

🏷 Ad / Organic label

Saves the scraped data into a timestamped CSV file, such as

amazon_laptops_laptop_20251116_101523.csv
⚙️ Features
✅ Scrapes multiple pages of Amazon search results
✅ Automatically detects “Sponsored” (Ad) vs “Organic” products
✅ Randomized user-agents and request delays to reduce blocking
✅ Saves output in a clean CSV format with a unique timestamp
✅ Easy-to-modify, lightweight, and requires only standard Python libraries

🧩 Requirements
Make sure Python 3.8 or later is installed.

Install dependencies:
pip install requests beautifulsoup4 pandas lxml

▶️ How to Run the Script
🪜 Step-by-Step Instructions

1. Clone or download the repository
git clone https://github.com/<yourusername>/amazon-laptop-scraper.git
cd amazon-laptop-scraper

3. Create and activate a virtual environment (recommended)
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

4. Install dependencies
   
pip install -r requirements.txt

6. Run the scraper
   
python amazon_laptop_scraper.py --query "laptop" --pages 3

Example Output Columns

| Column          | Description              |
| --------------- | ------------------------ |
| `asin`          | Amazon product ID        |
| `title`         | Product name             |
| `price`         | Price text (₹ included)  |
| `rating`        | Customer rating          |
| `image`         | Product image URL        |
| `product_url`   | Direct product page link |
| `ad_or_organic` | Shows “Ad” or “Organic”  |
