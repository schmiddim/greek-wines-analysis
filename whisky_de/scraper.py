from decimal import Decimal
from re import sub

import requests as req
from bs4 import BeautifulSoup
from tqdm import tqdm


class WhiskyScraper:
    def __init__(self):
        self._session = req.Session()

    def extract_data(self, page_url):
        soup = BeautifulSoup(self._session.get(page_url).content, 'lxml')

        def find_non_empty(tag, expected_type=str, **kwargs):
            assert expected_type in {str, float, int}

            res = soup.find(tag, **kwargs)
            return res.text if res else ''

        ret = dict({
            'url': page_url,
            'name': find_non_empty('span', itemprop='name'),
            'description': find_non_empty('div', class_='article-description-short').replace('\n', '').replace('\r',
                                                                                                               ' ').rstrip(
                ' '),
            'avg_rating_%': float(find_non_empty('span', class_='rating-value')),
            'n_votes': int(find_non_empty('span', class_='rating-count').replace('(', '').replace(')', '')),
            'price': int(find_non_empty('span', class_='article-price-default').replace('EUR', '').replace(',', '')),
            'whisky_type': soup.select("div.productMainInfo  > div.article-attributes  > ul > li")[0].text.replace(
                'Sorte:', '').strip(),
            'img': soup.find(id='image-zoom-first-image').get('src')
            'distillery': find_non_empty('div',  class_= 'article-company').strip()

        })

        article_amounts = soup.find('div', class_='article-amount').text.strip().split('\n')
        ret['alcohol_%'] = float(article_amounts[1].replace('% vol', '').strip())


        #Country
        items =soup.find('form', id='cloud-zoom-width').findAll('div' , class_="list-csv")
        ret['country'] = items[1].text.replace('Herkunftsland:', '').strip().split('\n') [1]


        ret['taste_box_sherry_port_barrel'] = soup.find(id="tastevote_criteriainput_0").get('value')
        ret['taste_box_smoke_torf'] = soup.find(id="tastevote_criteriainput_1").get('value')
        ret['taste_box_sweet'] = soup.find(id="tastevote_criteriainput_2").get('value')
        ret['taste_box_fruits'] = soup.find(id="tastevote_criteriainput_3").get('value')
        ret['taste_box_gravy'] = soup.find(id="tastevote_criteriainput_4").get('value')
        ret['taste_box_total'] = soup.find(id="tastevote_criteriainput_5").get('value')
        ret['taste_box_qualitiy'] = soup.find(id="tastevote_criteriainput_6").get('value')

        return ret

    @property
    def number_of_whiskys(self):
        bla = int(
            BeautifulSoup(self._session.get('http://www.houseofwine.gr/how/wine.html?mode=list').content, 'lxml'
                          ).find('p',
                                 class_='amount'
                                 ).text.replace('\n', '').replace('\r', '').lstrip(' ').rstrip(' ').split(' ')[
                -2])  # Είδη 1 εώς 25 από 1123 σύνολο
        return bla
        # def pages_urls(selfself, page_size=30):
        #     page_urls = set()
        #     n_pages= self.number_of_
