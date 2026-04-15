# Business Registry Web Scraper

## Overview

This project is a Python web scraper that extracts business registry records from a demo website:

https://scraping-trial-test.vercel.app

The website:
- Is built with React / Next.js
- Uses multi-page result navigation
- Serves business listings and profiles via server-rendered HTML

Although the content is currently accessible via direct HTTP requests, **Selenium was intentionally chosen** as the scraping interface to model real browser behavior and to avoid relying on assumptions about the site’s current or future rendering and data-delivery strategy.

The script:
- Accepts a user-provided search term
- Navigates through all result pages
- Opens each business profile
- Extracts detailed business and registered agent information
- Saves results to both JSON and CSV formats

---

## Table of Contents

- [Overview](#overview)
- [What Data Is Extracted](#what-data-is-extracted)
- [Output Files](#output-files)
- [Requirements](#requirements)
- [Version Information](#version-information)
- [Step-by-Step Installation (Beginner Friendly)](#step-by-step-installation-beginner-friendly)
- [How to Run the Script](#how-to-run-the-script)
- [Search Term Rules](#search-term-rules)
- [Pagination Handling](#pagination-handling)
- [Error Handling & Logging](#error-handling--logging)
- [Performance Notes](#performance-notes)
- [Limitations](#limitations)
- [Repository Structure](#repository-structure)
- [Versioning](#versioning)
- [Author’s Notes](#authors-notes)
- [Author](#author)

---

## What Data Is Extracted

For each business, the scraper extracts the following fields from the **Business Profile** page:

- Business Name
- Registration ID
- Status
- Filing Date
- Registered Agent Name
- Registered Agent Address
- Registered Agent Email (if available)

All fields are scraped directly from the site.  
No data is inferred, synthesized, or fabricated.

---

## Output Files

After execution, two output files are created in the project directory.

### output.json (example)

```json
{
  "business_name": "Silver Tech CORP",
  "registration_id": "SD0000001",
  "status": "Active",
  "filing_date": "1999-12-04",
  "agent_name": "Sara Smith",
  "agent_address": "1545 Maple Ave",
  "agent_email": "sara.smith@example.com"
}
```

### output.csv (example)

| business_name    | registration_id | status | filing_date | agent_name | agent_address  | agent_email            |
|------------------|-----------------|--------|-------------|------------|----------------|------------------------|
| Silver Tech CORP | SD0000001       | Active | 1999-12-04  | Sara Smith | 1545 Maple Ave | sara.smith@example.com |

---

## Requirements

- Python 3.x
- Mozilla Firefox
- GeckoDriver (Firefox WebDriver)
- Internet connection
- Git (optional)

---

## Version Information

This repository follows **Semantic Versioning**.

**Latest stable release:**  
**v1.3.1**

v1.3.1 is a documentation-only update that corrects technical descriptions and clarifies architectural and tooling decisions.  
No functional or behavioral changes were introduced relative to v1.3.0.

---

## Step-by-Step Installation (Beginner Friendly)

### Option A: Download the Latest Stable Release

1. Go to: https://github.com/Shnxxx/scraping-trial-test
2. Open the **Releases** section
3. Download the latest release archive
4. Extract the files
5. Open a terminal inside the project directory

---

### Option B: Clone Using Git

```bash
git clone https://github.com/Shnxxx/scraping-trial-test.git
cd scraping-trial-test
git checkout v1.3.1
```

---

### (Optional) Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it:

**Windows**
```bash
.venv\Scripts\activate
```

**macOS / Linux**
```bash
source .venv/bin/activate
```

---

### Install Dependencies

```bash
pip install selenium
```

---

## How to Run the Script

```bash
python scraper.py
```

1. Firefox launches automatically
2. Enter a search term (minimum 3 characters)
3. The script navigates all result pages and business profiles
4. Results are written to `output.json` and `output.csv`

---

## Search Term Rules

- Minimum of **3 characters**
- Empty searches are not allowed
- Wildcard searches are not supported

---

## Pagination Handling

- URL-based pagination
- All result pages are processed sequentially
- Stable page-level indicators are used to avoid stale element references caused by frontend re-renders

---

## Error Handling & Logging

- Explicit waits ensure DOM readiness
- Optional fields are handled safely
- Errors are logged to `scraper.log`
- Individual record failures do not halt execution

---

## Performance Notes

- Browser automation is inherently slower than direct HTTP scraping
- This tradeoff is intentional and accepted
- The implementation prioritizes correctness, transparency, and resilience over raw throughput

---

## Limitations

- Requires a local browser and WebDriver
- Slower than a requests-based scraper
- Resume-after-crash is not implemented
- Full registry enumeration without a search term is not supported

---

## Repository Structure

```
scraping-trial-test/
├── scraper.py
├── output.json
├── output.csv
├── scraper.log
├── README.md
├── .gitignore
```

---

## Versioning

- v1.0.0 – Initial working scraper
- v1.1.0 – Business profile navigation
- v1.2.0 – CSV output and stability fixes
- v1.3.0 – Agent scraping and performance tuning
- v1.3.1 – Documentation corrections and clarifications

---

## Author’s Notes

### Why Selenium Instead of requests + BeautifulSoup

While the site’s current HTML is server-rendered and technically scrapeable via
`requests` and `BeautifulSoup`, Selenium was selected based on **engineering risk
management**, not minimum technical feasibility.

Specifically:

- The site is built with React / Next.js, where rendering strategy (SSR, SSG, CSR)
  can change without altering visible browser behavior but can silently break
  request-based scrapers.
- Pagination and navigation are expressed through user-facing UI flows rather than
  a documented or stable backend API.
- A browser-driven approach avoids assumptions about where data originates, how it
  is rendered, or whether it will remain present in initial HTML responses.
- Selenium ensures continued correctness if content delivery shifts toward client-side
  rendering, hydration, or JavaScript-triggered navigation.

In this context, Selenium intentionally trades performance for robustness and
maintainability. This mirrors real-world scraping constraints, where browser
automation is often the only stable interface available.

### Scope Decisions

Persistent resume logic and API-based scraping were intentionally excluded to keep
the solution focused, transparent, and aligned with browser-oriented scraping
constraints.

---

## Author

Tanush
GitHub: https://github.com/tanush10061
