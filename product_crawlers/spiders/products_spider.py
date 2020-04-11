from product_crawlers.items import ProductCrawlersItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from datetime import datetime
import scrapy
# -*- coding: utf-8 -*-


class ProductCrawlersSpider(CrawlSpider):
    """
        Spider that will crawl will fetch the "product name" and "product line" foreach URL specified in the Offers Catalog.
    """
    
    name = 'product_crawlers'
    allowed_domains = ['mercadolivre.com.br',
                       'magazineluiza.com.br', 
                       'casasbahia.com.br']

    def start_requests(self):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}

        with open('C:\\Users\\gaco1\\Dev\\Estudando\\Trabalho\\offers.csv', 'r') as offers_file:
            for line in offers_file:
                try:
                    if not line.strip():
                        continue
                    yield scrapy.Request(url=line, callback=self.parse, headers=headers)
                except Exception:
                    self.log(">> Exception when trying to read url:", line)

    def parse(self, response):
        
        # Create an extracted list of product items
        productsItem = ProductCrawlersItem()
        origin_url = response.url
        try:
            # MERCADO LIVRE
            if 'https://www.mercadolivre.com.br' in origin_url:
                origin_domain = 'mercadolivre.com.br'
                self.addProductItem(productsItem,
                                    response.xpath('//*[@id="short-desc"]/div/header/h1').css('.item-title__primary::text').get().strip(), 
                                    response.xpath('//*[@id="productInfo"]/fieldset/span/span[2]').css('.price-tag-fraction::text').get(), 
                                    origin_domain, 
                                    origin_url)
                
            # MAGAZINE LUIZA
            elif 'https://www.magazineluiza.com.br' in origin_url:
                origin_domain = 'magazineluiza.com.br'
                self.addProductItem(productsItem,
                                    response.css('title::text').get(),
                                    response.xpath('//html/body/div[3]/div[5]/div[1]/div[4]/div[2]/div[4]/div/div/div/span[2]').css('.price-template__text::text').get(),
                                    origin_domain,
                                    origin_url)
            
            # CASAS BAHIA
            ### Não havia produtos disponíveis
            elif 'https://www.casasbahia.com.br' in origin_url:
                raise Exception
        except Exception:
            self.log(">> Exception when trying to parse: {0}".format(origin_url))
            self.addProductItem(productsItem, 'ERROR_UNKNOWN', '', origin_domain, origin_url)
        
        yield productsItem

    def addProductItem(self, productsItem, name, price, origin_domain, origin_url):
        productsItem['name'] = name
        productsItem['price'] = price
        productsItem['origin_domain'] = origin_domain
        productsItem['origin_url'] = origin_url
        productsItem['extract_date'] = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
