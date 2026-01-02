# src/seo_protocol/seo_analyzer.py
import logging
from .github_api import GitHubAPI

logger = logging.getLogger(__name__)

class SEOAnalyzer:
    """
    Computes visibility score and performs the core analysis.

    Current scoring weights (approximate):
      • 30% — Engagement (stars + forks + watchers)
      • 25% — Recent activity (commits + issues + views + clones)
      • 20% — Contributors count
      • 20% — Keyword presence
      •  5% — Structural bonuses (README + license)
    """

    def __init__(self, token: str, repo_name: str):
        self.api = GitHubAPI(token, repo_name)

    def compute_visibility_score(self, metrics: dict, keywords: list[str]) -> float:
        """Calculate the visibility score based on collected metrics."""
        try:
            engagement = (metrics.get('stars', 0) + metrics.get('forks', 0) + metrics.get('watchers', 0)) / 3.0
            activity = (metrics.get('commits', 0) + metrics.get('issues', 0) +
                        metrics.get('views_last_14d', 0) + metrics.get('clones_last_14d', 0)) / 4.0
            contrib = metrics.get('contributors', 0)
            keyword_score = len(keywords) * 5.0
            bonus = (10 if metrics.get('has_readme', False) else 0) + \
                    (10 if metrics.get('has_license', False) else 0)

            raw_score = (0.30 * engagement +
                         0.25 * activity +
                         0.20 * contrib +
                         0.20 * keyword_score +
                         0.05 * bonus)

            return round(min(100.0, raw_score / 10.0), 2)

        except Exception as e:
            logger.warning(f"Score calculation issue: {e}")
            return 0.0

    def analyze(self) -> dict:
        """Perform complete analysis in one call."""
        metrics = self.api.fetch_metrics()
        keywords, suggested = self.api.extract_keywords()
        score = self.compute_visibility_score(metrics, keywords)

        return {
            "metrics": metrics,
            "score": score,
            "keywords": keywords,
            "suggested_keywords": list(suggested)
        }
