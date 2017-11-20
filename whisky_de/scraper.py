from decimal import Decimal
from re import sub

import requests as req
from bs4 import BeautifulSoup
from tqdm import tqdm


class WhiskyScraper:
    def __init__(self, country='Scotland'):
        self._session = req.Session()
        self._country = country

    @property
    def number_of_whiskys(self):
        bs = BeautifulSoup(self._session.get('https://www.whisky.de/shop/Schottland/').content, 'lxml')
        count = int(bs.find('div', class_='list-locator-count').find('strong').text)
        return count

    def extract_data(self, page_url):
        soup = BeautifulSoup(self._session.get(page_url).content, 'lxml')
        print(page_url)

        def find_non_empty(tag, expected_type=str, **kwargs):
            assert expected_type in {str, float, int}

            res = soup.find(tag, **kwargs)
            return res.text if res else ''

        ret = dict({
            'name': find_non_empty('span', itemprop='name'),
            'country': self._country,
            'whisky_type': None,
            'price' : None,
            'alcohol_%': None,
            'avg_rating_%': None,
            'n_votes': None,
            'price': int(
                find_non_empty('span', class_='article-price-default').replace('EUR', '').replace(',', '').replace('.',
                                                                                                                   '')),
            'distillery': find_non_empty('div', class_='article-company').strip(),
            'url': page_url,
            'img': soup.find(id='image-zoom-first-image').get('src'),
            'description': find_non_empty('div', class_='article-description-short').replace('\n', '').replace('\r',
                                                                                                               ' ').rstrip(
                ' '),

        })
        ret['price'] = int(
            find_non_empty('span', class_='article-price-default').replace('EUR', '').replace(',', '').replace('.',
                                                                                                               '')),
        ret['whisky_type'] = soup.select("div.productMainInfo  > div.article-attributes  > ul > li")[0].text.replace(
            'Sorte:',
            '').strip(),

        # Rating value
        str_rating_value = find_non_empty('span', class_='rating-value')
        if str_rating_value != '':
            ret['avg_rating_%'] = float(str_rating_value.strip().replace(',','.'))
            ret['n_votes'] = soup.find("a", itemprop='aggregateRating').find('span',
                                                                             class_='rating-count').text.replace('(',
                                                                                                                 '').replace(
                ')', '').strip()

        article_amounts = soup.find('div', class_='article-amount').text.strip().split('\n')
        if len(article_amounts) > 1:
            ret['alcohol_%'] = float(article_amounts[1].replace('% vol', '').replace(',', '.').strip())

        if soup.find(id="tastevote_criteriainput_0") != None:
            ret['taste_box_sherry_port_barrel'] = soup.find(id="tastevote_criteriainput_0").get('value')
            ret['taste_box_smoke_torf'] = soup.find(id="tastevote_criteriainput_1").get('value')
            ret['taste_box_sweet'] = soup.find(id="tastevote_criteriainput_2").get('value')
            ret['taste_box_fruits'] = soup.find(id="tastevote_criteriainput_3").get('value')
            ret['taste_box_gravy'] = soup.find(id="tastevote_criteriainput_4").get('value')
            ret['taste_box_total'] = soup.find(id="tastevote_criteriainput_5").get('value')
            ret['taste_box_qualitiy'] = soup.find(id="tastevote_criteriainput_6").get('value')
        return ret


    def pages_urls(self, page_size=30):
        wine_page_urls = set()
        n_pages = int(self.number_of_whiskys / page_size + 1)
        n_pages = 43

        for current_page in tqdm(range(0, n_pages + 1), desc='Scraping  page urls', unit='page'):
            page_url = "https://www.whisky.de/shop/Schottland/?_artperpage=30&pgNr={}".format(current_page)
            page_soup = BeautifulSoup(req.get(page_url).content, 'lxml')
            wine_urls = map(lambda li: li.find('a').get('href'),
                            page_soup.find_all('div', class_='article-more', recursive=True)
                            )
            wine_page_urls.update(wine_urls)
        return wine_page_urls

    def whiskys(self):

        wines = []

        wine_pages_urls = list(self.pages_urls())
        for url in tqdm(wine_pages_urls, desc='Scraping Whiskys', unit='whisky', total=len(wine_pages_urls)):
            wines.append(self.extract_data(url))
        return wines
