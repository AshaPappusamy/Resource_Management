# -----------------------------
# Load CSV (updated path for main folder)
# -----------------------------
@st.cache_data
def load_csv(file_path="final_cleaned_industrial_data.csv"):
    df = pd.read_csv(file_path)
    df['total_workers_persons'] = df['main_workers_-_total_-_persons'] + df['marginal_workers_-_total_-_persons']
    df['rural_percent'] = round(df['main_workers_-_rural_-_persons'] / df['total_workers_persons'] * 100, 2)
    df['urban_percent'] = round(df['main_workers_-_urban_-_persons'] / df['total_workers_persons'] * 100, 2)
    return df
