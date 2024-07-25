import os
import requests

city_name = input('Choose your city: ').title()

url = "https://nominatim.openstreetmap.org/search"
params = {
    'q': city_name,
    'format': 'json',
    'limit': 1
}

headers = {
    'User-Agent': 'geoAPP/1.0 (your_email@example.com)'
}

try:
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    data = response.json()

    if data:
        location = data[0]  # Take the first result
        latitude = location.get('lat')
        longitude = location.get('lon')

        print("Address:", location.get('display_name'))
        print("Latitude:", latitude)
        print("Longitude:", longitude)

        api_key = os.getenv('WEATHER_API_KEY')
        if not api_key:
            print("API key is missing. Please set the WEATHER_API_KEY environment variable.")
            exit()

        weather_url = f'https://api.weatherbit.io/v2.0/current?lat={latitude}&lon={longitude}&key={api_key}'

        try:
            weather_response = requests.get(weather_url)
            weather_response.raise_for_status()
            weather_data = weather_response.json()

            data = weather_data['data'][0]
            description = data['weather']['description']
            datetime = data['datetime']
            sunrise = data['sunrise']
            sunset = data['sunset']

            print("Weather description:", description)
            print("Datetime:", datetime)
            print("Sunrise:", sunrise)
            print("Sunset:", sunset)

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as err:
            print(f"Error occurred: {err}")

    else:
        print("City not found.")

except requests.RequestException as e:
    print(f"Error: {e}")
