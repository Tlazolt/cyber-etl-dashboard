# Cyberwarfare & Espionage ETL Dashboard

An end-to-end ETL (Extract–Transform–Load) pipeline and interactive dashboard that visualizes global cyberwarfare and cyber-espionage activity over time.  

The project started as a **MTH 231 – Data Science Lecture (Fall 2025)** project and is now evolving into part of my public data science for my small business, **Smoking Mirror LLC**.

---

## 🧭 Project Goals

- Use a **real-world cyber incident dataset**.
- Build a **reproducible ETL pipeline** in Python:
  - Extract data from a public GitHub repo.
  - Clean and transform it into analysis-ready tables.
  - Aggregate metrics at the country–year level.
- Create **interactive visualizations**:
  - Temporal trends by threat type.
  - Ranking of countries by overall threat activity.
  - A basic **geospatial heat visualization** of top countries.
- Deploy a minimal **Flask app** on a VPS (Hostinger) as a live dashboard.

---

## 📊 Data Source

The main dataset is **DrSufi’s CyberData**:

- Raw CSV (public GitHub):  
  `https://raw.githubusercontent.com/DrSufi/CyberData/main/cyber_data.csv`

The notebook loads the CSV directly from GitHub, cleans it, and saves a processed version as `cyber_incidents_clean.csv` for the web app.

---

## 🛠 Tech Stack

- **Language:** Python
- **Core libraries:**
  - `pandas` – ETL and aggregation
  - `plotly` – interactive charts
  - `leafmap` + `folium` – maps and heat layers
  - `pycountry` – country code + centroid lookup
  - `flask` – minimal web app / dashboard
- **Environment:**
  - Development: Google Colab
  - Deployment: Hostinger VPS (Ubuntu, Gunicorn, Nginx)

---

## 🗂 Project Structure

Typical layout:

```text
cyber-etl-dashboard/
├─ README.md
├─ requirements.txt
├─ app.py                  # Flask dashboard
├─ cyber_incidents_clean.csv   # cleaned data (can be regenerated)
├─ dashboard.ipynb or cyber_etl_dashboard.ipynb
├─ templates/
│   └─ index.html          # main dashboard page
└─ static/
    ├─ style.css           # custom CSS
    └─ ...                 # images / JS if needed

