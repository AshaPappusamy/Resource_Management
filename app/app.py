# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Load CSV (from main folder)
# -----------------------------
@st.cache_data
def load_csv(file_path="final_cleaned_industrial_data.csv"):
    df = pd.read_csv(file_path)
    # Total workforce
    df['total_workers_persons'] = df['main_workers_-_total_-_persons'] + df['marginal_workers_-_total_-_persons']
    # Rural / Urban percentages
    df['rural_percent'] = round(df['main_workers_-_rural_-_persons'] / df['total_workers_persons'] * 100, 2)
    df['urban_percent'] = round(df['main_workers_-_urban_-_persons'] / df['total_workers_persons'] * 100, 2)
    return df

# -----------------------------
# Sidebar Filters
# -----------------------------
def filter_data(df):
    st.sidebar.header("Filters")
    
    selected_state = st.sidebar.selectbox("State", ["All"] + df['state_name'].unique().tolist())
    selected_sector = st.sidebar.selectbox("Industrial Sector", ["All"] + df['industrial_sector'].unique().tolist())
    
    rural_slider = st.sidebar.slider("Min % Rural Workers", 0, 100, 0)
    urban_slider = st.sidebar.slider("Min % Urban Workers", 0, 100, 0)
    
    filtered = df.copy()
    if selected_state != "All":
        filtered = filtered[filtered['state_name'] == selected_state]
    if selected_sector != "All":
        filtered = filtered[filtered['industrial_sector'] == selected_sector]
    filtered = filtered[(filtered['rural_percent'] >= rural_slider) & (filtered['urban_percent'] >= urban_slider)]
    
    return filtered

# -----------------------------
# Visualizations
# -----------------------------
def visualize_data(df):
    st.subheader("📊 Total Workforce by Industrial Sector")
    sector_sum = df.groupby('industrial_sector')['total_workers_persons'].sum().reset_index()
    fig1 = px.bar_polar(
        sector_sum, 
        r='total_workers_persons', 
        theta='industrial_sector',
        color='industrial_sector', 
        template='plotly_dark'
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("🌞 Workforce Distribution: State → District → Sector")
    fig2 = px.sunburst(
        df, 
        path=['state_name','district_name','industrial_sector'],
        values='total_workers_persons', 
        color='total_workers_persons',
        color_continuous_scale='Viridis'
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("🗺️ District Map (Workforce Size)")
    if 'latitude' in df.columns and 'longitude' in df.columns:
        fig3 = px.scatter_mapbox(
            df, 
            lat='latitude', 
            lon='longitude',
            size='total_workers_persons', 
            color='industrial_sector',
            hover_name='district_name', 
            zoom=4,
            mapbox_style='carto-positron'
        )
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("Map requires latitude & longitude columns to display districts.")

# -----------------------------
# Basic Checks / Metrics
# -----------------------------
def show_metrics(df):
    st.subheader("Filtered Data Preview")
    st.dataframe(df.head(10))
    
    st.metric("Total Workforce", f"{df['total_workers_persons'].sum():,}")
    st.metric("Average Rural %", f"{df['rural_percent'].mean():.2f}%")
    st.metric("Average Urban %", f"{df['urban_percent'].mean():.2f}%")

# -----------------------------
# Main App
# -----------------------------
def main():
    st.title("Industrial Workforce Dashboard")
    
    df = load_csv()
    filtered_df = filter_data(df)
    
    show_metrics(filtered_df)
    visualize_data(filtered_df)

if __name__ == "__main__":
    main()
