import requests


API_KEY = '3fd909629968761c4f36f936ba57ef90'
city = 'Ankleshwar'
url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'

response = requests.get(url)
data = response.json()

if response.status_code == 200:
    print(f"Temperature in {city}: {data['main']['temp']}°C")
else:
    print(f"Error: {data['message']}")

# url = "https://api.openweathermap.org/data/3.0/onecall?lat={21.626425}&lon={73.015198}appid={3fd909629968761c4f36f936ba57ef90}"

# Call current weather data
# for lattitude and longitude of any location -> latlong.net

# url = "https://api.openweathermap.org/data/2.5/weather?lat={21.626425}&lon={73.015198}&appid={3fd909629968761c4f36f936ba57ef90}"


# Units of measurement

# Example : Temperature is available in Fahrenheit, Celsius and Kelvin units.

# For temperature in Fahrenheit use units=imperial
# For temperature in Celsius use units=metric
# Temperature in Kelvin is used by default, no need to use units parameter in API call

# more details about units -> https://openweathermap.org/weather-data

# standard api_call
# url = "https://api.openweathermap.org/data/2.5/weather?lat=57&lon=-2.15&appid={API key}"

# metric api_call
# url = "https://api.openweathermap.org/data/2.5/weather?lat=57&lon=-2.15&appid={API key}&units=metric"

# imperial api_call
# url = "https://api.openweathermap.org/data/2.5/weather?lat=57&lon=-2.15&appid={API key}&units=imperial"

# Multilingual support
# url = "https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API key}&lang={lang}
# can use 'hi' for hindi


# headers = {
#     'Authorization': 'Bearer YOUR_ACCESS_TOKEN',
#     'Content-Type': 'application/json'
# }

# params = {'key1': 'value1', 'key2': 'value2'}

# try:
#     response = requests.get(url, headers=headers, params=params, timeout=10)
#     response.raise_for_status()
#     data = response.json()
#     print(data)
# except requests.exceptions.RequestException as e:
    # print(f"An error occurred: {e}")
