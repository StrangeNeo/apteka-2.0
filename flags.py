import sys
from PIL import Image
import requests
from io import BytesIO


here = sys.argv[1:]


def apt(coords):
    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
    coords = ','.join(coords)
    search_params = {
        "apikey": api_key,
        "text": "аптека",
        "lang": "ru_RU",
        "ll": coords,
        'results': '2',
    }
    response = requests.get(search_api_server, params=search_params)
    if not response:
        pass
    else:
        apteka = response.json()['features'][0]
        coordinaty = apteka['geometry']['coordinates']
        name = apteka['properties']['CompanyMetaData']['name']
        adress = apteka['properties']['CompanyMetaData']['address']
        timee = apteka['properties']['CompanyMetaData']['Hours']['text']
        map_params = {
            "l": "map",
            "pt": f"{coords},pm2rdl~{coordinaty[0]},{coordinaty[1]},pm2bll"
        }
        map_api_server = "http://static-maps.yandex.ru/1.x/"

        response = requests.get(map_api_server, params=map_params)

        Image.open(BytesIO(response.content)).show()

        print(f'''{name}
{adress}
{timee}''')

        coords = coords.split(',')
        l_x = abs(float(coords[0]) - coordinaty[0]) * 111300
        l_y = abs(float(coords[1]) - coordinaty[1]) * 111000
        xy = (l_x ** 2 + l_y ** 2) ** 0.5
        print(f'расстояние по прямой = {round(xy)} метров')


apt(here)
