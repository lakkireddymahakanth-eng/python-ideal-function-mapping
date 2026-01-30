# DLMDSPWP01 – Ideal Function Mapping & Deviation Analysis

**Programming with Python** – IU International University  
**Mahakanth Reddy Lakki**  
**Date:** 15 November 2025

## Project Overview
- Selects best-fitting ideal functions (least-squares) from 50 candidates
- Maps test points if deviation ≤ √2 × training deviation
- Stores results in SQLite (`ideal_functions.db`)
- Generates interactive Bokeh visualization (`function_mapping.html`)

## Files
- `train.csv`, `ideal.csv`, `test.csv` – input data
- `main.py`, `data_processor.py`, `database.py`, `visualization.py` – source code
- `function_mapping.html` – 4 interactive plots
- `ideal_functions.db` – SQLite database with `test_results` table

## How to Run
```bash
python main.py
