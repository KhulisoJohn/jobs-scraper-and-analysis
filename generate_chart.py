"""Create the charts (images/) and markdown tables (results.md) used in the README.

Usage:  python3 generate_charts.py      (run it in the folder that holds jobs.csv)
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # draw to files, no screen needed
import matplotlib.pyplot as plt
import pandas as pd

KEYWORD = "python"
IMAGES = Path("images")
IMAGES.mkdir(exist_ok=True)

COLOURS = ["#2a6f97", "#52796f", "#bc6c25", "#9b2226", "#6a4c93"]

df = pd.read_csv("jobs.csv")
df["region"] = df["location"].str.split(",").str[-1].str.strip()
df["is_match"] = df["title"].str.contains(KEYWORD, case=False)
total = len(df)

# ---- Numbers --------------------------------------------------------------
by_region = df["region"].value_counts()
region_table = pd.DataFrame({
    "jobs": by_region,
    "share_pct": (100 * by_region / total).round(1),
    f"{KEYWORD}_jobs": df.groupby("region")["is_match"].sum().astype(int),
}).sort_values("jobs", ascending=False)
title_counts = df["title"].value_counts()
top_titles = title_counts[title_counts > 1]  # only titles that repeat (the rest are ties at 1)

# ---- Chart 1: pie, jobs per region ---------------------------------------
fig, ax = plt.subplots(figsize=(5, 5))
by_region.plot(kind="pie", autopct="%1.1f%%", colors=COLOURS, startangle=90, ax=ax)
ax.set_ylabel("")
ax.set_title("Share of jobs per region")
fig.savefig(IMAGES / "pie_jobs_per_region.png", dpi=120, bbox_inches="tight")
plt.close(fig)

# ---- Chart 2: pie, keyword jobs vs the rest ------------------------------
fig, ax = plt.subplots(figsize=(5, 5))
df["is_match"].value_counts().rename({True: KEYWORD.title(), False: "Other"}).plot(
    kind="pie", autopct="%1.1f%%", colors=["#bbbbbb", COLOURS[0]], startangle=90, ax=ax
)
ax.set_ylabel("")
ax.set_title(f"Share of jobs with '{KEYWORD}' in the title")
fig.savefig(IMAGES / "pie_keyword_share.png", dpi=120, bbox_inches="tight")
plt.close(fig)

# ---- Chart 3: bars, all jobs vs keyword jobs per region ------------------
fig, ax = plt.subplots(figsize=(7, 4.5))
region_table[["jobs", f"{KEYWORD}_jobs"]].plot(
    kind="bar", color=["#bbbbbb", COLOURS[0]], ax=ax
)
ax.set_xlabel("Region code")
ax.set_ylabel("Number of jobs")
ax.set_title(f"Jobs per region, and how many mention '{KEYWORD}'")
ax.legend(["All jobs", f"'{KEYWORD}' jobs"])
ax.spines[["top", "right"]].set_visible(False)
plt.xticks(rotation=0)
fig.savefig(IMAGES / "bar_jobs_per_region.png", dpi=120, bbox_inches="tight")
plt.close(fig)

# ---- Chart 4: bars, top 10 job titles ------------------------------------
fig, ax = plt.subplots(figsize=(7, 4.5))
top_titles.sort_values().plot(kind="barh", color=COLOURS[1], ax=ax)
ax.set_xlabel("Number of jobs")
ax.set_ylabel("")
ax.set_title("Job titles that appear more than once")
ax.spines[["top", "right"]].set_visible(False)
fig.savefig(IMAGES / "bar_top_titles.png", dpi=120, bbox_inches="tight")
plt.close(fig)


# ---- Markdown tables ------------------------------------------------------
def md_table(frame: pd.DataFrame) -> str:
    frame = frame.reset_index()
    lines = ["| " + " | ".join(str(c) for c in frame.columns) + " |",
             "|" + "|".join("---" for _ in frame.columns) + "|"]
    for _, row in frame.iterrows():
        lines.append("| " + " | ".join(str(v) for v in row) + " |")
    return "\n".join(lines)


with open("results.md", "w", encoding="utf-8") as f:
    f.write("## Jobs per region\n\n" + md_table(region_table.rename_axis("region")) + "\n\n")
    f.write("## Job titles that appear more than once\n\n"
            + md_table(top_titles.rename("jobs").rename_axis("title").to_frame()) + "\n")

print(region_table, "\n")
print(top_titles)
print("\nSaved 4 charts to images/ and tables to results.md")
