"""Explore jobs.csv with pandas."""

import pandas as pd

df = pd.read_csv("jobs.csv")

# 1. The basics
print("Rows and columns:", df.shape)
print("\nFirst 5 rows:")
print(df.head())

print("\nColumn types and missing values:")
df.info()

# 2. Data quality
print("\nMissing values per column:")
print(df.isna().sum())
print("Duplicate rows:", df.duplicated().sum())

# 3. Simple questions
print("\nMost common job titles:")
print(df["title"].value_counts().head(10))

python_jobs = df[df["title"].str.contains("python", case=False)]
print(f"\nJobs with 'python' in the title: {len(python_jobs)}")
print(python_jobs[["title", "company", "location"]])

print("\nCompanies with more than one job:")
company_counts = df["company"].value_counts()
print(company_counts[company_counts > 1])

# 4. Location: the text after the last comma is a two-letter code (AA, AE, AP)
df["region"] = df["location"].str.split(",").str[-1].str.strip()
print("\nJobs per region code:")
print(df["region"].value_counts())

# 5. Save a cleaned copy with the new column
df.to_csv("jobs_clean.csv", index=False)
print("\nSaved jobs_clean.csv")
