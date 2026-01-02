# tests/test_charter.py
import unittest
from src.seo_protocol.charter import Charter

class TestCharter(unittest.TestCase):

    def test_generate_stars_trend_chart(self):
        charter = Charter()
        
        # Mock historical data
        historical_data = [
            {"date": "2025-01-01", "stars": 100, "forks": 20, "score": 70},
            {"date": "2025-02-01", "stars": 120, "forks": 25, "score": 75},
            {"date": "2025-03-01", "stars": 150, "forks": 30, "score": 80}
        ]
        
        # Test chart generation
        chart_base64 = charter.generate_stars_trend_chart(historical_data)
        
        self.assertIsNotNone(chart_base64)

if __name__ == '__main__':
    unittest.main()
