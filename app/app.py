# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# ------------------------------
# Constants
# ------------------------------
DATA_PATH = "final_cleaned_industrial_data.csv"

# ------------------------------
# Load Data
# ------------------------------
@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    # Create Rural/Urban ratio
    df["rural_ratio"] = df["main_workers_-_rural_-_persons"] / df["main_workers_-_total_-_persons"]
    df["urban_ratio"] = df["main_workers_-_urban_-_persons"] / df["main_workers_-_total_-_persons"]
    return df

# ------------------------------
# Filter Data
# ------------------------------
def filter_data(df, states_selected, sectors_selected):
    if states_selected:
        df = df[df["state_name"].isin(states_selected)]
    if sectors_selected:
        df = df[df["industrial_sector"].isin(sectors_selected)]
    return df

# ------------------------------
# Sector Workforce - Bar Polar
# ------------------------------
def plot_bar_polar(df):
    sector_sum = df.groupby("industrial_sector")["main_workers_-_total_-_persons"].sum().reset_index()
    fig = px.bar_polar(sector_sum, r="main_workers_-_total_-_persons",
                       theta="industrial_sector", color="industrial_sector",
                       template="plotly_dark",
                       title="Sector-wise Workforce Distribution")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("**Insight:** This chart shows which sectors have the highest workforce concentration.")

# ------------------------------
# Sunburst Chart: State → District → Sector
# ------------------------------
def plot_sunburst(df):
    fig = px.sunburst(df, path=["state_name", "district_name", "industrial_sector"],
                      values="main_workers_-_total_-_persons",
                      color="industrial_sector",
                      title="Workforce Distribution by State → District → Sector")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("**Insight:** Hierarchy of workforce by location and industry sector.")

# ------------------------------
# Stacked Bar: Rural vs Urban
# ------------------------------
def plot_stacked_rural_urban(df):
    stacked_df = df.groupby("industrial_sector")[["main_workers_-_rural_-_persons",
                                                 "main_workers_-_urban_-_persons"]].sum().reset_index()
    fig = px.bar(stacked_df, x="industrial_sector",
                 y=["main_workers_-_rural_-_persons", "main_workers_-_urban_-_persons"],
                 title="Rural vs Urban Workforce by Sector",
                 labels={"value":"Number of Workers", "industrial_sector":"Sector"},
                 text_auto=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("**Insight:** Compare rural and urban workforce per sector to identify gaps.")

# ------------------------------
# Geospatial Map (District Workforce)
# ------------------------------
def plot_geospatial(df):
    # Ensure lat/lon columns exist; for demonstration, we use dummy lat/lon
    if "lat" not in df.columns or "lon" not in df.columns:
        st.warning("No lat/lon data found. Using dummy coordinates for demonstration.")
        df["lat"] = np.random.uniform(8, 37, df.shape[0])
        df["lon"] = np.random.uniform(68, 97, df.shape[0])
    
    district_sum = df.groupby(["district_name", "lat", "lon"])["main_workers_-_total_-_persons"].sum().reset_index()
    fig = px.scatter_mapbox(district_sum, lat="lat", lon="lon", size="main_workers_-_total_-_persons",
                            hover_name="district_name",
                            color="main_workers_-_total_-_persons",
                            color_continuous_scale=px.colors.sequential.Viridis,
                            size_max=25,
                            zoom=3,
                            mapbox_style="carto-positron",
                            title="District-wise Workforce Size")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("**Insight:** Map showing which districts have larger workforce concentration.")

# ------------------------------
# Pie Chart: Top 5 Districts by Workforce
# ------------------------------
def plot_pie_top_districts(df):
    top_districts = df.groupby("district_name")["main_workers_-_total_-_persons"].sum().nlargest(5).reset_index()
    fig = px.pie(top_districts, values="main_workers_-_total_-_persons",
                 names="district_name",
                 title="Top 5 Districts by Workforce")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("**Insight:** Highlights districts with maximum workforce allocation.")

# ------------------------------
# Streamlit Layout
# ------------------------------
st.set_page_config(page_title="Industrial Workforce Dashboard", layout="wide")

st.title("Industrial Workforce Insights - India")
st.markdown("""
Explore workforce distribution across states, districts, and industrial sectors.
Focus on rural vs urban gaps and sector resource concentration.
""")

# Load data
df = load_data(DATA_PATH)

# Sidebar filters
st.sidebar.header("Filters")
states_selected = st.sidebar.multiselect("Select States", options=df["state_name"].unique())
sectors_selected = st.sidebar.multiselect("Select Sectors", options=df["industrial_sector"].unique())

# Filtered Data
filtered_df = filter_data(df, states_selected, sectors_selected)

# Tabs for visualizations
tabs = st.tabs(["Sector Polar", "Sunburst", "Rural vs Urban", "Geospatial Map", "Top Districts Pie"])

with tabs[0]:
    plot_bar_polar(filtered_df)
with tabs[1]:
    plot_sunburst(filtered_df)
with tabs[2]:
    plot_stacked_rural_urban(filtered_df)
with tabs[3]:
    plot_geospatial(filtered_df)
with tabs[4]:
    plot_pie_top_districts(filtered_df)
