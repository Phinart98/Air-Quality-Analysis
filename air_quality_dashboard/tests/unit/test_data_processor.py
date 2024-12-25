import unittest
import pandas as pd
import geopandas as gpd
from src.utils.data_processor import DataProcessor

class TestDataProcessor(unittest.TestCase):
    def setUp(self):
        self.data_processor = DataProcessor()
        
    def test_load_data(self):
        self.data_processor.load_data()
        self.assertIsNotNone(self.data_processor.stations_data)
        self.assertIsNotNone(self.data_processor.countries_data)
        
    def test_calculate_densities(self):
        self.data_processor.load_data()
        self.data_processor.calculate_densities()
        self.assertIsInstance(self.data_processor.density_results, pd.DataFrame)
