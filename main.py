from twilio.rest import Client
import os

account_sid = os.environ.get("ACCOUNT_SID_ENV")
auth_token = os.environ.get("AUTH_TOKEN_ENV")

import requests

api_key = os.environ.get("API_KEY_ENV")
api_url = "https://api.openweathermap.org/data/2.5/forecast"
weather_params={
    "lat": 54.518890,
    "lon": 18.530540, 
    "appid": api_key,
    "cnt": 4,
}

response = requests.get(api_url, params=weather_params)
response.raise_for_status()

data=response.json()
will_rain = False
list_of_weather = []
for i in range(weather_params["cnt"]):
    if data["list"][i]["weather"][0]["id"] < 700:
        list_of_weather.append(data["list"][i]["weather"][0]["main"])
        will_rain=True
if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        from_ = "+12185100579",
        body=f'WEATHER ALERT - {set(list_of_weather)}',
        to='+48572494900'
    )
else:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        from_ = "+12185100579",
        body='NO RAIN TODAY',
        to='+48572494900'
    )
print(message.status)
