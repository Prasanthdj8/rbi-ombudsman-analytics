# RBI Banking Ombudsman Complaint Analytics

A small analytics project built to demonstrate the kind of work described in
RBI's Young Professional, Data Analytics and Policy Research posting
(YP0626CEP01, Consumer Education and Protection Department): complaint
classification, trend analysis, dashboard reporting, and process automation
from data dumps.

**Live dashboard:** https://prasanthdj8.github.io/rbi-ombudsman-analytics/

## What this is

Two linked pieces, both grounded in RBI's own published data wherever
possible:

1. **A trend dashboard** built entirely on real, published RBI statistics
   from the Annual Reports of the Ombudsman Scheme (FY 2022-23 through
   FY 2024-25): total complaint volumes, category breakdowns, disposal
   rates, and entity and regional splits. Every figure was read directly
   from the primary source PDFs and cross-checked. See `data/SOURCES.md`
   for full citations and a verification note.

2. **A complaint text classifier** that tags complaint-style text into RBI's
   actual published complaint categories. Since RBI does not publish
   individual complaint narratives, this part uses synthetic, author-written
   text mapped to the real category structure. This is stated clearly here
   and in `classifier/README.md`, not buried in fine print.

Both pieces are documented openly, with real data cited against primary sources and the synthetic classifier data clearly labeled as such.

## Why I built this

The job profile for this role centers on data mining, complaint trend
classification, dashboard development, and process automation, skills I've
applied in past roles (Tableau and Power BI reporting at Honeywell, SQL
reporting at VMware) but not previously in a public policy or financial
consumer protection context. This project is a concrete demonstration of
that pipeline applied to RBI's own domain, built honestly: real data, read
directly from primary sources, where real data exists, and clearly labeled
demonstration data where it doesn't.

## Project structure

```
rbi-ombudsman-analytics/
├── data/
│   ├── SOURCES.md              # citations and verification notes for every real figure used
│   ├── ombudsman_trends.json   # real RBI data, structured for the web dashboard
│   └── data-exports/
│       ├── totals.csv
│       ├── category_share.csv
│       └── splits.csv
├── docs/
│   └── index.html              # self contained web dashboard, served via GitHub Pages
├── classifier/
│   ├── generate_synthetic_complaints.py
│   ├── synthetic_complaints.csv
│   ├── classify_complaints.py
│   └── README.md               # full disclosure on data provenance and accuracy
└── README.md                   # this file
```

## Running it locally

**Web dashboard:**
```bash
cd docs
python3 -m http.server 8000
# open http://localhost:8000
```
No build step or dependencies required; it's a single static HTML file.

**Classifier:**
```bash
cd classifier
pip install scikit-learn pandas joblib
python generate_synthetic_complaints.py
python classify_complaints.py
```

## What's real and what isn't, summarized

| Component | Status |
|---|---|
| Total complaint volumes, FY22-23 to FY24-25 | Real, verified directly against RBI Annual Report PDFs |
| Category share figures (Loans & Advances, Credit Cards, etc.) | Real, verified directly against RBI Annual Report PDFs |
| Disposal rates, entity splits, regional splits | Real, verified directly against RBI Annual Report PDFs |
| Complaint category structure used by the classifier | Real (RBI's actual published categories) |
| Individual complaint text used to train the classifier | Synthetic, author written, clearly labeled |

Full citations and a verification note (including one figure that was
corrected after checking the primary source): `data/SOURCES.md`.
Full classifier disclosure: `classifier/README.md`.

## Author

Prasanth P
[linkedin.com/in/prasanthp8](https://linkedin.com/in/prasanthp8)
prasanthdj8@gmail.com

This is an independent demonstration project and is not affiliated with,
endorsed by, or produced on behalf of the Reserve Bank of India.
