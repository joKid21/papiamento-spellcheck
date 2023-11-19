from bs4 import BeautifulSoup
import requests

def scrape_text(url):
    try:
        page = requests.get(url)
        page.raise_for_status()  # Raise an HTTPError for bad responses

        soup = BeautifulSoup(page.text, features="html.parser")
        heading = soup.find('h1', class_="entry-title").text.strip()

        with open('scraped_content.txt', 'a', encoding='utf-8') as file:
            file.write(heading + '\n')

            text = soup.find_all('p')
            for paragraph in text:
                file.write(paragraph.get_text() + '\n\n')

        print(f'Successfully scraped content from {url} and saved to scraped_content.txt')

    except requests.exceptions.RequestException as e:
        print(f'Error: {e}. Unable to scrape content from {url}')

if __name__ == '__main__':
    url_to_scrape = 'https://24ora.com/sindicato-di-bombero-sinba-a-presenta-nan-relato-financiero-na-su-miembresia/'
    scrape_text(url_to_scrape)
