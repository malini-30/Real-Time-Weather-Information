"""Real-Time Weather Detection  Application"""
# Author: Vayineni Devi malini
# TODO: Flipkart Internship Task
import requests
import os
import csv
from datetime import datetime  # important import to get current date and time


# Centralize configuration to avoid duplicate lines
API_KEY = os.environ.get("OPENWEATHER_API_KEY", "c402f44fda2cf9552949d088fc1b88a9")  # OpenWeather API key here
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather" #URI for weather data measurement


class RealTime:
    """RealTime weather client that fetches and (optionally) stores weather data."""

    def _init_(self, api_key: str = None, weather_url: str = WEATHER_URL, timeout: int = 10):
        self.api_key = api_key or API_KEY
        self.weather_url = weather_url
        self.timeout = timeout

    def weather_data_fetch(self, city: str):
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric",
        }
        try:
            resp = requests.get(self.weather_url, params=params, timeout=self.timeout)
        except Exception as e:
            print("\n Error:", str(e))
            return None

        if resp.status_code == 200:
            return resp.json()
        else:
            print("\n City not found or API error")
        return None
        #  Weather display function here
    def display_weather(self, city: str):
        """Fetch and print human-friendly weather information for city."""
        data = self.fetch_weather_data(city)
        if not data:
            return
        print(f"\nWeather in {city.title()}:")
        print(f" Temperature: {data['main']['temp']}°C")
        print(f" Feels Like: {data['main']['feels_like']}°C")
        print(f" Condition: {data['weather'][0]['description'].capitalize()}")
        print(f" Humidity: {data['main']['humidity']}%")
        print(f" Wind Speed: {data['wind']['speed']} m/s")

    def store_weather(self, city: str, filename: str = "weather_data.csv"):
        """Fetch weather and append a row to filename."""
        data = self.fetch_weather_data(city)
        if not data:
            return

        city_name = data["name"]
        country = data["sys"]["country"]
        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        condition = data["weather"][0]["description"].capitalize()
        wind_speed = data["wind"]["speed"]

        file_exists = os.path.isfile(filename)
        with open(filename, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(
                    [
                        "Timestamp",
                        "City",
                        "Country",
                        "Temperature (°C)",
                        "Feels Like (°C)",
                        "Humidity (%)",
                        "Condition",
                        "Wind Speed (m/s)",
                    ]
                )
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow(
                [timestamp, city_name, country, temperature, feels_like, humidity, condition, wind_speed]
            )
        print(f"\n Weather data for {city_name} stored in {filename}")

def main():
    city = input("Enter City: ")  # Get  name from user city
    obj= RealTime()
    obj.display_weather(city)  # Call the method for display weather information here
    obj.store_weather(city)  # Call the method for storage weather data in csv file

if __name__ == "_main_":
    main()
# Tested with cities: Guntur, sydney, paris, switzerland, chennai