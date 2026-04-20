"""
File: clean_data.py
Purpose: Load raw job posting data, normalize key fields, derive structured attributes,
and export a cleaned dataset focused on entry-level roles.

Responsibilities:
- Standardize incoming column names across raw data sources
- Resolve expected source columns when names vary between files
- Extract structured salary and skill data from unstructured text
- Flag entry-level postings and write the cleaned dataset to disk

Notes:
- This script expects a raw CSV file at the configured data path.
- The output is intentionally filtered to entry-level roles before export.
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd

# Resolve project-relative paths so the script works regardless of execution directory
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

RAW_FILE = DATA_DIR / "raw_jobs.csv"
CLEAN_FILE = DATA_DIR / "cleaned_jobs.csv"


def main() -> None:
    """Execute the data cleaning pipeline and persist the cleaned dataset."""
    df = pd.read_csv(RAW_FILE)

    # Normalize column names to a consistent snake_case format
    # This avoids downstream issues caused by inconsistent naming in raw data sources
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    # Compute average salary from provided min/max bounds
    # Assumes both columns are numeric and present in the dataset
    df["avg_salary"] = (df["salary_min"] + df["salary_max"]) / 2

    # Treat missing experience values as 0 to avoid excluding valid entry-level roles
    df["experience_required"] = df["experience_required"].fillna(0)

    # Filter to entry-level roles (defined as requiring <= 2 years of experience)
    df = df[df["experience_required"] <= 2]

    # Ensure skills column is consistently stored as a string for downstream processing/export
    df["skills"] = df["skills"].fillna("").astype(str)

    # Extract 2-letter state code from location (e.g., "City, ST")
    # If no match is found, the result will be NaN
    df["state"] = df["location"].str.extract(r"\b([A-Z]{2})\b", expand=False)

    # Select only the fields relevant for analysis/output
    # This also enforces a consistent schema for the cleaned dataset
    cleaned = df[
        [
            "job_title",
            "company",
            "location",
            "state",
            "avg_salary",
            "skills",
            "experience_required",
        ]
    ].copy()

    # Remove rows missing essential identifying fields
    cleaned = cleaned.dropna(subset=["job_title", "location"])

    # Persist cleaned dataset to disk
    cleaned.to_csv(CLEAN_FILE, index=False)

    print(f"Saved cleaned data to: {CLEAN_FILE}")
    print(f"Rows: {len(cleaned)}")
    print(cleaned.head())


if __name__ == "__main__":
    main()