import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd
from scrapy.http import Request


class On_Running_Crawler(scrapy.Spider):
    name = "on_running_crawler"
    headers = {
            'authority': 'algolia.on-running.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.on-running.com',
            'referer': 'https://www.on-running.com/',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        }
    main_url = 'https://algolia.on-running.com/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(4.18.0)%3B%20Browser%20(lite)%3B%20instantsearch.js%20(4.56.4)%3B%20Vue%20(2.6.12)%3B%20Vue%20InstantSearch%20(4.10.4)%3B%20JS%20Helper%20(3.13.3)&x-algolia-api-key=bff229776989d153121333c90db826b1&x-algolia-application-id=ML35QLWPOC'
    
    custom_settings = {
        'FEEDS': {
            'items.csv': {
                'format': 'csv',
                'encoding': 'utf8',
                'overwrite': True,
            },
        },
    }

    # parses through all products
    def start_requests(self):
        start_page = 0
        data = '{"requests":[{"indexName":"CH_products_production_v3","params":"clickAnalytics=true&distinct=true&facets=%5B%22productType%22%2C%22productSubtype%22%2C%22genderFilter%22%2C%22family%22%2C%22activities%22%2C%22collections%22%2C%22cushioning%22%2C%22roadRunningStyle%22%2C%22conditions%22%2C%22surface%22%2C%22fit%22%2C%22colorCodes%22%2C%22lacing%22%2C%22features%22%2C%22tags%22%2C%22technology%22%2C%22terrain%22%2C%22productSubtypeStyle%22%5D&filters=NOT%20productUrl%3ANULL%20AND%20NOT%20imageUrl%3ANULL%20AND%20NOT%20groupingKey%3ANULL%20AND%20stores.ch.canBePurchased%3Atrue%20AND%20stores.ch.isHiddenFromSearch%3Afalse%20AND%20NOT%20tags%3Aexclude_from_plp%20AND%20NOT%20tags%3Aclassics%20AND%20NOT%20tags%3Alost_and_found&highlightPostTag=__%2Fais-highlight__&highlightPreTag=__ais-highlight__&maxValuesPerFacet=50&page='+ str(start_page)+ '&tagFilters=&userToken=xxxxxxxx"}]}'

        yield Request(self.main_url, callback=self.parse, method="POST", body=data, headers=self.headers)

    def parse(self, response):
        response_data = response.json()
        totalPages=int(response_data.get('results')[0].get('nbPages'))
        current_page=int(response_data.get('results')[0].get('page'))

        print(f"Page number: {current_page}")
        hits = response_data['results'][0]['hits']
        for item in hits:
            name = item['name']
            price = item['stores']['ch']['price']
            skus = item['stores']['ch']['purchasableSkus']
            prod_url = 'https://www.on-running.com/en-ch' + item['productUrl']
            last_sync = item['lastStockSynced']
            stock = item['stock']

            result={}
            result['Product_name'] = name
            result['Product_url'] = prod_url
            result['Product_stock'] = stock
            result['Product_price'] = price
            result['Product_skus'] = skus
            result['Product_last_sync'] = last_sync
            yield result

        start_page = current_page + 1

        if start_page<=totalPages:
            data = '{"requests":[{"indexName":"CH_products_production_v3","params":"clickAnalytics=true&distinct=true&facets=%5B%22productType%22%2C%22productSubtype%22%2C%22genderFilter%22%2C%22family%22%2C%22activities%22%2C%22collections%22%2C%22cushioning%22%2C%22roadRunningStyle%22%2C%22conditions%22%2C%22surface%22%2C%22fit%22%2C%22colorCodes%22%2C%22lacing%22%2C%22features%22%2C%22tags%22%2C%22technology%22%2C%22terrain%22%2C%22productSubtypeStyle%22%5D&filters=NOT%20productUrl%3ANULL%20AND%20NOT%20imageUrl%3ANULL%20AND%20NOT%20groupingKey%3ANULL%20AND%20stores.ch.canBePurchased%3Atrue%20AND%20stores.ch.isHiddenFromSearch%3Afalse%20AND%20NOT%20tags%3Aexclude_from_plp%20AND%20NOT%20tags%3Aclassics%20AND%20NOT%20tags%3Alost_and_found&highlightPostTag=__%2Fais-highlight__&highlightPreTag=__ais-highlight__&maxValuesPerFacet=50&page='+ str(start_page)+ '&tagFilters=&userToken=xxxxxxxx"}]}'
            yield Request(self.main_url, callback=self.parse, method="POST", body=data, headers=self.headers)

process = CrawlerProcess()
process.crawl(On_Running_Crawler)
process.start()    
