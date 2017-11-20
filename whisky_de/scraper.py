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
            'img' : soup.find( id='image-zoom-first-image').get('src')
        })

        article_amounts = soup.find('div', class_='article-amount').text.strip().split('\n')
        ret['alcohol_%'] = float(article_amounts[1].replace('% vol', '').strip())


        #tasteboxes
        ret['taste_box_sherry_port_barrel'] =  soup.find(id="tastevote_criteriainput_0").get('value')
        ret['taste_box_smoke_torf'] =  soup.find(id="tastevote_criteriainput_1").get('value')
        ret['taste_box_sweet'] =  soup.find(id="tastevote_criteriainput_2").get('value')
        ret['taste_box_fruits'] =  soup.find(id="tastevote_criteriainput_3").get('value')
        ret['taste_box_abgang'] =  soup.find(id="tastevote_criteriainput_4").get('value')
        ret['taste_box_gesamt'] =  soup.find(id="tastevote_criteriainput_5").get('value')
        ret['taste_box_qualitiy'] =  soup.find(id="tastevote_criteriainput_6").get('value')


        return ret
