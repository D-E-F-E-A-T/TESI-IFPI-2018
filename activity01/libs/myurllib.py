from bs4 import BeautifulSoup as bs
from sqlalchemy import create_engine, Column, String, Integer, Float, Date, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import requests

# create an engine
engine = create_engine('sqlite:///mydb.db')

Base = declarative_base()

class Moment(Base):
    __tablename__ = 'moments'

    id = Column(Integer, primary_key=True)
    temperature = Column(String)
    condition = Column(String)
    sensation = Column(String)
    humidity = Column(String)
    pressure = Column(String)
    wind = Column(String)
    update = Column(String)

    def __init__(self, temperature, condition, sensation, humidity, pressure, wind, update):
        self.temperature = temperature
        self.condition = condition
        self.sensation = sensation
        self.humidity = humidity
        self.pressure = pressure
        self.wind = wind
        self.update = update

    def __str__(self):
        return 'Temperatura de tereina: %s, em: %s' % (self.temperature, self.update)

Base.metadata.create_all(engine)

# create a configured "Session" class
Session = sessionmaker(bind=engine)

# create a Session
session = Session()

def download(url, num_retries=2, quiet = False):
    
    if not quiet:
        print('Downloading data from:', url)
    page = None
    try:
        response = requests.get(url)
        page = response.text
        if response.status_code >= 400:
            print('Download error:', response.text)
        if num_retries and 500 <= response.status_code < 600:
            return download(url, num_retries - 1)
    except requests.exceptions.RequestException as e:
        print('Download error:', e.reason)
    return page

def get_parsed(url, num_retries=2, quiet = False):
    soup = bs(download(url, num_retries, quiet), 'html.parser')
    return soup

def easy_get_text(soup, str, id, is_class = False):
    if is_class:
        return soup.find(str,class_=id).get_text()
    return soup.find(str,id=id).get_text()

if __name__ == '__main__':
    a = download('http://www.google.com')
    print(a)