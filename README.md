
<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3775A9?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.10+"/>
  <img src="https://img.shields.io/badge/GitHub_API-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub API"/>
  <img src="https://img.shields.io/badge/Repository_Optimization-2E8B57?style=for-the-badge" alt="Repo Optimization"/>
  <img src="https://img.shields.io/github/license/ilyarah/Github_SEO_Protocol_MVP?style=for-the-badge&color=2E8B57" alt="MIT License"/>
</p>

<h1 align="center">GitHub SEO Protocol MVP</h1>

<p align="center">
  <strong>A read-only analysis tool designed to evaluate and enhance the discoverability of public GitHub repositories.</strong><br/>
  Built specifically to support open-source developers in the blockchain, Web3, and software engineering communities.
</p>

<br/>

## Overview

The GitHub SEO Protocol MVP provides developers with actionable insights into repository visibility without modifying any repository content.  
It analyzes key performance indicators, computes a visibility score, identifies keyword opportunities, tracks historical trends, and offers concrete recommendations — all through read-only GitHub API access.

### Core Capabilities

| Feature                              | Description                                                                                          | Status |
|--------------------------------------|------------------------------------------------------------------------------------------------------|--------|
| Read-only GitHub API analysis        | Fetches metrics without any write operations                                                         | ✓      |
| Visibility scoring (0–100)           | Weighted evaluation of engagement, activity, contributors, keywords and structural elements         | ✓      |
| Keyword extraction & recommendations | Identifies current keywords and suggests trending terms relevant to blockchain/Web3 domains         | ✓      |
| Historical trend tracking            | Stores metrics over time with SQLite and generates visual trend charts                              | ✓      |
| Google Indexing API integration      | Optional submission of repository URLs to accelerate Google crawling (requires service account)    | ✓      |
| Multiple output formats              | Professional HTML reports, clean Markdown, and JSON for integration purposes                        | ✓      |

## Installation & Quick Start

1. **Clone the repository**

```bash
git clone https://github.com/ilyarah/Github_SEO_Protocol_MVP.git
cd Github_SEO_Protocol_MVP
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Generate a read-only GitHub Personal Access Token**  
   GitHub → Settings → Developer settings → Personal access tokens (classic) → Select only `repo:public_repo` scope

4. **Run the analysis**

```bash
# Basic usage – HTML report recommended for best presentation
python -m seo_protocol \
  --repo <your-username>/<your-repo> \
  --token ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx \
  --output html

# With Google Indexing support (optional)
python -m seo_protocol \
  --repo <your-username>/<your-repo> \
  --token ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx \
  --google-json /path/to/service-account.json \
  --output html \
  --history-days 180
```

Output files are created in the current directory (e.g. `seo_report_<username>_<repo>.html`).

## Visibility Scoring Methodology

The visibility score (0–100) is calculated using the following weighted components:

- **30%** — Engagement (stars + forks + watchers)
- **25%** — Recent activity (commits + issues + views + clones over last 14 days)
- **20%** — Number of contributors
- **20%** — Keyword density and relevance
- **5%**  — Structural completeness (presence of README and LICENSE)

This balanced formula rewards genuine community traction while highlighting opportunities for improvement.

## Target Audience

- Blockchain and Web3 developers seeking greater visibility for open-source tools and protocols
- Individual maintainers aiming to increase repository discoverability
- Teams and contributors who value data-driven optimization of public-facing projects

## Current Status & Roadmap

**Current Version:** 0.1.0 MVP (January 2026)

**Planned Features (2026):**

- Batch analysis for multiple repositories
- Scheduled execution via GitHub Actions
- Enhanced keyword trend sourcing
- CSV export and basic dashboard visualization
- Optional integration with local LLM models for suggestion refinement

## License

This project is licensed under the **MIT License**.

## Acknowledgments

Developed with the goal of helping high-quality open-source projects reach the audiences they deserve.

Contributions, feedback, and issue reports are warmly welcomed.

---

**Repository maintained by** [@ilyarah](https://github.com/ilyarah)
