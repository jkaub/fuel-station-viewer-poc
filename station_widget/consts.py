import os

URL = f'https://donnees.roulez-eco.fr/opendata/instantane'
CITY_PATH = 'data/cities_coordinates.csv'

INIT_POST_CODE = '75001'
INIT_FUEL = 'SP98'
INIT_DIST = 3

R = 6371

TOKEN = os.environ["MAPBOX_TOKEN"]