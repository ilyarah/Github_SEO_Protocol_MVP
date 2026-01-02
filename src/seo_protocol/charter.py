# src/seo_protocol/charter.py
import logging
import matplotlib.pyplot as plt
import base64
from io import BytesIO

logger = logging.getLogger(__name__)

class Charter:
    """Simple chart generator that returns base64 encoded PNG images."""

    def generate_stars_trend_chart(self, historical_data: list[dict]) -> str | None:
        """
        Generate simple line chart of stars over time.
        Returns base64 encoded PNG or None if data is insufficient.
        """
        if len(historical_data) < 2:
            logger.info("Not enough historical data for chart")
            return None

        try:
            dates = [d['date'] for d in historical_data]
            stars = [d['stars'] for d in historical_data]

            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(dates, stars, marker='o', linestyle='-', color='#1f77b4')
            ax.set_title('Stars Growth Over Time')
            ax.set_xlabel('Date')
            ax.set_ylabel('Stars')
            ax.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            plt.tight_layout()

            buf = BytesIO()
            fig.savefig(buf, format='png', dpi=100)
            buf.seek(0)
            plt.close(fig)

            return base64.b64encode(buf.read()).decode('utf-8')

        except Exception as e:
            logger.error(f"Chart generation failed: {e}")
            return None
