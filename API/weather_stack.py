import requests
API_KEY_2 = "0d469164e7b1b6a7bfdecd4144e44001"
url = f"https://api.weatherstack.com/current?access_key={API_KEY_2}"

querystring = {"query":"New Delhi"}

response = requests.get(url, params=querystring)

print(response.json())