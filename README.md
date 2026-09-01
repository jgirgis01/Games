# Video Game Sales Data Pipeline (`clean_vg_sales.py`)

## Overview
This ETL script ingests the raw **VGChartz (2024)** dataset, filters down to commercially tracked records, handles missing release timestamps, computes decade buckets, normalizes franchise/series titles, enriches platform codes with standardized hardware metadata, and outputs an analysis-ready `.csv` file for Tableau.

---

## Processing Pipeline
Raw CSV (vgchartz-2024.csv)
│
▼

Filter Missing total_sales
│
▼

Date Imputation & Decade Binning (release_date -> last_update)
│
▼

Title Normalization (base_title extraction via Regex)
│
▼

Metadata Enrichment (Merge with platform_metadata reference table)
│
▼

Output Generation (games_final.csv)

---

## Key Transformation Steps

### 1. Sales Filtering
Rows lacking `total_sales` are dropped. This removes unreleased, cancelled, or non-commercial entries to focus solely on tracked commercial performance.

### 2. Date Parsing & Decade Binning
* **Imputation:** Combines `release_date` with `last_update` fallback via `.fillna()` to recover missing launch timestamps.
* **Decade Bucketing:** Calculates decade strings (`70s`, `80s`, `90s`, `00s`, `10s`, `20s`) using modulo-100 floor division, zero-padded to two digits. Unparseable dates (`<NA>s`) are excluded.

### 3. Franchise & Base Title Normalization
Extracts franchise prefixes by:
* Splitting on colons (`:`), hyphens (`-`), or en-dashes (`–`).
* Stripping trailing Arabic (`2`, `3`) and Roman numerals (`II`, `IV`, `X`) using regex pattern `r'\s+[0-9IVXLCDM]+$'`.
* *Example:* `"Super Mario Galaxy 2: Final Cut"` $\rightarrow$ `"Super Mario Galaxy"`.

### 4. Hardware & Platform Enrichment
Maps raw console abbreviations (`2600`, `PS2`, `NS`, `GBA`) to four structured dimensions:
* **`Platform_Full_Name`** (e.g., `Nintendo Switch`, `PlayStation 2`)
* **`Manufacturer`** (e.g., `Nintendo`, `Sony`, `Atari`, `Sega`)
* **`Form_Factor`** (e.g., `Home Console`, `Handheld`, `Computer / PC`, `Hybrid`)
* **`Is_Handheld`** (Boolean flag for regional handheld vs. console analysis)

---

SOURCE: https://www.kaggle.com/datasets/gregorut/videogamesales
