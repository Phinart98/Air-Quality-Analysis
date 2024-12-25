import json
import os
from datetime import datetime, timedelta

class CacheManager:
    def __init__(self, cache_dir='cache', expiry_hours=24):
        self.cache_dir = cache_dir
        self.expiry_hours = expiry_hours
        os.makedirs(cache_dir, exist_ok=True)
    
    def get_cache_path(self, key):
        return os.path.join(self.cache_dir, f"{key}.json")
    
    def get(self, key):
        cache_path = self.get_cache_path(key)
        if os.path.exists(cache_path):
            with open(cache_path, 'r') as f:
                cached_data = json.load(f)
                cached_time = datetime.fromisoformat(cached_data['timestamp'])
                if datetime.now() - cached_time < timedelta(hours=self.expiry_hours):
                    return cached_data['data']
        return None
    
    def set(self, key, data):
        cache_path = self.get_cache_path(key)
        cache_data = {
            'timestamp': datetime.now().isoformat(),
            'data': data
        }
        with open(cache_path, 'w') as f:
            json.dump(cache_data, f)
