import time
from bs4 import BeautifulSoup
from selenium import webdriver
import csv

# Set up the Chrome WebDriver (make sure you have ChromeDriver installed)
driver = webdriver.Chrome()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

Names = []
Prices = []
Url = [] 
Rating = []
Review = []

for n in range(2, 21):
    s = f'https://www.amazon.in/s?k=bag&page={n}&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{n}'
    driver.get(s)  # Open the URL using Selenium

    # Wait for the page to load (adjust this based on your needs)
    time.sleep(1)  # Wait for 5 seconds (for example)

    # Get the page source after it's been modified by JavaScript
    source = driver.page_source
    soup = BeautifulSoup(source, 'html.parser')

    # Find all product containers on the page
    product_containers = soup.find_all("div", {"data-asin": True})

    for container in product_containers:
        # Find product name
        product_name_elem = container.select_one("h2 span.a-text-normal")
        product_name = product_name_elem.get_text() if product_name_elem else "Not found"
        Names.append(product_name)

        # Find product URL
        product_url_elem = container.select_one("h2 a.a-link-normal")
        product_url = "https://amazon.in" + product_url_elem['href'] if product_url_elem else "Not found"
        Url.append(product_url)

        # Find product price
        product_price_elem = container.select_one("span.a-price span.a-offscreen")
        product_price = "Rs" + product_price_elem.get_text().replace(',', '') if product_price_elem else "Not found"
        Prices.append(product_price)

        # Find product rating
        product_rating_elem = container.select_one("i span.a-icon-alt")
        product_rating = product_rating_elem.get_text() if product_rating_elem else "Not available"
        Rating.append(product_rating)

        # Find number of reviews
        num_reviews_elem = container.select_one("div.a-spacing-top-micro span.a-size-base.s-underline-text")
        num_reviews = num_reviews_elem.get_text() if num_reviews_elem else "No Reviews found"
        Review.append(num_reviews)

    time.sleep(2)  # Introduce a delay of 2 seconds

# Close the WebDriver when done
driver.quit()


file_name = 'Bags.csv'

with open(file_name, 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Sr.No', 'Product Name', 'Price', 'Rating', 'Url', 'No. of Reviews'])

    for i in range(len(Names)):
        writer.writerow([i + 1, Names[i], Prices[i], Rating[i], Url[i], Review[i]])
