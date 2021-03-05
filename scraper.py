import os
import string
import re
import requests
from bs4 import BeautifulSoup

URL_NATURE = 'https://www.nature.com'
HEADERS = {'Accept-Language': 'en-US,en;q=0.5'}


def make_dirs(pages):
    for page in range(1, pages+1):
        dir_name = 'Page_' + str(page)
        dir_path = './' + dir_name
        if dir_name not in os.listdir():
            os.mkdir(dir_path)


def save_article(article, page):
    article_title = article.find('a', {'class': 'c-card__link'})
    article_link = str(article_title['href'])

    response = requests.get(URL_NATURE + article_link, headers=HEADERS)
    if not response:  # if server returns 4xx or 5xx
        print(article_link, 'returned ', response.status_code)
        return False

    soup = BeautifulSoup(response.content, 'html.parser')

    article_content = soup.find('div', {'class': re.compile('.*body.*')})
    if article_content is None:
        print(URL_NATURE + article_link, 'Article content not found')
        return False

    file_name = article_title.string.strip().translate(str.maketrans(' ', '_', string.punctuation))
    file = open(os.path.join(f'./Page_{page}',  f'{file_name}.txt'), 'wb')
    file.write(article_content.text.strip().encode("utf-8"))
    print(article_link, 'Success')
    file.close()
    return


def nature_scraper(pages, article_type):
    url = URL_NATURE + '/nature/articles'
    for page in range(1, pages+1):
        response = requests.get(url, headers=HEADERS, params={'page': page})
        if not response:  # if server returns 4xx or 5xx
            print(url, 'returned ', response.status_code)
            return False

        soup = BeautifulSoup(response.content, 'html.parser')

        articles = soup.findAll('article')
        for article in articles:
            type_from_article = article.find('span', {'data-test': 'article.type'}).text.strip('\n')
            if type_from_article == article_type:
                save_article(article, page)
    return


def main():
    pages = int(input('Number of pages:\n'))  # < 1
    article_type = input('Type of articles:\n')
    make_dirs(pages)  # make dirs even there's no content in it, req by hyperskill tests
    nature_scraper(pages, article_type)
    print('Done.')


if __name__ == '__main__':
    main()
