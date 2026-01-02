# src/seo_protocol/seo_report.py
import logging
import jinja2
import json

logger = logging.getLogger(__name__)

class SEOReport:
    """Handles different report formats."""

    def generate(self,
                 data: dict,
                 format_type: str = "md",
                 chart_base64: str | None = None) -> str:
        """
        Generate report in requested format.
        Supported formats: 'md', 'html', 'json'
        """
        try:
            if format_type == "json":
                return json.dumps(data, indent=2)

            elif format_type == "html":
                return self._render_html(data, chart_base64)

            else:  # default → markdown
                return self._render_markdown(data, chart_base64)

        except Exception as e:
            logger.error(f"Report generation failed: {e}")
            return "# Error\nReport generation failed."

    def _render_markdown(self, data: dict, chart_base64: str | None) -> str:
        lines = [
            f"# SEO Report — {data['repo']}",
            "",
            f"## Visibility Score: **{data['score']:.1f}/100**",
            "",
            "## Collected Metrics",
        ]

        for k, v in data['metrics'].items():
            lines.append(f"- **{k.replace('_', ' ').title()}**: {v}")

        lines.extend(["", "## Improvement Suggestions"])
        for suggestion in data['suggestions']:
            lines.append(f"- {suggestion}")

        if chart_base64:
            lines.append("")
            lines.append("## Stars Growth Trend")
            lines.append(f"![Stars Trend](data:image/png;base64,{chart_base64})")

        return "\n".join(lines)

    def _render_html(self, data: dict, chart_base64: str | None) -> str:
        """Render the HTML content with the necessary structure."""
        html_template = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>SEO Report - {{ repo }}</title>
            <style>
                body { font-family: system-ui, sans-serif; max-width: 900px; margin: 2rem auto; line-height: 1.6; }
                h1, h2 { color: #2c3e50; }
                .score { font-size: 2.5rem; font-weight: bold; color: #27ae60; }
                .alert { color: #c0392b; font-weight: bold; }
                ul { padding-left: 1.5rem; }
                img { max-width: 100%; margin: 1.5rem 0; border-radius: 8px; }
            </style>
        </head>
        <body>
            <h1>SEO Report — {{ repo }}</h1>
            <p class="score">{{ "%.1f"|format(score) }}/100</p>

            <h2>Metrics</h2>
            <ul>
            {% for key, value in metrics.items() %}
                <li><strong>{{ key|replace("_", " ")|title }}:</strong> {{ value }}</li>
            {% endfor %}
            </ul>

            <h2>Improvement Suggestions</h2>
            <ul>
            {% for s in suggestions %}
                <li {% if 'ALERT' in s %}class="alert"{% endif %}>{{ s }}</li>
            {% endfor %}
            </ul>

            {% if chart %}
            <h2>Stars Growth Trend</h2>
            <img src="data:image/png;base64,{{ chart }}" alt="Stars growth chart">
            {% endif %}
        </body>
        </html>
        """

        env = jinja2.Environment(loader=jinja2.DictLoader({"report": html_template}))
        template = env.get_template("report")
        return template.render(
            repo=data['repo'],
            score=data['score'],
            metrics=data['metrics'],
            suggestions=data['suggestions'],
            chart=chart_base64
        )
