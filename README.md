# Learning Portal V2 — Premium Frontend Upgrade

This package contains a complete vanilla JavaScript frontend for a modernized V2 learning portal, plus an optional additive Python JSON adapter.

## What is included

```text
learning_portal_v2/
├── frontend-v2/
│   ├── index.html
│   └── assets/
│       ├── css/styles.css
│       └── js/
│           ├── data-service.js
│           └── app.js
├── backend_optional/
│   └── learning_api_adapter.py
└── docs/
    ├── design-rationale.md
    └── integration-guide.md
```

## Design intent

The interface is designed to feel premium, credible, and executive-ready while preserving the current business functionality:

- Home hub for the learning portal
- Course catalog with category filters and search
- Training List sheet viewer
- Pilots sheet viewer
- HackerRank Assessment sheet viewer
- CSV export for table views
- Persona switch for university students and corporate learners

## Quick static preview

Open this file in a browser:

```text
frontend-v2/index.html
```

The UI will run with fallback demo data when the Python adapter is not running.

## Run with Python JSON adapter

From the package root:

```bash
pip install fastapi uvicorn pandas openpyxl
uvicorn backend_optional.learning_api_adapter:app --reload --port 8000
```

Open:

```text
http://127.0.0.1:8000
```

The adapter expects the existing files in the project root:

```text
Courses.csv
Courses.xlsx
Pilots.xlsx
Hacker_Rank_assessments.xlsx
```

## Color palette

The palette is centralized in `frontend-v2/assets/css/styles.css` inside the `:root` block. Replace the variables there with the exact company-approved colors.

Current defaults:

```css
--primary-blue: #0056D2;
--background-off-white: #F5F5F5;
```
