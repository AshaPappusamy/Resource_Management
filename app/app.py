# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# 1. Load CSV Function
# -----------------------------
@st.cache_data
def load_csv(file_path):
    """
    Load cleaned CSV and cache for Streamlit
    """
    df = pd.read_csv(file_path)
    
    # Optional: create % columns for quick stats
    df['total_workers_persons'] = df['main_workers_-_total_-_persons'] + df['marginal_workers_-_total_-_persons']
    df['rural_percent'] = round(df['main_workers_-_rural_-_persons'] / df['total_workers_persons'] * 100, 2)
    df['urban_percent'] = round(df['main_workers_-_urban_-_persons'] / df['total_workers_persons'] * 100, 2)
    
    return df

# -----------------------------
# 2. Filters Function
# -----------------------------
def filter_data(df):
    st.sidebar.header("Filters")
    selected_state = st.sidebar.selectbox("Select State", ["All"] + df['state_name'].unique().tolist())
    selected_sector = st.sidebar.selectbox("Select Industrial Sector", ["All"] + df['industrial_sector'].unique().tolist())
    
    filtered_df = df.copy()
    if selected_state != "All":
        filtered_df = filtered_df[filtered_df['state_name'] == selected_state]
    if selected_sector != "All":
        filtered_df = filtered_df[filtered_df['industrial_sector'] == selected_sector]
    
    return filtered_df

# -----------------------------
# 3. Visualizations Function
# -----------------------------
def visualize_data(df):
    st.subheader("1️⃣ Bar Polar: Workforce by Industrial Sector")
    sector_sum = df.groupby('industrial_sector')['total_workers_persons'].sum().reset_index()
    fig_barpolar = px.bar_polar(sector_sum, r='total_workers_persons', theta='industrial_sector',
                                color='industrial_sector', template='plotly_dark',
                                title="Total Workforce by Industrial Sector")
    st.plotly_chart(fig_barpolar, use_container_width=True)
    
    st.subheader("2️⃣ Sunburst: State > District > Industrial Sector")
    fig_sunburst = px.sunburst(df, path=['state_name', 'district_name', 'industrial_sector'],
                               values='total_workers_persons',
                               color='total_workers_persons',
                               color_continuous_scale='Viridis',
                               title="Workforce Distribution by State/District/Sector")
    st.plotly_chart(fig_sunburst, use_container_width=True)
    
    st.subheader("3️⃣ Map: District-level Workforce")
    # Map requires 'latitude' and 'longitude' columns
    if 'latitude' in df.columns and 'longitude' in df.columns:
        fig_map = px.scatter_mapbox(df, lat='latitude', lon='longitude',
                                    size='total_workers_persons',
                                    color='industrial_sector',
                                    hover_name='district_name',
                                    zoom=4,
                                    mapbox_style='carto-positron',
                                    title="District-wise Workforce Distribution")
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.warning("Latitude and longitude columns not found. Map skipped.")

# -----------------------------
# 4. Main App
# -----------------------------
def main():
    st.title("Industrial Workforce Dashboard")
    
    # Load dataset
    df = load_csv("final_cleaned_industrial_data.csv")
    
    # Sidebar Filters
    filtered_df = filter_data(df)
    
    # Show filtered dataframe
    st.subheader("Filtered Data Preview")
    st.dataframe(filtered_df.head(10))
    
    # Visualizations
    visualize_data(filtered_df)
    
if __name__ == "__main__":
    main()                            
