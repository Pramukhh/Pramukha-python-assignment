import requests
from bs4 import BeautifulSoup
import re
import csv

base_url = "https://www.amazon.in/s"
search_params = {
    "k": "bags",
    "crid": "2M096C61O4MLT",
    "qid": "1653308124",
    "sprefix": "ba,aps,283",
    "ref": "sr_pg_1"
}

product_data = []

# Scrape multiple pages
for page in range(1, 21):
    search_params["page"] = page
    response = requests.get(base_url, params=search_params)
    soup = BeautifulSoup(response.content, "html.parser")

    products = soup.find_all("div", class_="s-result-item")

    for product in products:
        product_info = {}

        # ... (code to extract previous fields)

        product_data.append(product_info)

# Scrape additional details from product URLs
for product in product_data:
    url = product["Product URL"]
    response = requests.get(url)
    product_soup = BeautifulSoup(response.content, "html.parser")

    # Extract ASIN
    asin_tag = product_soup.find("th", string="ASIN")
    if asin_tag:
        product["ASIN"] = asin_tag.find_next("td").get_text()

    # Extract Product Description
    description_tag = product_soup.find("h2", string="Product Description")
    if description_tag:
        product["Product Description"] = description_tag.find_next("p").get_text()

    # Extract Manufacturer
    manufacturer_tag = product_soup.find("th", string="Manufacturer")
    if manufacturer_tag:
        product["Manufacturer"] = manufacturer_tag.find_next("td").get_text()

# Export data to CSV
csv_filename = "amazon_product_data.csv"
with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = [
        "Product URL", "Product Name", "Product Price", "Rating", "Number of reviews",
        "ASIN", "Product Description", "Manufacturer"
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for product in product_data:
        writer.writerow(product)

print(f"Data exported to {csv_filename}")
