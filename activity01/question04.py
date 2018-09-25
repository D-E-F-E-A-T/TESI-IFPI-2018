from libs.myurllib import get_parsed
from time import sleep

base_url = 'http://example.webscraping.com'

for i in range(1,25):
    print('\n   PAGINA SENDO BAIXADA ',i, '\n')
    sleep(0.5)
    soup = get_parsed('%s/places/default/index/%s' % (base_url, i)) 
    countries_urls = [row['href'] for row in soup.find('div', id='results').find_all('a')]
    for coutry_url in countries_urls:	
        country_soup = get_parsed('%s%s'% (base_url, coutry_url))
        country_name = country_soup.find(attrs={'id':'places_country__row'}).find(attrs={'class':'w2p_fw'}).get_text()
        country_population = country_soup.find(attrs={'id':'places_population__row'}).find(attrs={'class':'w2p_fw'}).get_text()
        country_area = country_soup.find(attrs={'id':'places_area__row'}).find(attrs={'class':'w2p_fw'}).get_text().replace(' square kilometres','')
        print('nome do pais: %s | populacao: %s hab | area: %s km2 | densidade demografica : %.2f hab/km2\n' %(country_name,country_population,country_area,   int(country_population.replace(',',''))/int(country_area.replace(',',''))))
        sleep(0.5)