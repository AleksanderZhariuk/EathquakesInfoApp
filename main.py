#   Earthquake app

#   OUTPUT VIEW: {PLACE}: {direction}, {COUNTRY}, {MAGNITUDE}: {VALUE}


import requests
import time
from earthquake import Earthquake
from termcolor import colored

dict_dick = {
    'russia': [52.4000000, 54.9833300],
    'usa': [39.000000, -80.500000],
    'netherlands': [52.3740300, 4.8896900],
    'japan': [35.6895000, 139.6917100],
}

user_starttime = input('Введи старт временного промежутка: ')
user_endtime = input('Введи конец временного промежутка: ')
user_country = input('Введи страну: ').lower()

if user_country in dict_dick.keys():
    user_latitude = dict_dick[user_country][0]
    user_longitude = dict_dick[user_country][1]
else:
    print('Страна не найдена')
    user_latitude = input('Введи широту (в десятичных градусах): ')
    user_longitude = input('Введи долготу(в десятичных градусах): ')

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

answer = input('Отсортировать по магнитуде или по времени? [m/t] ').lower()
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
