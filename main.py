#   Earthquake app

#   OUTPUT VIEW: {PLACE}: {direction}, {COUNTRY}, {MAGNITUDE}: {VALUE}


import requests

user_starttime = input('Введи старт временного промежутка: ')
user_endtime = input('Введи конец временного промежутка: ')
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

for place in range(data['metadata']['count']):
    magnitude_value = str(data['features'][count]['properties']['mag'])
    print(str(count + 1) + '.' + 'Место: ' + data['features'][count]['properties']['place'] + '.' + ' Магнитуда: ' +
          magnitude_value + '.')
    count += 1


test_variable = 1
