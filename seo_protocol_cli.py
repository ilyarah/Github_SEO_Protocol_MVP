
import argparse
import logging
from seo_protocol import SEOProtocol

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_arguments():
    parser = argparse.ArgumentParser(description="GitHub SEO Protocol MVP")
    parser.add_argument("--repo", required=True, help="Repo name (username/repo)")
    parser.add_argument("--gh-token", required=True, help="GitHub token (read-only)")
    parser.add_argument("--google-json", default=None, help="Google service account JSON (optional)")
    parser.add_argument("--output", default="md", choices=["md", "json", "html"], help="Report format")
    parser.add_argument("--history-days", type=int, default=30, help="Days of historical data to analyze")
    parser.add_argument("--min-score", type=float, default=50.0, help="Min visibility score for alerts")
    return parser.parse_args()

def main():
    args = parse_arguments()
    try:
        protocol = SEOProtocol(args.repo, args.gh_token, args.google_json)
        protocol.run_pipeline(args.output, args.history_days, args.min_score)
    except Exception as e:
        logging.error(f"Critical error: {e}")
        print("Protocol failed - check logs.")

if __name__ == "__main__":
    main()
    