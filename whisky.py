from whisky_de import get
from whisky_de.scraper import WhiskyScraper


#print(WhiskyScraper().number_of_whiskys)

#url='https://www.whisky.de/shop/USA/Rye-Corn-Andere/Jim-Beam-Rye-inkl-gratis-Glas.html'


url='https://www.whisky.de/shop/Schottland/Shetland-Reel-Whisky.html?&searchorigin=2&force_sid=6836377ce01b37762bb87a99b125139a'
url='https://www.whisky.de/shop/Schottland/Single-Malt/Islay/Lagavulin-8-Jahre.html'
url='https://www.whisky.de/shop/Schottland/Single-Malt/Highlands/Oban-14-Jahre.html?force_sid=a34f3edb574a2db9b4150f804554f4ba'
url='https://www.whisky.de/shop/Schottland/Bunnahabhain-M-ine.html?force_sid=49e4932b084a6a28433aed42a31df7df&&searchorigin=2'
url='https://www.whisky.de/shop/Schottland/Kilchoman-Set-Red-Wine-Cask-Sanaig-5J-2012-2017.html?&searchorigin=2&force_sid=453e9309e7fb74dd7cd9734a03465ba3'
url='https://www.whisky.de/shop/Schottland/The-Deveron-18-Jahre.html?force_sid=3e4f889c5323baefdfab0558ed08aa0d&&searchorigin=2'
url='https://www.whisky.de/shop/International/Aichinger-Weizenmalt-No-13-Oesterreich.html?&searchorigin=2'

print(get(url))


#result = WhiskyScraper().pages_urls()
#print(len(result))

pass