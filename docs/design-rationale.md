# Design Rationale — Learning Portal V2

## Current platform understanding

The uploaded Python files show a Streamlit multi-page learning portal:

- `home_page.py` acts as the portal hub and routes to the other pages.
- `Courses.py` reads `Courses.csv`, expects `Course Name`, `Link`, and `Duration(Hr)`, applies category filtering, search, course cards, and summary metrics.
- `Training_list.py` reads `Courses.xlsx`, creates one tab per Excel sheet, supports table search and CSV download.
- `Pilots.py` reads `Pilots.xlsx`, creates one tab per Excel sheet, supports table search and CSV download.
- `Hacker_Rank_Assessment.py` reads `Hacker_Rank_assessments.xlsx`, creates one tab per Excel sheet, supports table search and CSV download.

## UX psychology applied

### 1. Reduced cognitive load

The V2 uses chunked cards, short labels, clear hierarchy, and a sticky filter bar. Learners should not need to think about where to start; the interface gives a visible path from discovery to launch.

### 2. Persona-based relevance

A student and a corporate employee have different motivations. Students are motivated by employability, momentum, and skill confidence. Corporate employees are motivated by business relevance, role readiness, and credibility. The persona switch changes the framing without fragmenting the product.

### 3. Visual authority and trust

The layout uses a restrained enterprise palette, strong whitespace, mature typography, soft borders, and data-led cards. This creates a premium, Coursera-inspired impression suitable for executive demos.

### 4. Retention nudges

Course duration, level, category, and launch actions are visible on the card. This supports commitment before the click and reduces abandonment caused by uncertainty.

### 5. Scannability

Tables are optimized for enterprise users with sticky headings, clean rows, search-first interaction, and export actions. This is important for training managers and leadership reviewers.

### 6. Progressive disclosure

The home page gives strategic pathways. Detailed data is one click deeper. This avoids overwhelming first-time viewers while still supporting power users.

## Audience fit

### University students

- Clear course cards
- Skill categories
- Assessment access
- Employability-focused language
- Lightweight launch actions

### Corporate professionals

- Executive-grade visual polish
- Training and pilot tracking
- Measurable readiness indicators
- Table search and CSV exports
- Role/path based framing
