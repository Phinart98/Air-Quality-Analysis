APP_CONFIG = {
    "api_endpoints": {
        "stations": "https://api.energyandcleanair.org/stations",
        "countries": "https://r2.datahub.io/clvyjaryy0000la0cxieg4o8o/main/raw/data/countries.geojson"
    },
    "countries_of_interest": {
        'US': 'USA',   # United States
        'GB': 'GBR',   # United Kingdom
        'DE': 'DEU',   # Germany
        'FR': 'FRA',   # France
        'IT': 'ITA',   # Italy
        'ES': 'ESP',   # Spain
        'JP': 'JPN',   # Japan
        'KR': 'KOR',   # South Korea
        'CN': 'CHN',   # China
        'IN': 'IND',   # India
        'BR': 'BRA',   # Brazil
        'AU': 'AUS',   # Australia
        'CA': 'CAN',   # Canada
        'TR': 'TUR',   # Turkey
        'TH': 'THA',   # Thailand
        'PH': 'PHL',   # Philippines
        'MY': 'MYS',   # Malaysia
        'SG': 'SGP',   # Singapore
        'ZA': 'ZAF',   # South Africa
        'AE': 'ARE'    # UAE
    },
    "pollutants": ["pm10", "pm25", "no2", "o3", "so2", "co"],
    "map_config": {
        "default_zoom": 3,
        "default_center": [20, 0],
        "style": "mapbox://styles/mapbox/light-v10"
    },
    "time_ranges": {
        "1D": "1 Day",
        "7D": "1 Week",
        "1M": "1 Month",
        "3M": "3 Months",
        "6M": "6 Months",
        "1Y": "1 Year",
        "ALL": "All Time"
    }
}
