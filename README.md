# Investigate Malicious URLs

This project provides a multi-stage pipeline for investigating potentially malicious URLs. It automates the process of:

1. **Checking domain reputation with VirusTotal** – Quickly screen a list of target URLs for known threats using the VirusTotal API.
2. **Browsing and downloading site code with Playwright** – Visit each site in a headless browser, saving all HTML and JavaScript resources for offline analysis.
3. **Analysing downloaded code with an LLM** – Use OpenAI's language models to review the captured JavaScript for signs of compromise, obfuscation, or malicious behaviour.

The result is a set of detailed, human-readable reports for each domain, helping you identify threats and suspicious activity at scale.

## Features
- Bulk domain reputation checks via VirusTotal
- Automated site crawling and resource capture using Playwright
- LLM-powered static analysis of JavaScript for malware, phishing, and other threats
- All configuration via simple text files and environment variables
- Output as clear markdown reports, suitable for further review or sharing

## Setup

1. **Clone the repository**

```bash
git clone https://github.com/ciaran-finnegan/investigate_malicious_urls.git
cd investigate_malicious_urls
```

2. **Create and activate a virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Install Playwright browsers** (required for `fetch_resources.py`):

```bash
python -m playwright install
```

5. **Add your API keys**

Create a file called `.env` in the project directory with the following content:

```
VT_API_KEY=your_actual_virustotal_api_key_here
OPENAI_API_KEY=your_actual_openai_api_key_here
```

**Do NOT commit your `.env` file or API keys to version control.**

## Usage

### 1. Prepare your target URLs

Edit `target_urls.txt` to list the URLs you want to investigate (one per line).

### 2. VirusTotal Domain Lookup

Run the script:

```bash
python vt_url_lookup.py
```

This will check each domain's reputation and print a summary.

### 3. Fetch Site Resources

This script fetches HTML and JavaScript from each site and saves them to the `output/` directory:

```bash
python fetch_resources.py
```

### 4. Analyse JavaScript with OpenAI

This script analyses all downloaded JavaScript files and writes detailed reports to `reports/`:

```bash
python analyse_code.py
```

## Example Output

```
thecrystalcouncil.com      ✅ Clean  (engines: 0⛔  0⚠️  85✅)
github.com                 🚫 MALICIOUS  (engines: 2⛔  0⚠️  83✅)
```

Each report in `reports/` will contain a breakdown of findings for every JavaScript file captured from the site.

## Notes
- Requires Python 3.7 or newer.
- The script will exit with an error if the API key is missing.
- Add `venv/`, `.env`, `output/`, and `reports/` to your `.gitignore`.
- Playwright browsers must be installed once per environment with `python -m playwright install`.

## License
MIT
