# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import sessionmaker
from product_crawlers.models import Products, db_connect, create_products_table

class ProductCrawlersPipeline(object):
    """Products pipeline for storing scraped product into database"""

    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates products table.
        """
        engine = db_connect()
        create_products_table(engine)
        self.Session = sessionmaker(bind=engine)
        
    def process_item(self, item, spider):
            """Save Products in database.

            This method is called for every item pipeline component.

            """
            print("ITEMZINHO:", item)
            session = self.Session()
            productItem = Products(**item)

            try:
                session.add(productItem)
                session.commit()
            except:
                session.rollback()
                raise
            finally:
                session.close()

            return item