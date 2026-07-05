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
list_of_weather1 = []
list_of_weather2 = []
for i in range(weather_params["cnt"]):
    exact_hour = data["list"][i]["dt_txt"].split(" ")[1].split(":")[0]
    list_of_weather1.append(data["list"][i]["weather"][0]["description"])
    if len(str(int(exact_hour)+3))==1:
        list_of_weather2.append(f"{exact_hour}-0{int(exact_hour)+3}")
    else:
        list_of_weather2.append(f"{exact_hour}-{int(exact_hour)+3}")
    if data["list"][i]["weather"][0]["id"] < 700:
        will_rain=True
if will_rain:
    body1='Warning! - WEATHER ALERT: \n'
else:
    body1='WEATHER ALERT: \n'
for i in range(weather_params["cnt"]):
    body1 += f"{str(list_of_weather1[i]).capitalize()}: {list_of_weather2[i]}\n"
client = Client(account_sid, auth_token)
message = client.messages.create(
    from_ = "+12185100579",
    body=body1,
    to='+48572494900'
)
print(message.status)
