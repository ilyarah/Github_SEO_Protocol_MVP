
# SEO Protocol MVP - Usage

## Setup Instructions

1. **Clone the repository**:

   ```bash
   git clone https://github.com/username/repo.git
   cd seo-protocol-mvp
````

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Create `config.json`**:

   Add your **GitHub token** in the `config.json` file:

   ```json
   {
       "github_token": "YOUR_ACTUAL_GITHUB_TOKEN"
   }
   ```

4. **Optional: Google Indexing API (for URL submission)**

   * Set up a **Google Service Account** for the Google Indexing API.
   * Save the JSON credentials file and provide its path in the code if you want to use the Indexing API.

## Running the CLI

Use the following command to generate a report:

```bash
python seo_protocol_cli.py --repo "username/repo" --gh-token "YOUR_ACTUAL_GITHUB_TOKEN" --output html --history-days 30 --min-score 50
```

### Parameters:

* `--repo`: GitHub repository name (e.g., `octocat/Hello-World`)
* `--gh-token`: GitHub personal access token (read-only)
* `--output`: Report format (`html`, `json`, or `md`)
* `--history-days`: Number of historical days to analyze (default: 30)
* `--min-score`: Minimum visibility score threshold for alerts (default: 50)

## Example Output

The program generates a report with:

* SEO visibility score (out of 100)
* Repository metrics (stars, forks, contributors, etc.)
* Keywords extracted from the repository description and topics
* Suggested improvements to increase visibility

## Contributing

Fork the repository, make changes, and submit a pull request.

## License

MIT License 