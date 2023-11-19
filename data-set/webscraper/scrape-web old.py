from bs4 import BeautifulSoup
import requests

def Scrape_text(x):
    url=x
    page=requests.get(url)

    soup=(BeautifulSoup(page.text, features="html.parser"))

    Heading=(soup.find('h1', class_="entry-title").text.strip())

    print (Heading)
    text=(soup.find_all('p'))
    for i in text:
        print("\n")
        print(i.get_text())


if __name__ == '__main__':
    pass