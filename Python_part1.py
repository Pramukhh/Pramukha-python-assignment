import requests
from bs4 import BeautifulSoup
import re

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

        # Extract product URL
        product_url = product.find("a", class_="a-link-normal s-no-outline")["href"]
        product_info["Product URL"] = "https://www.amazon.in" + product_url

        # Extract product name
        product_name = product.find("span", class_="a-text-normal").get_text()
        product_info["Product Name"] = product_name.strip()

        # Extract product price
        product_price = product.find("span", class_="a-offscreen")
        if product_price:
            product_info["Product Price"] = product_price.get_text()

        # Extract rating and number of reviews
        rating = product.find("span", class_="a-icon-alt")
        if rating:
            rating_text = rating.get_text()
            product_info["Rating"] = float(re.search(r"(\d+\.\d+)", rating_text).group(1))

            reviews_count = product.find("span", {"aria-label": re.compile(r"\d+ ratings?")})
            if reviews_count:
                product_info["Number of reviews"] = int(re.search(r"(\d+)", reviews_count["aria-label"]).group(1))
        else:
            product_info["Rating"] = None
            product_info["Number of reviews"] = None

        product_data.append(product_info)

# Print scraped data
for product in product_data:
    print(product)
