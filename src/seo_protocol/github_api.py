# src/seo_protocol/github_api.py
import logging
from github import Github, GithubException
from retrying import retry
import nltk
from nltk.corpus import stopwords

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

logger = logging.getLogger(__name__)

def is_rate_limit_error(exception):
    """Retry predicate for GitHub rate limit errors"""
    return isinstance(exception, GithubException) and exception.status == 403


class GitHubAPI:
    """
    Handles all read-only interactions with the GitHub API.
    """

    def __init__(self, token: str, repo_name: str):
        """
        Initialize GitHub client and fetch the repository.
        
        Raises ValueError if repository cannot be accessed.
        """
        self.g = Github(token)
        try:
            self.repo = self.g.get_repo(repo_name)
        except GithubException as e:
            logger.error(f"Failed to access repository {repo_name}: {e}")
            raise ValueError(f"Invalid repository or token: {repo_name}")

    @retry(stop_max_attempt_number=3, wait_fixed=2000, retry_on_exception=is_rate_limit_error)
    def fetch_metrics(self) -> dict:
        """Fetch key repository metrics (read-only)."""
        try:
            return {
                'stars': self.repo.stargazers_count,
                'forks': self.repo.forks_count,
                'watchers': self.repo.watchers_count,
                'contributors': len(list(self.repo.get_contributors())),
                'commits': self.repo.get_commits().totalCount,
                'issues': self.repo.open_issues_count,
                'views_last_14d': self.repo.get_views().total_count,
                'clones_last_14d': self.repo.get_clones().total_count,
                'has_readme': bool(self.repo.get_readme() if hasattr(self.repo, 'get_readme') else False),
                'has_license': self.repo.license is not None,
            }
        except GithubException as e:
            logger.warning(f"Could not fetch full metrics: {e}")
            return {}

    def extract_keywords(self) -> tuple[list[str], set[str]]:
        """Extract keywords from description and topics."""
        try:
            description = (self.repo.description or "").lower()
            topics = [t.lower() for t in self.repo.get_topics()]
            text = description + " " + " ".join(topics)

            tokens = nltk.word_tokenize(text)
            stop_words = set(stopwords.words('english'))
            keywords = [w for w in tokens if w.isalnum() and w not in stop_words]

            # Blockchain-relevant trending terms (can be expanded/updated)
            trends = {
                "blockchain", "solidity", "ethereum", "defi", "nft",
                "web3", "smart-contract", "layer2", "zk", "polygon", "solana"
            }
            suggested = trends - set(keywords)

            return keywords, suggested

        except Exception as e:
            logger.error(f"Keyword extraction failed: {e}")
            return [], set()
