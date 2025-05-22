# VirusTotal URL Lookup

Bulk-check a list of domains against VirusTotal reputation data using the public VirusTotal API.

## Features
- Checks multiple domains for malicious, suspicious, or clean status
- Uses the VirusTotal v3 API
- Reads your API key securely from a `.env` file
- Simple, readable output

## Setup

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/virustotal_url_lookup.git
cd virustotal_url_lookup
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

### VirusTotal Domain Lookup

Run the script:

```bash
python vt_url_lookup.py
```

You can edit the `DOMAINS` list in `vt_url_lookup.py` to check different domains.

### Fetch Site Resources

This script fetches HTML and JavaScript from a list of sites and saves them to the `output/` directory:

```bash
python fetch_resources.py
```

### Analyse JavaScript with OpenAI

This script analyses JavaScript files in the `output/` directory and writes reports to `reports/`:

```bash
python analyse_code.py
```

## Example Output

```
thecrystalcouncil.com      ✅ Clean  (engines: 0⛔  0⚠️  85✅)
github.com                 🚫 MALICIOUS  (engines: 2⛔  0⚠️  83✅)
```

## Notes
- Requires Python 3.7 or newer.
- The script will exit with an error if the API key is missing.
- Add `venv/`, `.env`, `output/`, and `reports/` to your `.gitignore`.
- Playwright browsers must be installed once per environment with `python -m playwright install`.

## License
MIT
