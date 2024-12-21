# import required modules
import requests, json
import ollama

def get_weather(location):
    api_key = "YOUR_API_KEY"

    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    complete_url = base_url + "appid=" + api_key + "&q="  + location
    response = requests.get(complete_url)
    weather_data = response.json()

    return weather_data

x=get_weather(input(">>>"))
stream = ollama.generate(model='llama3.2',
                         prompt=f'You are a Weather Expert now analyse this data and explain the weather! crisp clear and concise! not more than 100 words \n DATA= {x}'
                         ,stream=True)
# Now x contains list of nested dictionaries
for chunk in stream:
    print(chunk['response'], flush=True, end="")
print()
# print(f"Response: \n {response} \n")
# Check the value of "cod" key is equal to
# "404", means city is not found otherwise,
# city is not found
if x["cod"] != "404":
    # print(x)
    # store the value of "main"
    # key in variable y
    y = x["main"]

    # store the value corresponding
    # to the "temp" key of y
    current_temperature = int(y["temp"]) - 273.15
    feels_like = int(y['feels_like']) - 273.15
    # store the value corresponding
    # to the "pressure" key of y
    current_pressure = y["pressure"]

    # store the value corresponding
    # to the "humidity" key of y
    current_humidity = y["humidity"]

    # store the value of "weather"
    # key in variable z
    z = x["weather"]

    # store the value corresponding
    # to the "description" key at
    # the 0th index of z
    weather_description = z[0]["description"]

    # print following values
    print(" Temperature (in kelvin unit) = " +
          str(current_temperature) +
          "\n\n atmospheric pressure (in hPa unit) = " +
          str(current_pressure) +
          "\n\n humidity (in percentage) = " +
          str(current_humidity) +
          "\n\n description = " +
          str(weather_description))
else:
    print("City Not Found ")
