__all__ = ['scraper', 'dump']

from whisky_de.scraper import WhiskyScraper


def get(page_url):
    return WhiskyScraper().extract_data(page_url)
