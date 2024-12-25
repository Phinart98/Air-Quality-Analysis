import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor

class DataAggregator:
    def __init__(self, api_endpoints):
        self.api_endpoints = api_endpoints
        self.cache_manager = None
        self.rate_limiter = None
    
    def fetch_from_endpoint(self, endpoint):
        if self.rate_limiter and not self.rate_limiter.can_make_request():
            self.rate_limiter.wait_for_next_window()
        
        response = requests.get(endpoint)
        return response.json()
    
    def aggregate_data(self, max_workers=5):
        aggregated_data = []
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_endpoint = {
                executor.submit(self.fetch_from_endpoint, endpoint): endpoint
                for endpoint in self.api_endpoints
            }
            
            for future in future_to_endpoint:
                try:
                    data = future.result()
                    aggregated_data.append(data)
                except Exception as e:
                    endpoint = future_to_endpoint[future]
                    print(f"Error fetching from {endpoint}: {str(e)}")
        
        return pd.concat([pd.DataFrame(data) for data in aggregated_data])
