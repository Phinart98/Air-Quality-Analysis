import unittest
import pandas as pd
from src.analytics.statistical_analysis import StatisticalAnalyzer
from src.analytics.trend_detection import TrendDetector

class TestAnalytics(unittest.TestCase):
    def setUp(self):
        self.sample_data = pd.DataFrame({
            'pm10': [10, 20, 30, 40, 50]
        })
        
    def test_statistical_analyzer(self):
        analyzer = StatisticalAnalyzer(self.sample_data)
        stats = analyzer.compute_basic_stats('pm10')
        self.assertEqual(stats['mean'], 30)
        
    def test_trend_detector(self):
        detector = TrendDetector()
        trend = detector.calculate_moving_average(self.sample_data['pm10'])
        self.assertIsInstance(trend, pd.Series)
