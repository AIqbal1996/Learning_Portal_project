"""
Optional additive Python adapter for Learning Portal V2.
This does not replace the existing Streamlit pages. It reads the same CSV/XLSX
files and exposes JSON endpoints for the vanilla JS frontend.

Run from the project root where Courses.csv, Courses.xlsx, Pilots.xlsx and
Hacker_Rank_assessments.xlsx are stored:
    pip install fastapi uvicorn pandas openpyxl
    uvicorn backend_optional.learning_api_adapter:app --reload --port 8000
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import pandas as pd
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FRONTEND_DIR = PROJECT_ROOT / "frontend-v2"

app = FastAPI(title="Learning Portal V2 API", version="2.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

CATEGORY_MAPPING: dict[str, list[str]] = {
    "Data Engineering": [
        "Data Engineering", "Data Architecture", "Data Warehouse", "ETL", "DataOps",
        "MLOps", "Data Management", "Data Mangement", "Datastage", "Airflow",
        "Data Science", "GCP Data Engineer", "PubSub", "Dataproc",
    ],
    "Azure": ["Azure", "Cosmos DB", "Logic App", "MS Fabric", "SSAS", "SSIS", "PubSub"],
    "AWS": ["AWS"],
    "Spark": ["Spark", "PySpark", "Scala", "Hadoop", "Dataproc"],
    "Snowflake": ["Snowflake"],
    "Power BI": ["Power BI", "Power Platform", "Power Automate", "Power Apps", "Tableau"],
    "SQL": ["SQL", "MySQL", "Postgre", "MongoDB", "Teradata", "Kustos", "BigQuery"],
}

WORKBOOK_FILES = {
    "training": "Courses.xlsx",
    "pilots": "Pilots.xlsx",
    "assessments": "Hacker_Rank_assessments.xlsx",
}


def clean_cell(value: Any) -> Any:
    """Convert pandas/Excel values into JSON-safe scalars."""
    if pd.isna(value):
        return ""
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return value


def get_href(link_text: str) -> str:
    """Return first URL from the raw CSV link cell, matching existing behavior."""
    link_text = str(link_text or "").strip()
    if not link_text:
        return ""
    url_match = re.search(r"https?://\S+", link_text)
    if url_match:
        return url_match.group(0).rstrip(";,).")
    return ""


def infer_category(course_name: str) -> str:
    lower_name = course_name.lower()
    for category, keywords in CATEGORY_MAPPING.items():
        if any(keyword.lower() in lower_name for keyword in keywords):
            return category
    return "Data Engineering"


def course_description(name: str, category: str) -> str:
    return f"Focused {category} learning experience designed for practical application, retention, and role readiness."


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/categories")
def categories() -> dict[str, list[str]]:
    return CATEGORY_MAPPING


@app.get("/api/courses")
def courses(
    category: str | None = Query(default=None),
    q: str | None = Query(default=None, description="Search text"),
) -> dict[str, Any]:
    csv_path = PROJECT_ROOT / "Courses.csv"
    if not csv_path.exists():
        raise HTTPException(status_code=404, detail="Courses.csv not found in project root")

    df = pd.read_csv(csv_path, usecols=["Course Name", "Link", "Duration(Hr)"])
    df = df.dropna(subset=["Course Name"]).copy()
    df["Duration(Hr)"] = pd.to_numeric(df["Duration(Hr)"], errors="coerce").fillna(0)

    records = []
    for idx, row in df.reset_index(drop=True).iterrows():
        name = str(row["Course Name"])
        inferred_category = infer_category(name)
        record = {
            "id": f"COURSE-{idx + 1:03d}",
            "name": name,
            "category": inferred_category,
            "durationHours": float(row["Duration(Hr)"]),
            "level": "Advanced" if float(row["Duration(Hr)"]) >= 12 else "Intermediate" if float(row["Duration(Hr)"]) >= 8 else "Beginner",
            "link": get_href(str(row.get("Link", ""))),
            "description": course_description(name, inferred_category),
        }
        records.append(record)

    if category and category != "All":
        records = [item for item in records if item["category"] == category]

    if q:
        query = q.lower()
        records = [
            item for item in records
            if query in " ".join(str(value).lower() for value in item.values())
        ]

    return {"courses": records, "count": len(records)}


@app.get("/api/workbooks/{workbook_name}")
def workbook(workbook_name: str) -> dict[str, Any]:
    file_name = WORKBOOK_FILES.get(workbook_name)
    if not file_name:
        raise HTTPException(status_code=404, detail="Unknown workbook")

    workbook_path = PROJECT_ROOT / file_name
    if not workbook_path.exists():
        raise HTTPException(status_code=404, detail=f"{file_name} not found in project root")

    excel_file = pd.ExcelFile(workbook_path)
    sheets = []
    for sheet_name in excel_file.sheet_names:
        df = pd.read_excel(workbook_path, sheet_name=sheet_name)
        rows = [
            {str(column): clean_cell(value) for column, value in row.items()}
            for row in df.to_dict(orient="records")
        ]
        sheets.append({"name": sheet_name, "rows": rows})

    titles = {
        "training": "Training List",
        "pilots": "Pilots",
        "assessments": "HackerRank Assessment",
    }
    subtitles = {
        "training": "Curated learning sheets with searchable, downloadable records.",
        "pilots": "Pilot programs, rollout readiness, and stakeholder actions.",
        "assessments": "Assessment records for technical practice and benchmarking.",
    }
    return {
        "title": titles.get(workbook_name, workbook_name.title()),
        "subtitle": subtitles.get(workbook_name, "Search and export source records."),
        "sheets": sheets,
    }


# Serve the V2 frontend from the same Python process when desired.
# Keep this at the bottom so /api/* routes take precedence.
if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend-v2")
