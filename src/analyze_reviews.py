from pathlib import Path
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"dataset"; GRAPHS=ROOT/"graphs"; REPORTS=ROOT/"reports"
GRAPHS.mkdir(exist_ok=True); REPORTS.mkdir(exist_ok=True)
source=DATA/"Womens Clothing E-Commerce Reviews.csv"
if not source.exists(): raise FileNotFoundError(f"Dataset CSV not found at: {source}. Check that the original CSV is present in the dataset folder.")
raw=pd.read_csv(source); missing_before=raw.isna().sum()
data=raw.drop(columns=["Unnamed: 0"],errors="ignore").copy()
for c in ["Title","Review Text"]: data[c]=data[c].fillna("").astype(str)
for c in ["Division Name","Department Name","Class Name"]: data[c]=data[c].fillna("Unknown").astype(str).str.strip()
numeric=["Clothing ID","Age","Rating","Recommended IND","Positive Feedback Count"]
for c in numeric: data[c]=pd.to_numeric(data[c],errors="coerce")
data.loc[~data["Age"].between(13,100),"Age"]=np.nan
data.loc[~data["Rating"].between(1,5),"Rating"]=np.nan
data.loc[~data["Recommended IND"].isin([0,1]),"Recommended IND"]=np.nan
data.loc[data["Positive Feedback Count"]<0,"Positive Feedback Count"]=np.nan
data=data.dropna(subset=numeric).drop_duplicates()
for c in numeric: data[c]=data[c].astype(int)
data.to_csv(DATA/"cleaned_womens_clothing_reviews.csv",index=False)
def save(name):
    plt.tight_layout(); plt.savefig(GRAPHS/name,dpi=160); plt.close()
data["Rating"].value_counts().sort_index().plot(kind="bar",figsize=(8,5)); plt.title("Customer Rating Distribution"); plt.xlabel("Rating (1–5)"); plt.ylabel("Reviews"); plt.xticks(rotation=0); save("01_rating_distribution.png")
data["Recommended IND"].map({1:"Recommended",0:"Not recommended"}).value_counts().plot(kind="bar",figsize=(7,5)); plt.title("Recommended vs Not Recommended"); plt.ylabel("Reviews"); plt.xticks(rotation=0); save("02_recommendations.png")
data.groupby("Department Name")["Rating"].mean().sort_values().plot(kind="barh",figsize=(9,5)); plt.title("Average Rating by Department"); plt.xlabel("Average rating"); plt.xlim(0,5); save("03_department_ratings.png")
cs=data.groupby("Class Name")["Rating"].agg(["mean","count"]); cs=cs[cs["count"]>=30].sort_values("mean",ascending=False).head(10).sort_values("mean"); cs["mean"].plot(kind="barh",figsize=(10,6)); plt.title("Top-Rated Clothing Classes (30+ reviews)"); plt.xlabel("Average rating"); plt.xlim(0,5); save("04_class_ratings.png")
data["Age"].plot(kind="hist",bins=20,figsize=(8,5),edgecolor="black"); plt.title("Customer Age Distribution"); plt.xlabel("Age"); plt.ylabel("Reviews"); save("05_age_distribution.png")
data["Positive Feedback Count"].clip(upper=30).plot(kind="hist",bins=16,figsize=(8,5),edgecolor="black"); plt.title("Positive Feedback Counts (30 means 30+)"); plt.xlabel("Feedback count"); plt.ylabel("Reviews"); save("06_positive_feedback.png")
data=data.copy(); data["Review_Length"]=data["Review Text"].str.len(); data.boxplot(column="Review_Length",by="Rating",figsize=(8,5),grid=False); plt.suptitle(""); plt.title("Review Text Length by Rating"); plt.xlabel("Rating"); plt.ylabel("Characters"); save("07_review_length_by_rating.png")
tokens=re.findall(r"\b[a-z]{3,}\b"," ".join(data["Review Text"].astype(str)).lower())
stop=set("the and for that this with was but are you have had not she her his they them their from were will would can all about very just really too its one out get got fit size dress love great good nice wear wore look like more when what which who how did because been into also than then there here still only some much little".split())
freq=pd.Series([w for w in tokens if w not in stop]).value_counts().head(15).sort_values()
freq.plot(kind="barh",figsize=(9,6)); plt.title("Most Frequent Review Words"); plt.xlabel("Count"); save("08_common_words.png")
dept=data.groupby("Department Name")["Rating"].agg(["mean","count"]).drop(index="Unknown",errors="ignore").sort_values("mean",ascending=False)
aq1,aq3=data["Age"].quantile([.25,.75]); ai=aq3-aq1; fq1,fq3=data["Positive Feedback Count"].quantile([.25,.75]); fi=fq3-fq1
age_flags=int(((data["Age"]<aq1-1.5*ai)|(data["Age"]>aq3+1.5*ai)).sum()); fb_flags=int((data["Positive Feedback Count"]>fq3+1.5*fi).sum())
report=f"""# Short Insights Report

- Original records: {len(raw):,}; cleaned records: {len(data):,}.
- Average rating: {data["Rating"].mean():.2f}/5.
- Ratings 4 or 5: {(data["Rating"]>=4).mean()*100:.1f}%.
- Recommendation rate: {(data["Recommended IND"]==1).mean()*100:.1f}%.
- Mean age: {data["Age"].mean():.1f}; median age: {data["Age"].median():.0f}.
- Highest average named department: {dept.index[0]} ({dept.iloc[0]["mean"]:.2f}/5).
- Lowest average named department: {dept.index[-1]} ({dept.iloc[-1]["mean"]:.2f}/5).
- Median positive feedback: {data["Positive Feedback Count"].median():.0f}; 99th percentile: {data["Positive Feedback Count"].quantile(.99):.0f}.
- Mean review length: {data["Review Text"].str.len().mean():.0f} characters.
- Age-rating correlation: {data["Age"].corr(data["Rating"]):.3f}.

## Cleaning notes
Missing values before cleaning:\n{missing_before[missing_before>0].to_string()}
IQR age bounds {aq1-1.5*ai:.1f} to {aq3+1.5*ai:.1f}; flagged {age_flags}.
IQR positive-feedback upper bound {fq3+1.5*fi:.1f}; flagged {fb_flags}. Outliers are not automatically deleted because an IQR flag does not prove an error.

## Limitations
This describes one retailer's dataset, not all shoppers. Correlation does not prove causation, and word counts are not sentiment analysis.
"""
(REPORTS/"insights_report.md").write_text(report,encoding="utf-8")
(REPORTS/"data_cleaning_log.md").write_text(f"""# Data Cleaning Log

Original shape: {raw.shape[0]:,} rows × {raw.shape[1]} columns.

Missing values before cleaning:\n{missing_before[missing_before>0].to_string()}

- Dropped `Unnamed: 0`, an exported row index.
- Filled missing review title/text with blank strings and missing clothing categories with `Unknown`.
- Converted numeric fields and validated age (13–100), rating (1–5), recommendation (0/1), and non-negative feedback count.
- Removed exact duplicates after dropping the exported index.
- IQR age bounds: {aq1-1.5*ai:.1f} to {aq3+1.5*ai:.1f}; flagged {age_flags}.
- Positive-feedback IQR upper bound: {fq3+1.5*fi:.1f}; flagged {fb_flags}.
- IQR flags were retained because unusual values are not necessarily errors.
- Cleaned output: {len(data):,} rows × {data.shape[1]} columns.
""",encoding="utf-8")
print(f"Cleaned {len(data):,} records; generated eight charts and reports.")
