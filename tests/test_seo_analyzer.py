# tests/test_seo_analyzer.py
import unittest
from unittest.mock import MagicMock
from src.seo_protocol.seo_analyzer import SEOAnalyzer

class TestSEOAnalyzer(unittest.TestCase):

    def test_compute_visibility_score(self):
        # Test data
        metrics = {
            'stars': 100,
            'forks': 50,
            'watchers': 30,
            'commits': 200,
            'issues': 15,
            'views_last_14d': 1200,
            'clones_last_14d': 1000,
            'contributors': 5,
            'has_readme': True,
            'has_license': True
        }
        keywords = ['blockchain', 'ethereum', 'solidity']

        analyzer = SEOAnalyzer('dummy_token', 'username/repo')
        score = analyzer.compute_visibility_score(metrics, keywords)

        # Check if the score is calculated correctly
        self.assertEqual(score, 71.2)

    def test_analyze(self):
        # Mock the GitHubAPI object
        mock_api = MagicMock()
        mock_api.fetch_metrics.return_value = {
            'stars': 100,
            'forks': 50,
            'watchers': 30,
            'commits': 200,
            'issues': 15,
            'views_last_14d': 1200,
            'clones_last_14d': 1000,
            'contributors': 5,
            'has_readme': True,
            'has_license': True
        }
        mock_api.extract_keywords.return_value = (['blockchain', 'ethereum', 'solidity'], {'defi'})

        analyzer = SEOAnalyzer('dummy_token', 'username/repo')
        result = analyzer.analyze()

        self.assertIn('metrics', result)
        self.assertIn('score', result)
        self.assertIn('keywords', result)
        self.assertIn('suggested_keywords', result)

if __name__ == '__main__':
    unittest.main()
