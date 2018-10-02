from bs4 import BeautifulSoup as bs
from sqlalchemy import create_engine, Column, String, Integer, Float, Date, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import requests
from collections import OrderedDict

# create an engine
engine = create_engine('sqlite:///mydb.db')

Base = declarative_base()

OGOL = 'http://www.ogol.com.br/equipa.php?id=%s&search=1'

PESSTAT = 'https://pesstatsdatabase.com/PSD/Players.php?Club=%s&type=0' 

SOFIFA = 'https://sofifa.com/team/%s'

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

class Team(Base):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    ogol_id = Column(Integer, unique=True, nullable=False)
    pesstat_id = Column(Integer, unique=True, nullable=False)
    sofifa_id = Column(Integer, unique=True, nullable=False)
    stadium = Column(String(160), nullable=True)
    rival = Column(String(160), nullable=True)
    captain = Column(String(160), nullable=True)
    league = Column(String(160), nullable=True)

    def get_from_sofifa(self):
        url = SOFIFA % (self.sofifa_id)
        soup = get_parsed(url)
        all = soup.find_all('.pl > li > label')
        
        print(all)

        for i in all:
            a = i.get_text()
            print(a)
            if a.startswith('Home Stadium'):
                print(a)
    
    def get_from_pesstat(self):
        url = PESSTAT % (self.pesstat_id)
        soup = get_parsed(url)
        soup.find(id='info')

    def get_from_ogol(self):
        url = OGOL % (self.ogol_id)
        soup = get_parsed(url)

        all = soup.find_all(class_='info')
        
        print(all)

        for i in all:
            a = i.get_text()
            #print(dir(a))
            #.startswith('mMálaga')
            #if a.startswith('Home Stadium'):
            #    print(a)

    def __repr__(self):
        return '<Team %r>' % self.name

    def asdict(self):
        result = OrderedDict()
        for key in self.__mapper__.c.keys():
            if getattr(self, key) is not None:
                result[key] = str(getattr(self, key))
            else:
                result[key] = getattr(self, key)
        return result

#############################

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