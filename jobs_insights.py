"""Ask a question, answer it with pandas, chart it, and write the finding.

Question: Which regions have the most jobs with KEYWORD in the title?
Usage:    python3 jobs_insights.py
"""

import matplotlib
matplotlib.use("Agg")  # draw to a file, no screen needed
import matplotlib.pyplot as plt
import pandas as pd

KEYWORD = "python"  # change this to "engineer", "manager", ... and re-run

# ---- Taste 1: ask a question, answer it with pandas ------------------------
df = pd.read_csv("jobs.csv")

# The text after the last comma in "Stewartbury, AA" is the region code
df["region"] = df["location"].str.split(",").str[-1].str.strip()
df["matches"] = df["title"].str.contains(KEYWORD, case=False)

summary = (
    df.groupby("region")
    .agg(all_jobs=("title", "count"), matching_jobs=("matches", "sum"))
    .sort_values("matching_jobs", ascending=False)
)
summary["matching_pct"] = (100 * summary["matching_jobs"] / summary["all_jobs"]).round(1)
print(summary)

# ---- Taste 2: make a chart --------------------------------------------------
ax = summary[["all_jobs", "matching_jobs"]].plot(
    kind="bar",
    color=["#bbbbbb", "#2a6f97"],
    figsize=(7, 4.5),
    title=f"Jobs per region, and how many mention '{KEYWORD}'",
)
ax.set_xlabel("Region code")
ax.set_ylabel("Number of jobs")
ax.legend(["All jobs", f"'{KEYWORD}' jobs"])
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("jobs_per_region.png", dpi=120)
print("\nSaved chart: jobs_per_region.png")

# ---- Taste 3: write the finding in plain English ---------------------------
total = len(df)
matching = int(df["matches"].sum())

if matching == 0:
    finding = f"None of the {total} jobs have '{KEYWORD}' in the title."
else:
    top_region = summary.index[0]
    top_count = int(summary.iloc[0]["matching_jobs"])
    finding = (
        f"Of {total} jobs, {matching} ({100 * matching / total:.1f}%) have "
        f"'{KEYWORD}' in the title. Region {top_region} has the most "
        f"({top_count}), which is {100 * top_count / matching:.0f}% of all "
        f"'{KEYWORD}' jobs."
    )

print("\nFINDING:", finding)
with open("findings.txt", "w", encoding="utf-8") as f:
    f.write(finding + "\n")
print("Saved finding: findings.txt")
