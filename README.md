# Python Job Listings Scraper

A beginner-friendly web scraper that collects job listings from the [Fake Python Jobs](https://realpython.github.io/fake-jobs/) practice site, saves them to CSV, and includes a small pandas analysis of the results.

The target site is built for learning, so it is safe to scrape and has no anti-bot protection.

## Features

- Fetches the listings page with `requests` and parses it with Beautiful Soup
- Extracts **job title**, **company**, **location** and **job URL** for every posting
- Handles missing fields (they become empty values) and network errors
- Optional `--keyword` filter on the job title (case-insensitive)
- Optional `--output` flag to choose the CSV file name
- Pandas scripts to explore the data and turn it into a chart and a plain-English finding

## Requirements

- Python 3.10 or newer
- requests, beautifulsoup4, pandas, matplotlib (see `requirements.txt`)

## Installation

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>

python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

### 1. Scrape the jobs

```bash
python3 Job_Scraper.py                         # all jobs -> jobs.csv
python3 Job_Scraper.py -k python               # only titles containing "python"
python3 Job_Scraper.py -k engineer -o engineer_jobs.csv
```

Success looks like: `Saved 100 jobs to jobs.csv`

### 2. Explore the data with pandas

```bash
python3 explore_jobs.py
```

Prints the shape, column types, missing values, duplicates, most common titles, jobs per region code and more, then saves `jobs_clean.csv` with an extra `region` column.

### 3. Get an insight

```bash
python3 jobs_insights.py
```

Answers the question *"Which regions have the most jobs with a given keyword in the title?"*
It prints a summary table, saves a chart (`jobs_per_region.png`) and writes a one-sentence finding to `findings.txt`.
Change `KEYWORD` at the top of the file to ask a different question.

## Output

`jobs.csv` has one row per job:

| Column     | Description                      |
|------------|----------------------------------|
| `title`    | Job title                        |
| `company`  | Company name                     |
| `location` | City and region code             |
| `url`      | Link to the job's apply page     |

Example row:

```csv
title,company,location,url
Senior Python Developer,"Payne, Roberts and Davis","Stewartbury, AA",https://realpython.github.io/fake-jobs/jobs/senior-python-developer-0.html
```

## Project structure

```
.
├── Job_Scraper.py       # scraper: fetch, parse, filter, save
├── explore_jobs.py      # pandas data exploration
├── jobs_insights.py     # question -> chart -> plain-English finding
├── requirements.txt     # dependencies
├── README.md
├── .gitignore
└── jobs.csv             # sample output from the scraper
```

## How the scraper works

1. `parse_args()` reads the `--keyword` and `--output` options.
2. `fetch_page()` downloads the HTML and raises an error on a bad response.
3. `parse_jobs()` finds every `div.card-content` and extracts the fields with CSS selectors.
4. `get_text()` and `get_apply_url()` return `""` when an element is missing instead of crashing.
5. `filter_jobs()` keeps only titles containing the keyword, if one was given.
6. `save_to_csv()` writes the results to a CSV file.

## What I learned

- Inspect the page's HTML first: the code only follows the structure you find, and a single misspelled class name (`card-contant`) returns zero results.
- Real-world data is messy, so missing values and errors need handling.
- Small single-purpose functions are easier to test and fix.
- Every analysis follows the same loop: ask a question, query the data, chart it, explain it in plain English.

## Ideas for improvement

- Scrape each job's detail page for the full description
- Add unit tests for `parse_jobs()` using a saved HTML sample
- Filter by location or company as well as title
- Export to JSON or SQLite

## Disclaimer

For educational purposes only. Always check a website's terms of service and `robots.txt` before scraping a real site.

## License

MIT
