from bs4 import BeautifulSoup
import requests
import csv

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

Names = []
Prices = []
Url = [] 
Rating = []
Review = []








s='https://www.amazon.in/s?k=bag&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283ref=sr_pg_1'
source = requests.get(s, headers = headers).text
soup = BeautifulSoup(source, 'lxml')

for i in soup.select('div.s-asin span.a-text-normal'):
        string = i.text
        Names.append(string)

for i in soup.select('div.s-asin h2.a-size-mini a.a-text-normal'):
        string = i.attrs['href'] 
        Url.append('https://amazon.in' + string)

for i in soup.select('div.s-asin div.a-section a.a-size-base span.a-price span.a-price-whole'):
        string=i.text
        Prices.append('Rs' + string)

for i in soup.select('div.s-asin i.a-icon span.a-icon-alt'):
        string = i.text
        Rating.append(string)

for i in soup.select('div.s-asin a.a-link-normal span.a-size-base'):
        string = i.text
        Review.append(string)


file_name = 'Bags.csv'

with open(file_name, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(['Sr.No', 'Product Name', 'Price' , 'Rating', 'Url', 'No. of Reviews'])

        for i in range(len(Rating)):
                writer.writerow([i, Names[i], Prices[i], Rating[i], Url[i], Review[i]])
