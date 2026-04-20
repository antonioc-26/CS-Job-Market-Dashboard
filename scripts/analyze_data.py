from __future__ import annotations

"""
File: analyze_jobs.py
Purpose: Read the cleaned job dataset, generate summary outputs for skills, salaries,
and geographic distribution, and save both tabular results and charts to the output directory.

Responsibilities:
- Expand comma-separated skill values into an analysis-friendly row format
- Generate summary CSV outputs for top skills, salary by skill, and jobs by state
- Produce chart images for key analysis views
- Write a compact JSON summary for downstream consumption or reporting

Notes:
- This script expects the cleaned dataset to already exist at the configured path.
- Output files are written under the project-level output directory.
"""

from pathlib import Path
import json
import pandas as pd
import matplotlib.pyplot as plt

# Resolve project-relative paths so the script can be run from any working directory.
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

CLEAN_FILE = DATA_DIR / "cleaned_jobs.csv"


def explode_skills(df: pd.DataFrame) -> pd.DataFrame:
    """
    Split comma-separated skill strings into individual rows.

    This transforms the dataset into a shape better suited for counting skill
    frequency and aggregating salary statistics by skill.
    """
    temp = df.copy()

    # Normalize missing skill values before splitting to avoid propagating NaN
    # into the exploded output.
    temp["skills"] = temp["skills"].fillna("")

    # Convert the stored comma-separated string into a normalized list of skills.
    temp["skills"] = temp["skills"].apply(
        lambda x: [s.strip().lower() for s in str(x).split(",") if s.strip()]
    )

    return temp.explode("skills")


def main() -> None:
    """Run the analysis pipeline and persist summary files and charts."""
    # Ensure the output directory exists before writing any artifacts.
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(CLEAN_FILE)
    skill_df = explode_skills(df)

    # Count the most frequently requested skills across job postings.
    top_skills = (
        skill_df["skills"]
        .value_counts()
        .head(10)
        .reset_index()
    )
    top_skills.columns = ["skill", "count"]
    top_skills.to_csv(OUTPUT_DIR / "top_skills.csv", index=False)

    # Compute average salary by skill using only rows with salary data present.
    salary_by_skill = (
        skill_df.dropna(subset=["avg_salary"])
        .groupby("skills", as_index=False)["avg_salary"]
        .mean()
        .sort_values("avg_salary", ascending=False)
        .head(10)
    )
    salary_by_skill.to_csv(OUTPUT_DIR / "salary_by_skill.csv", index=False)

    # Summarize posting counts by state for basic location distribution analysis.
    jobs_by_state = (
        df["state"]
        .dropna()
        .value_counts()
        .reset_index()
    )
    jobs_by_state.columns = ["state", "count"]
    jobs_by_state.to_csv(OUTPUT_DIR / "jobs_by_state.csv", index=False)

    # Generate a simple bar chart for the most common skills.
    plt.figure(figsize=(10, 6))
    plt.bar(top_skills["skill"], top_skills["count"])
    plt.xticks(rotation=45)
    plt.title("Top Skills")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "top_skills.png")
    plt.close()

    # Generate a bar chart for the highest average salaries by skill.
    plt.figure(figsize=(10, 6))
    plt.bar(salary_by_skill["skills"], salary_by_skill["avg_salary"])
    plt.xticks(rotation=45)
    plt.title("Salary by Skill")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "salary_by_skill.png")
    plt.close()

    # Write a compact summary for quick inspection or downstream automation.
    # This assumes at least one skill exists in the analyzed dataset.
    summary = {
        "jobs_analyzed": int(len(df)),
        "top_skill": top_skills.iloc[0]["skill"],
        "top_skill_count": int(top_skills.iloc[0]["count"]),
    }

    with open(OUTPUT_DIR / "summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    print("Analysis complete.")
    print(top_skills.head())


if __name__ == "__main__":
    main()