# NewsFlow: Automated ETL Pipeline & Trend Monitor

## Problem Statement
Training machine learning models on news data requires consistent, high-quality historical datasets. One-off datasets are often noisy, prone to duplicates, and lack temporal context. Businesses need autonomous systems that can ingest unstructured data daily, validate its quality, and persist it without manual intervention to enable downstream NLP analysis and trend monitoring.

## Objective
To architect and deploy a robust, self-healing ETL (Extract, Transform, Load) pipeline that autonomously harvests tech news headlines, enforces data integrity through idempotency, and demonstrates engineering reliability using CI/CD automation.

## Data Source / Dataset
* **Source:** Hacker News (Y Combinator)
* **Method:** Web Scraping via `BeautifulSoup` (Python)
* **Volume:** Daily ingestion of ~30 top headlines (scalable to thousands)
* **Storage:** SQLite database with "Git Scraping" persistence

## Methodology / Approach
* **Ingestion:** Implemented a modular Python scraper with error handling (retries, user-agent rotation) to fetch raw HTML.
* **Transformation:** Developed a cleaning module using Regex to normalize text (whitespace removal, formatting) and validate metadata.
* **Storage Logic:** Designed an idempotent SQLite schema with `UNIQUE` constraints on URLs to prevent duplicate entries and ensure data integrity.
* **Automation:** Configured GitHub Actions (Cron Job) to execute the pipeline daily at 06:00 UTC, committing the updated database back to the repository to simulate persistent storage.

## Exploratory Data Analysis (EDA)
* **Data Validation:** The pipeline includes runtime statistical checks to log the count of new vs. duplicate articles, ensuring the scraper is functioning correctly.
* **Trend Monitoring:** The database structure supports longitudinal analysis of headline keywords over time (e.g., tracking the frequency of "AI" or "Rust").

## Modeling & Evaluation
* **Not applicable:** This project focuses on Data Engineering and MLOps infrastructure rather than predictive modeling. The primary "evaluation" metric is pipeline uptime and data integrity (zero duplicates).

## Results & Key Findings
* **Zero-Touch Automation:** Achieved 100% autonomous daily execution using GitHub Actions, requiring no manual triggers.
* **Data Integrity:** Successfully handled duplicate detection via SQL constraints, ensuring the dataset grows cleanly without redundancy.
* **Resilience:** The pipeline gracefully handles network errors and "stale element" changes without crashing, logging issues for review.

## Tools & Technologies
* **Language:** Python 3.9
* **Libraries:** `pandas`, `BeautifulSoup4`, `requests`, `sqlite3`
* **Infrastructure:** GitHub Actions (CI/CD), Git
* **Database:** SQLite

## Limitations
* **Storage:** Currently relies on "Git Scraping" (committing the DB to the repo), which is suitable for portfolio scale but not enterprise production (which would use AWS RDS or PostgreSQL).
* **Source Diversity:** Currently scraped from a single aggregator (Hacker News); expanding to dynamic JS-heavy sites would require `Selenium` or `Playwright`.

## Future Improvements
* **Drift Detection:** Implement a statistical module to flag significant changes in keyword frequency (e.g., a sudden spike in "Layoffs") compared to the 7-day moving average.
* **Cloud Migration:** Migrate the storage layer to a cloud-hosted PostgreSQL instance to decouple data from the codebase.
* **Dashboarding:** Connect the SQLite database to a Streamlit app for real-time visualization of news trends.

## How to Run the Project
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/news-flow.git](https://github.com/YOUR_USERNAME/news-flow.git)
    cd news-flow
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the pipeline manually:**
    ```bash
    python main.py
    ```
4.  **View the database:**
    Use any SQLite viewer (e.g., DB Browser for SQLite) to open `data/news.db`.

## Project Structure
```text
news-flow/
├── .github/workflows/  # CI/CD Configuration
├── data/               # SQLite Database
├── src/                # Source Code
│   ├── scraper.py      # Data Extraction
│   ├── cleaner.py      # Data Transformation
│   └── database.py     # Storage & Schema
├── main.py             # Pipeline Orchestrator
├── requirements.txt    # Dependencies
└── README.md           # Documentation
