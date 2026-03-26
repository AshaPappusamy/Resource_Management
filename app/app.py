# app.py

import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------
# 1️⃣ Load & Preprocess Data
# ----------------------------
@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    # Compute total workers for convenience
    df['main_workers_total'] = df['main_workers_-_total_-_persons']
    df['rural_ratio'] = df['main_workers_-_rural_-_persons'] / df['main_workers_total']
    df['urban_ratio'] = df['main_workers_-_urban_-_persons'] / df['main_workers_total']
    return df

# ----------------------------
# 2️⃣ Metrics & Insights
# ----------------------------
def display_metrics(df):
    total_workers = df['main_workers_total'].sum()
    sector_summary = df.groupby('industrial_sector')['main_workers_total'].sum()
    largest_sector = sector_summary.idxmax()
    smallest_sector = sector_summary.idxmin()
    top_state = df.groupby('state_name')['main_workers_total'].sum().idxmax()
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Workforce", f"{total_workers:,}")
    col2.metric("Largest Sector", f"{largest_sector}", f"{sector_summary.max():,}")
    col3.metric("Smallest Sector", f"{smallest_sector}", f"{sector_summary.min():,}")
    col4.metric("Top State by Workforce", f"{top_state}")

# ----------------------------
# 3️⃣ Visualizations
# ----------------------------
def plot_bar_polar(df):
    fig = px.bar_polar(df.groupby('industrial_sector')['main_workers_total'].sum().reset_index(),
                       r='main_workers_total', theta='industrial_sector',
                       color='industrial_sector', template="plotly_dark",
                       title="Sector-wise Workforce (Bar Polar)")
    return fig

def plot_pie(df):
    fig = px.pie(df.groupby('industrial_sector')['main_workers_total'].sum().reset_index(),
                 names='industrial_sector', values='main_workers_total',
                 title="Sector Share of Workforce")
    return fig

def plot_sunburst(df):
    fig = px.sunburst(df, path=['state_name', 'district_name', 'industrial_sector'],
                      values='main_workers_total', title="Workforce Hierarchy")
    return fig

def plot_stacked_bar(df):
    df_grouped = df.groupby('industrial_sector')[['main_workers_-_rural_-_persons', 'main_workers_-_urban_-_persons']].sum().reset_index()
    fig = px.bar(df_grouped, x='industrial_sector',
                 y=['main_workers_-_rural_-_persons', 'main_workers_-_urban_-_persons'],
                 title="Rural vs Urban Workforce per Sector",
                 labels={'value':'Workers','variable':'Category'})
    return fig

def plot_map(df):
    # You need lat/lon columns; here we assume 'latitude' & 'longitude' exist
    fig = px.scatter_mapbox(df, lat='latitude', lon='longitude', size='main_workers_total',
                            hover_name='district_name', hover_data=['state_name', 'industrial_sector'],
                            zoom=4, mapbox_style="carto-positron", title="Workforce by District")
    return fig

# ----------------------------
# 4️⃣ Streamlit App Layout
# ----------------------------
st.set_page_config(page_title="Resource Management Dashboard", layout="wide")

st.title("🏭 Resource Management Dashboard")
st.markdown("Explore workforce distribution across States, Districts, and Industrial Sectors.")

# Load data
file_path = "cleaned_dataset.csv"  # Update if needed
df = load_data(file_path)

# Sidebar filters
st.sidebar.header("Filters")
states = st.sidebar.multiselect("Select States", df['state_name'].unique(), default=df['state_name'].unique())
sectors = st.sidebar.multiselect("Select Sectors", df['industrial_sector'].unique(), default=df['industrial_sector'].unique())

filtered_df = df[(df['state_name'].isin(states)) & (df['industrial_sector'].isin(sectors))]

# Metrics
st.subheader("Key Workforce Metrics")
display_metrics(filtered_df)

# Visualizations
st.subheader("Sector Analysis")
st.plotly_chart(plot_bar_polar(filtered_df), use_container_width=True)
st.plotly_chart(plot_pie(filtered_df), use_container_width=True)

st.subheader("State & District Analysis")
st.plotly_chart(plot_sunburst(filtered_df), use_container_width=True)
st.plotly_chart(plot_stacked_bar(filtered_df), use_container_width=True)

st.subheader("Geospatial Workforce Map")
st.info("Ensure your dataset contains 'latitude' and 'longitude' columns for this map.")
st.plotly_chart(plot_map(filtered_df), use_container_width=True)

# Download filtered dataset
st.subheader("Download Filtered Data")
st.download_button("Download CSV", filtered_df.to_csv(index=False), "filtered_workforce.csv", "text/csv")
