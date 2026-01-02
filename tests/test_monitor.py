# tests/test_monitor.py
import unittest
import sqlite3
from datetime import datetime, timedelta
from src.seo_protocol.monitor import Monitor

class TestMonitor(unittest.TestCase):

    def test_save_current_metrics(self):
        monitor = Monitor(db_path="test_seo_monitor.db")

        # Test data
        metrics = {
            'stars': 50,
            'forks': 10,
            'score': 70.5
        }

        # Save metrics
        monitor.save_current_metrics("username/repo", metrics, 70.5)

        # Verify by querying the database directly
        conn = sqlite3.connect("test_seo_monitor.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM metrics WHERE repo = 'username/repo'")
        data = cursor.fetchone()
        conn.close()

        self.assertIsNotNone(data)
        self.assertEqual(data[0], "username/repo")

    def test_get_historical_data(self):
        monitor = Monitor(db_path="test_seo_monitor.db")
        
        # Mock data (using the `save_current_metrics` method)
        metrics = {
            'stars': 50,
            'forks': 10,
            'score': 70.5
        }
        monitor.save_current_metrics("username/repo", metrics, 70.5)
        
        # Retrieve historical data
        historical_data = monitor.get_historical_data("username/repo", days_back=30)

        self.assertGreater(len(historical_data), 0)

if __name__ == '__main__':
    unittest.main()
