# tests/test_github_api.py
import unittest
from unittest.mock import patch, MagicMock
from src.seo_protocol.github_api import GitHubAPI
import json
import os

class TestGitHubAPI(unittest.TestCase):

    def setUp(self):
        """Set up the test environment by loading the GitHub token from config.json"""
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
        try:
            with open(config_path, 'r') as config_file:
                config = json.load(config_file)
            self.github_token = config.get("github_token")
            if not self.github_token:
                raise ValueError("GitHub token not found in config.json")
        except Exception as e:
            raise FileNotFoundError(f"Could not load config.json: {e}")

    @patch('src.seo_protocol.github_api.Github')
    def test_fetch_metrics(self, MockGithub):
        """Test fetching the metrics (stars, forks, etc.) for the repository."""
        # Mocking the GitHub repo object
        mock_repo = MagicMock()
        mock_repo.stargazers_count = 100
        mock_repo.forks_count = 20
        mock_repo.watchers_count = 50
        mock_repo.get_contributors.return_value = ['user1', 'user2', 'user3']
        mock_repo.get_commits.return_value.totalCount = 300
        mock_repo.open_issues_count = 5
        mock_repo.get_views.return_value.total_count = 1500
        mock_repo.get_clones.return_value.total_count = 1200
        mock_repo.description = "Blockchain project"
        mock_repo.get_topics.return_value = ["blockchain", "ethereum"]

        MockGithub.return_value.get_repo.return_value = mock_repo

        # Initialize GitHubAPI with the token
        api = GitHubAPI(self.github_token, 'username/repo')
        metrics = api.fetch_metrics()

        # Check if the metrics match the mock data
        self.assertEqual(metrics['stars'], 100)
        self.assertEqual(metrics['forks'], 20)
        self.assertEqual(metrics['watchers'], 50)
        self.assertEqual(metrics['contributors'], 3)
        self.assertEqual(metrics['commits'], 300)
        self.assertEqual(metrics['issues'], 5)
        self.assertEqual(metrics['views_last_14d'], 1500)
        self.assertEqual(metrics['clones_last_14d'], 1200)
        self.assertTrue(metrics['has_readme'])
        self.assertTrue(metrics['has_license'])

    @patch('src.seo_protocol.github_api.Github')
    def test_extract_keywords(self, MockGithub):
        """Test extracting keywords from the repository description and topics."""
        mock_repo = MagicMock()
        mock_repo.description = "This is a Solidity smart contract project"
        mock_repo.get_topics.return_value = ["solidity", "ethereum", "nft"]

        MockGithub.return_value.get_repo.return_value = mock_repo

        # Initialize GitHubAPI with the token
        api = GitHubAPI(self.github_token, 'username/repo')
        keywords, suggested = api.extract_keywords()

        # Verify that keywords are extracted correctly
        self.assertIn('solidity', keywords)
        self.assertIn('ethereum', keywords)
        self.assertIn('nft', suggested)

if __name__ == '__main__':
    unittest.main()
