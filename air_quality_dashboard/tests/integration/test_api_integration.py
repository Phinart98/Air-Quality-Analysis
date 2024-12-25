import unittest
from src.api.data_fetcher import DataFetcher
from src.api.cache_manager import CacheManager

class TestAPIIntegration(unittest.TestCase):
    def setUp(self):
        self.data_fetcher = DataFetcher()
        self.cache_manager = CacheManager()
        
    def test_data_fetch_and_cache(self):
        data = self.data_fetcher.fetch_data()
        self.assertIsNotNone(data)
        
        self.cache_manager.set('test_data', data)
        cached_data = self.cache_manager.get('test_data')
        self.assertEqual(data, cached_data)
