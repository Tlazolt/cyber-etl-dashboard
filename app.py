from flask import Flask, render_template, send_from_directory
import os
import pandas as pd
import plotly.express as px
import pycountry, random, re
import folium
from leafmap import foliumap as leafmap

app = Flask(__name__)

def build_cyber_dashboard():
    # --- Load & clean data ---
    url = "https://raw.githubusercontent.com/DrSufi/CyberData/main/cyber_data.csv"
    df = pd.read_csv(url)

    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    df = df.rename(columns={"attackdate": "date"})

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["year"] = df["date"].dt.year

    metric_cols = [
        c for c in df.columns
        if not c.startswith("rank") and c not in ["date", "country", "year"]
    ]

    df = df.dropna(subset=["country", "year"])

    agg = df.groupby(["country", "year"])[metric_cols].mean().reset_index()

    # --- Plotly figure 1: global threat over time ---
    melted = agg.melt(
        id_vars=["country", "year"],
        var_name="threat_type",
        value_name="intensity"
    )

    fig1 = px.bar(
        melted,
        x="year",
        y="intensity",
        color="threat_type",
        title="Average Cyber Threat Levels Over Time (Global Aggregates)",
    )
    fig1.update_layout(template="plotly_white", width=900, height=500)
    bar_html = fig1.to_html(full_html=False)

    # --- Plotly figure 2: top 10 countries latest year ---
    agg["total_threat_score"] = agg[metric_cols].sum(axis=1)
    latest_year = int(agg["year"].max())
    top_countries = agg[agg["year"] == latest_year].nlargest(
        10, "total_threat_score"
    )

    fig2 = px.bar(
        top_countries.sort_values("total_threat_score"),
        x="total_threat_score",
        y="country",
        orientation="h",
        title=f"Top 10 Countries by Threat Activity ({latest_year})",
        color="total_threat_score",
    )
    fig2.update_layout(template="plotly_white", height=500)
    top_html = fig2.to_html(full_html=False)

    # --- Plotly geo heatmap of threat intensity (replaces Leafmap/Folium) ---
    # Convert country names to ISO alpha-3 codes for Plotly
    def get_alpha3(name):
        try:
            return pycountry.countries.lookup(name).alpha_3
        except LookupError:
            cleaned = re.sub(
                r"(?i)(people's republic of|republic of|kingdom of|socialist|"
                r"islamic|democratic|state of|federal|the)",
                "",
                name,
            ).strip()
            try:
                return pycountry.countries.lookup(cleaned).alpha_3
            except LookupError:
                return None

    top_countries_iso = top_countries.copy()
    top_countries_iso["iso_a3"] = top_countries_iso["country"].apply(get_alpha3)
    top_countries_iso = top_countries_iso.dropna(subset=["iso_a3"])

    fig3 = px.choropleth(
        top_countries_iso,
        locations="iso_a3",
        color="total_threat_score",
        hover_name="country",
        color_continuous_scale="Viridis",
        title=f"Threat Intensity Heatmap ({latest_year})",
    )
    fig3.update_layout(template="plotly_white", height=500)
    map_html = fig3.to_html(full_html=False)

    print("DEBUG lengths:", len(bar_html), len(top_html), len(map_html))

    return bar_html, top_html, map_html


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    bar_html, top_html, map_html = build_cyber_dashboard()
    return render_template(
	'dashboard.html',
        bar_html=bar_html,
        top_html=top_html,
        map_html=map_html
    )

@app.route('/automation')
def automation():
    return render_template('automation.html')

# Optional: serve a health check
@app.route('/healthz')
def healthz():
    return {'status': 'ok'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
