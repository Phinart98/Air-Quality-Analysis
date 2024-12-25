import requests

class DataFetcher:
    def __init__(self):
        self.stations_url = "https://api.energyandcleanair.org/stations?country=GB,US,TR,PH,IN,TH&format=geojson"
        self.countries_url = "https://r2.datahub.io/clvyjaryy0000la0cxieg4o8o/main/raw/data/countries.geojson"

    def fetch_data(self):
        stations = requests.get(self.stations_url).json()
        countries = requests.get(self.countries_url).json()
        return stations, countries
