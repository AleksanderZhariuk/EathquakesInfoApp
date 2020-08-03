#   Earthquake app

#   OUTPUT VIEW: {PLACE}: {direction}, {COUNTRY}, {MAGNITUDE}: {VALUE}


import requests
import time
import sqlite3
from earthquake import Earthquake
from termcolor import colored


user_starttime = input('Введи старт временного промежутка: ')
user_endtime = input('Введи конец временного промежутка: ')
name = [input('Введите страну: ').lower().capitalize()]
connection = sqlite3.connect('countries_db.db')
cursor = connection.cursor()
# cursor.execute('CREATE TABLE Countries (CountryName TEXT, Latitude FLOAT, Longitude FLOAT)')
cursor.execute('SELECT CountryName from Countries WHERE CountryName = ?', name)
countries_name = cursor.fetchall()
if len(countries_name) == 0:
    print('Такой страны не найдено, она будет добавлена в базу. Введите пожалуйста данные.')
    name_of_country = name[0]
    user_latitude = float(input('Введите широту: '))
    user_longitude = float(input('Введите долготу: '))
    info_about_country = (name_of_country, user_latitude, user_longitude)
    cursor.execute('INSERT INTO Countries VALUES(?, ?, ?)', info_about_country)
else:
    cursor.execute('SELECT CountryName, Latitude, Longitude from Countries WHERE CountryName = ?', name)
    info_about_country = cursor.fetchall()
    user_latitude = info_about_country[0][1]
    user_longitude = info_about_country[0][2]
connection.commit()
connection.close()
user_maxradiuskm = input('Введи максимальный радиус (в км): ')
user_minmagnitude = input('Введи минимальную магнитуду: ')

url = 'https://earthquake.usgs.gov/fdsnws/event/1/query?'
response = requests.get(url, headers={'Accept': 'application/json'}, params={
    'format': 'geojson',
    'starttime': user_starttime,
    'endtime': user_endtime,
    'latitude': user_latitude,
    'longitude': user_longitude,
    'maxradiuskm': user_maxradiuskm,
    'minmagnitude': user_minmagnitude,
})

data = response.json()
count = 0
range_value = data['metadata']['count']
lst_of_earthquakes = []
for _ in range(range_value):
    place = data['features'][count]['properties']['place']
    date = data['features'][count]['properties']['time']
    magnitude = data['features'][count]['properties']['mag']
    earthquake = Earthquake(place, date, magnitude)
    lst_of_earthquakes.append(earthquake)
    count += 1

answer = input('Отсортировать по магнитуде или по времени? [M/T] ').lower()
if answer == 'm':
    lst_of_earthquakes.sort(key=lambda x: x.magnitude, reverse=True)
elif answer == 't':
    lst_of_earthquakes.sort(key=lambda x: x.date, reverse=True)

count = 1
place = colored(' место: ', 'green', attrs=['bold'])
date = colored('Дата: ', 'cyan', attrs=['bold'])
magnitude = colored('Магнитуда: ', 'yellow', attrs=['bold'])
for obj in lst_of_earthquakes:
    colored_count = colored(str(count), 'green', attrs=['bold'])
    print(colored_count + place + obj.place + ' | ' + date + time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(
        obj.date / 1000)) + ' | ' + magnitude + str(obj.magnitude))
    count += 1

# ------------------------------------Для корректного вывода в консоле cmd---------------------------------------------
# for obj in lst_of_earthquakes:
#     print(f'{count}' + ' место: ' + obj.place + ' | Дата: ' + time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(
#         obj.date / 1000)) + ' | Магнитуда: ' + str(obj.magnitude))
#     count += 1
