# src/seo_protocol/seo_booster.py
import logging
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials

logger = logging.getLogger(__name__)

class SEOBooster:
    """Generates improvement suggestions and handles optional Google Indexing API calls."""

    def __init__(self, repo_url: str, google_service_json: str | None = None):
        self.repo_url = repo_url
        self.google_service_json = google_service_json

    def get_improvement_suggestions(self,
                                    keywords: list[str],
                                    suggested: list[str],
                                    score: float,
                                    alert_threshold: float = 50.0) -> list[str]:
        """
        Generate actionable improvement suggestions.
        Returns list of strings (each is one suggestion/recommendation).
        """
        suggestions = []

        # Formatting the suggestion for social share
        if keywords:
            top_tags = " #".join(keywords[:5])
            suggestions.append(f"X Post: 'Explore my blockchain project → {self.repo_url} #{top_tags}'")
            suggestions.append(f"Blog/article idea: 'Deep dive into {keywords[0]} – my open-source approach'")

        # Suggestions for improving README and project visibility
        suggestions.extend([
            "Make README more discoverable: clear H1/H2 headers + code examples + badges",
            "Consider structured data hints in README for better AI/LLM crawling",
            "Build backlinks: contribute to related projects and mention your repo in PRs"
        ])

        # If the score is low, add alerts and suggestions
        if score < alert_threshold:
            suggestions.append(f"**ALERT** Visibility score {score:.1f} < {alert_threshold}")
            if suggested:
                suggestions.append(f"→ Consider adding trending keywords: {', '.join(suggested[:4])}")

        return suggestions

    def try_submit_urls_to_google(self, urls: list[str] | None = None) -> None:
        """Try to notify Google about updated/important URLs (optional feature)."""
        if not self.google_service_json:
            logger.info("No Google service account provided → skipping Indexing API submission")
            return

        urls = urls or [self.repo_url, f"{self.repo_url}/blob/main/README.md"]

        try:
            credentials = ServiceAccountCredentials.from_json_keyfile_name(
                self.google_service_json,
                scopes=["https://www.googleapis.com/auth/indexing"]
            )
            service = build("indexing", "v3", credentials=credentials)

            for url in urls:
                response = service.urlNotifications().publish(
                    body={"url": url, "type": "URL_UPDATED"}
                ).execute()
                logger.info(f"Indexing request sent for {url}: {response}")

        except HttpError as e:
            logger.warning(f"Google Indexing API error: {e}")
        except Exception as e:
            logger.error(f"Failed to submit to Google Indexing API: {e}")
