import os
import sys

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WEATHERAPI_KEY")
BASE_URL = "https://api.weatherapi.com/v1/current.json"


class Weather:
    """Holds the parsed weather data for one city."""

    def __init__(self, city, country, temp, feels_like,
                 humidity, wind_speed, description):
        self.city = city
        self.country = country
        self.temp = temp
        self.feels_like = feels_like
        self.humidity = humidity
        self.wind_speed = wind_speed
        self.description = description

    @classmethod
    def from_json(cls, data):
        """Build a Weather object from the API's JSON response."""
        return cls(
            city=data["location"]["name"],
            country=data["location"]["country"],
            temp=data["current"]["temp_c"],
            feels_like=data["current"]["feelslike_c"],
            humidity=data["current"]["humidity"],
            wind_speed=data["current"]["wind_kph"],
            description=data["current"]["condition"]["text"],
        )

    def __str__(self):
        line = "=" * 35
        return (
            f"{line}\n"
            f" Weather in {self.city}, {self.country}\n"
            f"{line}\n"
            f" Condition   : {self.description}\n"
            f" Temperature : {self.temp:.1f} °C\n"
            f" Feels like  : {self.feels_like:.1f} °C\n"
            f" Humidity    : {self.humidity}%\n"
            f" Wind speed  : {self.wind_speed} km/h\n"
            f"{line}"
        )


def fetch_weather(city, api_key):
    """Call the API and return the parsed JSON (dict)."""
    params = {"key": api_key, "q": city}
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError:
        if response.status_code == 400:
            print(f"Error: city '{city}' not found.")
        elif response.status_code in (401, 403):
            print("Error: invalid or disabled API key.")
        else:
            print(f"HTTP error: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("Error: no internet connection.")
    except requests.exceptions.Timeout:
        print("Error: the request timed out.")
    except requests.exceptions.RequestException as e:
        print(f"Unexpected error: {e}")
    return None


def main():
    if not API_KEY:
        print("Error: WEATHERAPI_KEY is missing. Check your .env file.")
        sys.exit(1)

    city = input("Enter city name: ").strip()
    if not city:
        print("Error: city name cannot be empty.")
        sys.exit(1)

    data = fetch_weather(city, API_KEY)
    if data is None:
        sys.exit(1)

    weather = Weather.from_json(data)
    print(weather)


if __name__ == "__main__":
    main()