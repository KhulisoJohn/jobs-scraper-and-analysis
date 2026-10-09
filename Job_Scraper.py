"""Scrape job listings from the Fake Python Jobs site and save them to CSV."""

import argparse
import csv
import sys

import requests
from bs4 import BeautifulSoup

URL = "https://realpython.github.io/fake-jobs/"
DEFAULT_OUTPUT = "jobs.csv"
FIELDS = ["title", "company", "location", "url"]


def parse_args() -> argparse.Namespace:
    """Read options typed on the command line."""
    parser = argparse.ArgumentParser(
        description="Scrape job listings and save them to a CSV file."
    )
    parser.add_argument(
        "-k", "--keyword",
        help="only keep jobs whose title contains this word (case-insensitive)",
    )
    parser.add_argument(
        "-o", "--output",
        default=DEFAULT_OUTPUT,
        help=f"CSV file to write (default: {DEFAULT_OUTPUT})",
    )
    return parser.parse_args()


def fetch_page(url: str) -> str:
    """Download the page and return its HTML."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text


def get_text(parent, selector: str) -> str:
    """Return the stripped text of the first match, or '' if missing."""
    element = parent.select_one(selector)
    return element.get_text(strip=True) if element else ""


def get_apply_url(card) -> str:
    """Return the href of the 'Apply' link, or '' if missing."""
    for link in card.select("footer a"):
        if link.get_text(strip=True).lower() == "apply":
            return link.get("href", "")
    return ""


def parse_jobs(html: str) -> list[dict]:
    """Extract all job postings from the page HTML."""
    soup = BeautifulSoup(html, "html.parser")
    jobs = []
    for card in soup.select("div.card-content"):
        job = {
            "title": get_text(card, "h2.title"),
            "company": get_text(card, "h3.company"),
            "location": get_text(card, "p.location"),
            "url": get_apply_url(card),
        }
        # Skip cards that have no usable data at all
        if any(job.values()):
            jobs.append(job)
    return jobs


def filter_jobs(jobs: list[dict], keyword: str | None) -> list[dict]:
    """Keep only jobs whose title contains the keyword (if one is given)."""
    if not keyword:
        return jobs
    keyword = keyword.lower()
    return [job for job in jobs if keyword in job["title"].lower()]


def save_to_csv(jobs: list[dict], filename: str) -> None:
    """Write the job list to a CSV file."""
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(jobs)


def main() -> None:
    args = parse_args()

    try:
        html = fetch_page(URL)
    except requests.RequestException as error:
        sys.exit(f"Could not fetch {URL}: {error}")

    jobs = parse_jobs(html)
    if not jobs:
        sys.exit("No jobs found - the page structure may have changed.")

    jobs = filter_jobs(jobs, args.keyword)
    if not jobs:
        sys.exit(f"No jobs matched the keyword '{args.keyword}'.")

    save_to_csv(jobs, args.output)
    print(f"Saved {len(jobs)} jobs to {args.output}")


if __name__ == "__main__":
    main()
