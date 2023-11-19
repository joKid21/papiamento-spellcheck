from bs4 import BeautifulSoup
import requests,time
from scrape_web import scrape_text


links=[]
# Function to extract unique links from a page
def extract_links(page_url):
    page = requests.get(page_url)
    soup = BeautifulSoup(page.text, features="html.parser")
    div_with_links = soup.find('div', class_='td-ss-main-content')
    links_in_div = div_with_links.find_all('a', href=True)
    unique_links = set()

    for link in links_in_div:
        href = link['href']
        if href != "/category/local/" and not href.startswith("https://24ora.com/category/local/page/"):
            unique_links.add(href)

    return unique_links

# Define the base URL
base_url = 'https://24ora.com/category/local/'

# Specify the number of pages to scrape (e.g., 30)
num_pages_to_scrape = 30

# Use a set to store all unique links from all pages
all_unique_links = set()

# Iterate through each page
for page_num in range(1, num_pages_to_scrape + 1):
    page_url = f'{base_url}page/{page_num}/'
    page_links = extract_links(page_url)
    all_unique_links.update(page_links)

# Print or process all unique links
for unique_link in all_unique_links:
    links.append(unique_link)


for i in links:
    scrape_text(i)
    time.sleep(0.5)
