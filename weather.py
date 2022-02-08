import argparse
import json
import sys
from configparser import ConfigParser
from urllib import parse, request
from pprint import pp


BASE_WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"

def _get_api_key():
    config = ConfigParser()
    config.read("secrets.ini")
    return config["openweather"]["api_key"]

def read_user_cli_args():
    parser = argparse.ArgumentParser(
        description="gets weather and temperature information for a city"
    )

    parser.add_argument(
        "city", nargs="+", type=str, help="enter the city name"
    )
    parser.add_argument(
        "-i",
        "--imperial",
        action="store_true",
        help="display the temperature in imperial units",
    )
    return parser.parse_args()

def build_weather_query(city_input, imperial=False):
    api_key = _get_api_key()
    city_name = " ".join(city_input)
    url_encoded_city_name = parse.quote_plus(city_name)
    units = "imperial" if imperial else "metric"
    url = (
        f"{BASE_WEATHER_API_URL}?q={url_encoded_city_name}"
        f"&units={units}&appid={api_key}"
    )
    return url

def get_weather_data(query_url):
    try:
        response = request.urlopen(query_url)
    except error.HTTPError as http_error:
        if http_error.code == 401:  # 401 - Unauthorized
            sys.exit("Access denied. Check your API key.")
        elif http_error.code == 404:  # 404 - Not Found
            sys.exit("Can't find weather data for this city.")
        else:
            sys.exit(f"Something went wrong... ({http_error.code})")
    data = response.read()
    return json.loads(data)

def display_weather_info(weather_data, imperial=False):
    city = weather_data["name"]
    weather_description = weather_data["weather"][0]["description"]
    temperature = weather_data["main"]["temp"]

    print(f"{city}", end=" ")
    print(f"\t{weather_description.capitalize()}", end=" ")
    print(f"({temperature}°{'F' if imperial else 'C'})")


if __name__ == "__main__":
    user_args = read_user_cli_args()
    #print(user_args.city, user_args.imperial)
    query_url = build_weather_query(user_args.city, user_args.imperial)
    #print(query_url)
    weather_data = get_weather_data(query_url)
    #pp(weather_data)
    #print(
     # f"{weather_data['name']}: "
     # f"{weather_data['weather'][0]['description']} "
     # f"({weather_data['main']['temp']})"
     # )
    display_weather_info(weather_data, user_args.imperial)