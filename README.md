Amazon.in Laptop Scraper
📘 Overview
This Python script scrapes Amazon.in search results for laptop listings and extracts the following information for each product:

🖼 Image (product thumbnail URL)

🏷 Title

⭐ Rating

💰 Price

🏷 Ad / Organic Result

🔗 Product URL

🔢 ASIN

All collected data are saved into a timestamped CSV file for later analysis.

⚙️ Features
✅ Automatically fetches multiple pages of search results
✅ Extracts key product fields from each listing
✅ Detects whether a listing is sponsored (Ad) or organic
✅ Saves clean data in CSV format with a timestamp in the filename
✅ Polite scraping – adds randomized delays and header rotation to avoid blocking

🧠 How It Works
Sends an HTTP GET request to the Amazon.in search results page for "laptop"

Parses the HTML response using BeautifulSoup

Locates each product container via data-asin attribute

Extracts:

product title and URL

image link

price and rating

sponsored label (if any)

Repeats the process for the specified number of pages

Combines all results into a single pandas DataFrame

Writes output to a file like

amazon_laptops_laptop_20251116_101523.csv
🧩 Requirements
Install dependencies:

pip install requests beautifulsoup4 pandas lxml
▶️ Usage
Run the script from a terminal:

python amazon_laptop_scraper.py --query "laptop" --pages 3
Arguments

Parameter	Description	Default
--query	Search term (e.g., "laptop", "gaming laptop")	laptop
--pages	Number of result pages to scrape	3
Example output

[+] Fetching page 1 for 'laptop' ...
[+] Fetching page 2 for 'laptop' ...
[+] Fetching page 3 for 'laptop' ...
[+] Saved 64 rows to amazon_laptops_laptop_20251116_101523.csv
Open the CSV in Excel / pandas / Sheets to view product data.

📂 Output Columns
Column	Description
asin	Amazon product identifier
title	Product title
price	Listed price (text format)
rating	Customer rating string
image	Product image URL
product_url	Direct Amazon link
ad_or_organic	Either “Ad” or “Organic” based on sponsored labels
