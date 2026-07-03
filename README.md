# covid_19-Analysis
# 🦠 COVID-19 India Analytics Dashboard

An interactive **Plotly Dash** web application for exploring India's state-wise daily COVID-19 data — confirmed/recovered/deceased trends, containment zone distribution, resource allocation, and state-by-state comparisons — backed by an exploratory analysis notebook.

---

## 📌 Overview

This project analyzes India's `state_wise_daily.csv` dataset (daily Confirmed / Recovered / Deceased counts per state) in two parts:

1. **`Untitled.ipynb`** — initial exploratory data analysis: loading the dataset, checking status value counts, and computing headline totals (confirmed, recovered, deceased).
2. **`index.py`** — a full interactive **Dash** dashboard that turns the raw daily data into a live, filterable analytics tool with KPI cards, trend lines, zone breakdowns, resource tracking, and state comparisons.

---

## 🛠️ Tech Stack

- **Python**
- **Dash** (`dash`, `dcc`, `html`) — web app framework
- **Plotly** (`plotly.express`, `plotly.graph_objs`) — interactive charts
- **pandas** / **numpy** — data loading & aggregation
- **Bootstrap 5** (via CDN) — layout/grid styling

---

## 📊 Dataset

- **File:** `state_wise_daily.csv`
- **Granularity:** One row per `Status` (`Confirmed` / `Recovered` / `Deceased`) per date, with one column per state code (e.g., `MH`, `KL`, `DL`) plus a `Total` column.
- **Date column:** `Date_YMD`, parsed to `datetime` for chronological sorting and filtering.
- State codes are mapped to full state/UT names (Maharashtra, Kerala, Delhi, etc.) via a lookup dictionary, filtered to only the codes actually present in the dataset.

---

## 🎛️ Dashboard Features

### Filters (apply globally)
- **State / Territory selector** — "All India" or any individual state/UT
- **Date range picker** — restrict all visuals to a custom time window

### KPI Cards
- Total Confirmed
- Active Cases (`Confirmed − Recovered − Deceased`)
- Recovered Cases
- Total Deceased

### Visuals
| Chart | Type | Description |
|---|---|---|
| **Daily Timeline Trends** | Multi-line chart | Confirmed / Recovered / Deceased over time for the selected state & date range |
| **Zoning Distribution** | Donut chart | Split of Red / Orange / Green / Blue zone counts |
| **Resource Footprint** | Bar chart | Mask / Sanitizer / Oxygen allocation totals |
| **State Standings & Insights** | Horizontal bar chart | Top 15 states ranked by a selectable metric (Confirmed / Recovered / Deceased), color-scaled |

All charts use a shared **dark theme** (`apply_dark_theme`) for a consistent, modern look (dark slate background, Inter font, muted gridlines).

---

## 🚀 How to Run

1. Install dependencies:
   ```bash
   pip install pandas numpy plotly dash
   ```
2. Make sure `state_wise_daily.csv` is in the same directory as `index.py`.
3. Run the app:
   ```bash
   python index.py
   ```
4. Open the local URL shown in the terminal (typically `http://127.0.0.1:8050/`) in your browser.

---

## 📓 Exploratory Notebook (`Untitled.ipynb`)

Quick sanity checks performed before building the dashboard:
- Loaded `state_wise_daily.csv` into a DataFrame
- Confirmed the dataset is balanced across statuses (597 rows each for Confirmed / Recovered / Deceased)
- Computed row-level totals for `Confirmed` (Active), `Recovered`, and `Deceased` status categories

---

## 📁 Repository Structure

```
├── index.py                # Dash dashboard application
├── Untitled.ipynb           # Exploratory data analysis notebook
├── state_wise_daily.csv     # Source dataset (state-wise daily COVID-19 counts, India)
└── README.md
```

---

## 💡 Key Design Notes

- **Active cases** are derived (not read directly) as `Confirmed − Recovered − Deceased` within the selected date range — this only represents cumulative cases within the filtered window, not true "currently active" patients, since the dataset is daily new-case data rather than cumulative totals.
- The **comparison chart** caps at the top 15 states to keep the horizontal bar chart readable.
- `STATE_MAP` is dynamically filtered to only include state codes that actually exist as columns in the CSV, so the dropdown never shows a state with no data.

---

## 👤 Author

**Ajay Verma**

---

## 📄 License

This project is open-sourced for educational purposes. Dataset sourced from publicly available COVID-19 India tracking data (e.g., covid19india.org / API).
