from whisky_de import get
from whisky_de.scraper import WhiskyScraper


#print(WhiskyScraper().number_of_whiskys)

url='https://www.whisky.de/shop/Schottland/Single-Malt/Islay/Lagavulin-8-Jahre.html'
#url='https://www.whisky.de/shop/USA/Rye-Corn-Andere/Jim-Beam-Rye-inkl-gratis-Glas.html'

print(get(url))