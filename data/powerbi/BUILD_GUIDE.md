# Power BI Build Guide

This folder contains clean CSV exports of the same real RBI data used in the
web dashboard, structured for Power BI. Power BI Desktop is Windows only
software and cannot be run inside this build environment, so the `.pbix`
file itself needs to be assembled on your machine. This guide gives you the
exact steps, written so the result demonstrates the specific Power BI skills
the YP0626CEP01 job profile asks for: DAX measures, data modelling,
interactive dashboards, and drill through functionality.

## Files in this folder

| File | Contents |
|---|---|
| `totals.csv` | Year wise total complaints, YoY growth, disposal rate |
| `category_share.csv` | Complaint category breakdown by year. Includes an `is_calculated` column: FY22-23 rows are TRUE because RBI's FY22-23 report does not publish a single share-of-total figure per category, so those three figures were derived by summing entity-level data (see `../SOURCES.md` for the calculation). Consider formatting these bars with a dashed border or lighter shade in your Power BI visual to keep them visually distinct from the directly-published FY23-24 and FY24-25 figures, matching the web dashboard's treatment. |
| `splits.csv` | Entity (Bank/NBFC), centre, and bank type splits, FY22-23 through FY24-25 |

## Step 1: Import data

1. Open Power BI Desktop, **Get Data > Text/CSV**, import all three files.
2. In Power Query Editor, set data types explicitly: `fiscal_year` as Text,
   numeric columns as Decimal Number, percentage columns as Decimal Number.
3. For `splits.csv`, use **Power Query > Split Column** or filter to create
   three separate logical tables (Entity, Centre, Bank Type) if you want
   cleaner slicers, or keep as one table and use `dimension_type` as a slicer
   field. Either is fine; the unified table is faster to set up.

## Step 2: Build the data model

1. Go to the **Model** view.
2. These tables are independent dimensions of the same fiscal year, so create
   a relationship on `fiscal_year` between `totals` and `category_share` if
   you want cross filtering between the trend chart and the category chart.
3. Mark `totals.fiscal_year` as the "one" side if prompted (it has one row
   per year).

## Step 3: DAX measures to add

In the `totals` table, add these as new measures (Modelling tab > New Measure):

```dax
Total Complaints (Latest) =
CALCULATE(
    SUM(totals[total_complaints]),
    totals[fiscal_year] = "2024-25"
)
```

```dax
YoY Growth % (Latest) =
CALCULATE(
    SUM(totals[yoy_growth_pct]),
    totals[fiscal_year] = "2024-25"
)
```

```dax
Disposal Rate % (Latest) =
CALCULATE(
    SUM(totals[disposal_rate_pct]),
    totals[fiscal_year] = "2024-25"
)
```

In `category_share`, add:

```dax
Top Category Share % =
CALCULATE(
    MAX(category_share[share_pct]),
    category_share[fiscal_year] = "2024-25"
)
```

These give you the headline KPI cards (the same four stats shown at the top
of the web dashboard) as live, filterable measures rather than hardcoded text,
which is the actual point of using Power BI over a static chart.

## Step 4: Build the report page

Recommended layout, matching the web dashboard's structure:

1. **Top row**: four KPI Cards using the DAX measures above (Total
   Complaints, YoY Growth, Disposal Rate, Top Category Share).
2. **Line chart**: `fiscal_year` on the X axis, `total_complaints` on the Y
   axis, from the `totals` table. This is the three year trend.
3. **Stacked bar or clustered bar chart**: `category` on the axis,
   `share_pct` as the value, from `category_share`, with `fiscal_year` as a
   legend or small multiple to compare FY23-24 vs FY24-25.
4. **Donut or bar charts**: two small charts from `splits`, one filtered to
   `dimension_type = "Entity"` and one to `dimension_type = "Centre"`.

## Step 5: Add drill through

The job listing specifically asks for drill through functionality, so include
at least one:

1. Create a second report page named **Category Detail**.
2. On that page, add a table visual showing `category`, `complaints`,
   `share_pct`, filtered by `fiscal_year`.
3. Go back to the main page, select the category bar chart, open the
   **Format** pane, and under **Drill through**, add the `category` field as
   a drill through filter on the **Category Detail** page.
4. Right click any category bar on the main page and confirm **Drill
   through > Category Detail** works and filters correctly.

## Step 6: Polish

- Apply a consistent theme: View > Themes, or build a custom theme JSON using
  the same palette as the web dashboard (navy `#0B2240`, accent
  `#C75B3F`, cream background `#F7F5F0`) so both versions look like the same
  project.
- Add a text box citing the source: "RBI Annual Reports of Ombudsman Scheme,
  FY 2022-23 to FY 2024-25" with a link, matching `../SOURCES.md`.
- Save as `RBI_Ombudsman_Trends.pbix`.

## What to submit alongside the application

Export the final report as a PDF (**File > Export > Export to PDF**) and
include both the PDF and the `.pbix` file in your supporting materials,
since the application reviewer may not have Power BI installed to open the
`.pbix` directly. Mention the GitHub repository link (which has the live web
version) in your CV or statement of interest, since that's viewable without
any software at all.
