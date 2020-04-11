from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
import product_crawlers.settings


DeclarativeBase = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**product_crawlers.settings.DATABASE))


def create_products_table(engine):
    DeclarativeBase.metadata.create_all(engine)


class Products(DeclarativeBase):
    """Sqlalchemy Products model"""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column('Name', String)
    origin_domain = Column('Origin_Domain', String)
    origin_url = Column('Origin_URL', String)
    extract_date = Column('extract_date', DateTime)
    price = Column('Price', String, nullable=True)