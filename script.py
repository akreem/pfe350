import os
import requests
import random
from bs4 import BeautifulSoup
from slugify import slugify

API_URL = "http://localhost:8004/products/api/products/bulk-upload/"
MEDIA_PATH = "media/products"
LOCAL_MEDIA_ROOT = os.path.abspath(MEDIA_PATH)

def download_image(image_url):
    filename = slugify(os.path.basename(image_url).split('?')[0])
    filepath = os.path.join(LOCAL_MEDIA_ROOT, filename)
    if not os.path.exists(filepath):
        img = requests.get(image_url)
        if img.status_code == 200:
            with open(filepath, 'wb') as f:
                f.write(img.content)
    return f"products/{filename}"

def scrape_products():
    url = "https://pharma-shop.tn/957-compl%C3%A9ments-alimentairess?page=4"
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    products = []

    cards = soup.select('.product-miniature')

    for card in cards:
        try:
            name = card.select_one('.product-title').get_text(strip=True)
            price = card.select_one('.price').get_text(strip=True).replace('TND', '').strip().replace(',', '.')
            image_url = card.select_one('img')['src']
            image_path = download_image(image_url)

            product = {
                "name": name,
                "flag": "Sale",
                "price": float(price),
                "sku": f"SKU{random.randint(1000,9999)}",
                "subtitle": "Imported promo",
                "descripition": "Scraped from pharma-shop.tn",
                "quantity": 15,
                "brand": 6,  # adjust to your brand ID
                "tags": ["promotion"],
                "image": image_path,
                "product_image": [{"image": image_path}]
            }

            products.append(product)
        except Exception as e:
            print("Skipping one product due to error:", e)

    return products

def send_to_api(products):
    res = requests.post(API_URL, json=products)
    print("API response:", res.status_code, res.text)

if __name__ == "__main__":
    if not os.path.exists(LOCAL_MEDIA_ROOT):
        os.makedirs(LOCAL_MEDIA_ROOT)

    scraped = scrape_products()
    if scraped:
        send_to_api(scraped)
    else:
        print("No products found.")
