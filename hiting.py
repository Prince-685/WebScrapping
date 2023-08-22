import time
from bs4 import BeautifulSoup
from selenium import webdriver
import csv

# Set up the Chrome WebDriver (make sure you have ChromeDriver installed)
driver = webdriver.Chrome()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def scrape_product_page(url):
    try:
        driver.get(url)  # Open the product URL using Selenium

        # Wait for the page to load (adjust this based on your needs)
        time.sleep(1)  # Wait for 1 seconds (for example)

        # Get the page source after it's been modified by JavaScript
        source = driver.page_source
        soup = BeautifulSoup(source, 'html.parser')

        # Extract description, ASIN, product description, and manufacturer
        product_description_elem = soup.select_one("div#productDescription p span")
        if product_description_elem==None:product_description="Not Found"
        else:product_description = product_description_elem.get_text().strip() if product_description_elem else "Not found"

        asin_elem = soup.select_one("div#title_feature_div")
        asin = asin_elem['data-csa-c-asin'] if asin_elem else "Not found"

        manufacturer_elem = soup.select_one('div#detailBullets_feature_div')
        if manufacturer_elem==None: 
            manufacturer_elem=soup.select_one('table#productDetails_techSpec_section_1')
            manufacturer=manufacturer_elem.select_one('tr:nth-of-type(2) td').get_text().strip()
        else:manufacturer = manufacturer_elem.select_one('ul.detail-bullet-list li:nth-of-type(3)').get_text().strip().replace('\n','').replace('\u200f','').replace('\u200e','') if manufacturer_elem else "Not found"

        return asin,product_description,manufacturer
    except Exception as e:
        print(f"Error scraping URL: {url}")
        return "Not found", "Not found", "Not found"

# Load URLs from Bags.csv and scrape additional data
scraped_data = []
urls_to_scrape = 250

with open('Bags.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip the header row
    for row in csv_reader:
        if urls_to_scrape == 0:
            break
        product_url = row[4]  # Assuming URL is in the 5th column
        asin,product_description,manufacturer = scrape_product_page(product_url)

        scraped_data.append({
            "ASIN": asin,
            "Product Name": row[1],
            "Product URL": product_url,
            "Product Price": row[2],
            "Rating": row[3],
            "Number of Reviews": row[5],
            "Manufacturer": manufacturer
        })
        urls_to_scrape -= 1

        time.sleep(1)  # Introduce a delay of 1 seconds

# Save scraped data to a new CSV file
new_csv_filename = 'Bags_with_additional_data.csv'

with open(new_csv_filename, 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["S.no","ASIN", "Product Name", "Product URL", "Product Price", "Product Description", "Rating", "Number of Reviews", "Manufacturer"])
    i=0
    for data in range(len(scraped_data)):
        writer.writerow([i+1,scraped_data[i]])
        i=i+1

# Close the WebDriver when done
driver.quit()
