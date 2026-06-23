# Integration Guide — Connect V2 UI to Existing Python Portal

## Step 1 — Keep the existing Streamlit files unchanged

Do not change the core logic in the current files:

- `home_page.py`
- `pages/Courses.py`
- `pages/Training_list.py`
- `pages/Pilots.py`
- `pages/Hacker_Rank_Assessment.py`

They can remain available as the current production interface.

## Step 2 — Copy the V2 package into the project

Copy these folders into your project root:

```text
frontend-v2/
backend_optional/
```

Your root should contain the current data files:

```text
Courses.csv
Courses.xlsx
Pilots.xlsx
Hacker_Rank_assessments.xlsx
```

## Step 3 — Install the optional JSON adapter dependencies

```bash
pip install fastapi uvicorn pandas openpyxl
```

## Step 4 — Run the V2 adapter

```bash
uvicorn backend_optional.learning_api_adapter:app --reload --port 8000
```

Open:

```text
http://127.0.0.1:8000
```

## Step 5 — Validate endpoints

```bash
curl http://127.0.0.1:8000/api/health
curl http://127.0.0.1:8000/api/courses
curl http://127.0.0.1:8000/api/workbooks/training
curl http://127.0.0.1:8000/api/workbooks/pilots
curl http://127.0.0.1:8000/api/workbooks/assessments
```

## Step 6 — Replace fallback data with live data

No code change is required if the adapter is running from the same host. The frontend calls:

```text
/api/courses
/api/workbooks/training
/api/workbooks/pilots
/api/workbooks/assessments
```

If the API is hosted elsewhere, set this before `app.js` in `index.html`:

```html
<script>
  window.LEARNING_API_BASE = "https://your-api-domain.com";
</script>
```

## Step 7 — Update exact brand colors

Open:

```text
frontend-v2/assets/css/styles.css
```

Replace the `:root` variables:

```css
--primary-blue: #0056D2;
--background-off-white: #F5F5F5;
```

Add any exact colors provided by management.

## Step 8 — Demo script for executives

1. Open the home page and show the premium V2 look.
2. Toggle Students and Corporate to show that one platform serves two audiences.
3. Open Courses and demonstrate search/category filtering.
4. Open Training List and show sheet tabs, search, and CSV download.
5. Open Pilots to show rollout readiness tracking.
6. Open Assessments to show measurable skills validation.
7. Explain that the backend is not rewritten; this is an additive frontend/API adapter layer.

## Non-breaking backend rule

The adapter reads the same CSV/XLSX sources as the existing Streamlit pages. It does not alter records, database logic, authentication, or current page routing.
