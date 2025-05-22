#!/usr/bin/env python3
"""
Send each saved JS file to OpenAI and write a markdown report per domain.

Creates:
  reports/
    example_com.md
"""

import os, pathlib, textwrap

import tiktoken, openai
from dotenv import load_dotenv
from tqdm import tqdm

# --------------------------------------------------------------------------- #
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-4o-mini"              # cheaper + plenty for static code review
TOK_LIMIT = 16000                  # spare some room for the prompt/response

SRC_ROOT = pathlib.Path("output")
DST_ROOT = pathlib.Path("reports")
DST_ROOT.mkdir(exist_ok=True)

enc = tiktoken.encoding_for_model("gpt-4o-mini")  # reasonable default

SYSTEM_PROMPT = textwrap.dedent("""
    You are a security analyst. Review the supplied JavaScript code for
    indicators of compromise, obfuscation, or malicious behaviour such as
    drive-by downloads, crypto-mining, key-logging, or phishing redirects.
    Summarise findings clearly. If nothing suspicious is found, say so.
""").strip()

# --------------------------------------------------------------------------- #
def chunk_text(code: str, max_toks: int):
    toks = enc.encode(code)
    for i in range(0, len(toks), max_toks):
        yield enc.decode(toks[i : i + max_toks])

# --------------------------------------------------------------------------- #
def analyse_file(js_path: pathlib.Path) -> str:
    code = js_path.read_text(errors="ignore")
    report_parts = []

    for chunk in chunk_text(code, TOK_LIMIT - 4000):
        response = openai.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"```javascript\n{chunk}\n```"},
            ],
            max_tokens=2048,
            temperature=0,
        )
        report_parts.append(response.choices[0].message.content.strip())

    return "\n\n".join(report_parts)

# --------------------------------------------------------------------------- #
def main():
    for domain_dir in SRC_ROOT.iterdir():
        if not domain_dir.is_dir():
            continue
        report_file = DST_ROOT / f"{domain_dir.name}.md"
        with report_file.open("w") as out:
            out.write(f"# Analysis of {domain_dir.name}\n\n")
            js_files = sorted((domain_dir / "js").glob("*.js"))
            if not js_files:
                out.write("_No JS captured._\n")
                continue

            for js in tqdm(js_files, desc=domain_dir.name):
                out.write(f"## {js.name}\n")
                try:
                    findings = analyse_file(js)
                    out.write(findings + "\n\n")
                except Exception as e:
                    out.write(f"Error analysing {js.name}: {e}\n\n")

if __name__ == "__main__":
    main()