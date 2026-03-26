# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# Data Loading Function
# -------------------------------
@st.cache_data
def load_data(file_path):
    """
    Load cleaned industrial workforce dataset
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        st.error(f"File not found: {file_path}. Please check the file location!")
        return pd.DataFrame()

# -------------------------------
# Feature Engineering Functions
# -------------------------------
def add_features(df):
    """
    Adds new features for insights:
    - Rural/Urban workforce ratio
    - Total workforce
    """
    df['total_workforce'] = df['main_workers_-_total_-_persons'] + df['marginal_workers_-_total_-_persons']
    df['rural_urban_ratio'] = (df['main_workers_-_rural_-_persons'] + df['marginal_workers_-_rural_-_persons']) / \
                              (df['main_workers_-_urban_-_persons'] + df['marginal_workers_-_urban_-_persons'] + 1e-6)
    return df

# -------------------------------
# Visualization Functions
# -------------------------------
def bar_polar_sector(df):
    """
    Polar bar chart: Workforce distribution by Industrial Sector
    """
    df_sector = df.groupby('industrial_sector')['total_workforce'].sum().reset_index()
    fig = px.bar_polar(df_sector, r='total_workforce', theta='industrial_sector',
                       color='industrial_sector', template='plotly_dark',
                       title="Sector-wise Workforce Distribution")
    return fig

def sunburst_state_district_sector(df):
    """
    Sunburst: State → District → Industrial Sector
    """
    df_sun = df.groupby(['state_name', 'district_name', 'industrial_sector'])['total_workforce'].sum().reset_index()
    fig = px.sunburst(df_sun, path=['state_name', 'district_name', 'industrial_sector'], values='total_workforce',
                      color='total_workforce', color_continuous_scale='Viridis',
                      title="Workforce Hierarchy: State → District → Sector")
    return fig

def geospatial_map(df):
    """
    Map: Workforce size by district
    NOTE: Requires 'latitude' and 'longitude' columns. Replace below with geocoding if needed.
    """
    if 'latitude' not in df.columns or 'longitude' not in df.columns:
        st.warning("Geospatial map not available: 'latitude'/'longitude' missing in dataset.")
        return None
    
    df_map = df.groupby(['district_name', 'state_name', 'latitude', 'longitude'])['total_workforce'].sum().reset_index()
    fig = px.scatter_mapbox(df_map, lat='latitude', lon='longitude', size='total_workforce',
                            hover_name='district_name', hover_data=['state_name', 'total_workforce'],
                            color='total_workforce', color_continuous_scale='Turbo', zoom=4, height=600)
    fig.update_layout(mapbox_style="open-street-map", title="District-wise Workforce Size")
    return fig

def stacked_rural_urban(df):
    """
    Stacked bar: Rural vs Urban workforce by Industrial Sector
    """
    df_stack = df.groupby('industrial_sector')[['main_workers_-_rural_-_persons', 'main_workers_-_urban_-_persons']].sum().reset_index()
    fig = px.bar(df_stack, x='industrial_sector', y=['main_workers_-_rural_-_persons', 'main_workers_-_urban_-_persons'],
                 title="Rural vs Urban Workforce by Sector", barmode='stack', height=500)
    return fig

# -------------------------------
# Streamlit App
# -------------------------------
st.set_page_config(page_title="Industrial Workforce Insights", layout="wide")
st.title("Resource Management: Industrial Workforce Dashboard")

# Load dataset
file_path = "final_cleaned_industrial_data.csv"
df = load_data(file_path)

if df.empty:
    st.stop()

# Add engineered features
df = add_features(df)

# Show basic info
st.subheader("Dataset Overview")
st.write(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
st.dataframe(df.head(10))

# Show key visualizations
st.subheader("Sector-wise Workforce Distribution (Bar Polar)")
st.plotly_chart(bar_polar_sector(df), use_container_width=True)

st.subheader("State → District → Sector (Sunburst)")
st.plotly_chart(sunburst_state_district_sector(df), use_container_width=True)

st.subheader("Rural vs Urban Workforce (Stacked Bar)")
st.plotly_chart(stacked_rural_urban(df), use_container_width=True)

st.subheader("Geospatial Workforce Map")
geo_fig = geospatial_map(df)
if geo_fig:
    st.plotly_chart(geo_fig, use_container_width=True)

# Insights Section
st.subheader("Quick Insights")
top_sectors = df.groupby('industrial_sector')['total_workforce'].sum().sort_values(ascending=False).head(5)
st.write("Top 5 sectors by workforce size:")
st.dataframe(top_sectors)

top_districts = df.groupby(['state_name', 'district_name'])['total_workforce'].sum().sort_values(ascending=False).head(10)
st.write("Top 10 districts by workforce size:")
st.dataframe(top_districts)

st.write("Rural vs Urban workforce ratio (sample):")
st.dataframe(df[['state_name', 'district_name', 'industrial_sector', 'rural_urban_ratio']].head(10))
