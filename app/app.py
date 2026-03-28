import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------

st.set_page_config(
    page_title="Resource Management India - 2011",
    layout="wide"
)

# -------------------------------------------------
# STYLE
# -------------------------------------------------

st.markdown("""
<style>

.stApp{
background: linear-gradient(120deg,#eef2f7,#e2e8f0);
}

.chart-card{
background:white;
padding:25px;
border-radius:18px;
box-shadow:0px 10px 30px rgba(0,0,0,0.12);
margin-bottom:30px;
}

[data-testid="stSidebar"]{
background:linear-gradient(#1d3557,#457b9d);
}

[data-testid="stSidebar"] *{
color:white;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("final_cleaned_industrial_data.csv")
    df.columns = df.columns.str.strip().str.lower()
    return df

df = load_data()

# -------------------------------------------------
# TITLE
# -------------------------------------------------

st.title("Resource Management India - 2011")
st.caption("Industrial Workforce Data Story | Based on Census 2011")

# -------------------------------------------------
# SIDEBAR FILTERS
# -------------------------------------------------

st.sidebar.header("Filters")

states = ["All States"] + sorted(df["state_name"].dropna().unique())
state = st.sidebar.selectbox("Select State", states)

filtered_df = df.copy()

if state != "All States":
    filtered_df = filtered_df[filtered_df["state_name"] == state]

districts = ["All Districts"] + sorted(filtered_df["district_name"].dropna().unique())
district = st.sidebar.selectbox("Select District", districts)

if district != "All Districts":
    filtered_df = filtered_df[filtered_df["district_name"] == district]

# -------------------------------------------------
# DASHBOARD STORY NAVIGATION
# -------------------------------------------------

section = st.sidebar.radio(

"Dashboard Story",

[
"Workforce Overview",
"Industrial Structure",
"Regional Workforce",
"Gender Workforce",
"Strategic Insights"
]

)

# -------------------------------------------------
# SECTION 1
# WORKFORCE OVERVIEW
# -------------------------------------------------

if section == "Workforce Overview":

    st.header("1️⃣ Workforce Overview")

    st.markdown("""
**Business Question**

How large is India's industrial workforce and how stable are employment patterns?
""")

    total = int(filtered_df["total_workers"].sum())
    main = int(filtered_df["main_total"].sum())
    marginal = int(filtered_df["marginal_total"].sum())

    c1,c2,c3 = st.columns(3)

    c1.metric("Total Workforce", f"{total:,}")
    c2.metric("Main Workers", f"{main:,}")
    c3.metric("Marginal Workers", f"{marginal:,}")

    st.divider()

    state_data = (
        filtered_df.groupby("state_name")[["main_total","marginal_total"]]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        state_data,
        x="state_name",
        y=["main_total","marginal_total"],
        barmode="stack",
        color_discrete_sequence=px.colors.qualitative.Bold
    )

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig,use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    top_states = (
        filtered_df.groupby("state_name")["total_workers"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )

    st.markdown("### Top Workforce States")

    st.write(top_states)

    st.info("""
Key Insight

Industrial employment is heavily concentrated in a few states.

Recommendation

Encourage industrial expansion in emerging states to balance workforce distribution.
""")

# -------------------------------------------------
# SECTION 2
# INDUSTRIAL STRUCTURE
# -------------------------------------------------

elif section == "Industrial Structure":

    st.header("2️⃣ Industrial Workforce Structure")

    st.markdown("""
**Business Question**

Which industrial sectors generate the highest employment?
""")

    sector_data = (
        filtered_df.groupby(["macro_sector","industry_sector"])
        ["total_workers"]
        .sum()
        .reset_index()
    )

    fig = px.sunburst(
        sector_data,
        path=["macro_sector","industry_sector"],
        values="total_workers",
        color="macro_sector"
    )

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig,use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.info("""
Key Insight

A few industries dominate employment generation.

Business Strategy

Encourage investments in emerging industries to diversify job creation.
""")

# -------------------------------------------------
# SECTION 3
# REGIONAL WORKFORCE
# -------------------------------------------------

elif section == "Regional Workforce":

    st.header("3️⃣ Regional Workforce Distribution")

    st.markdown("""
**Business Question**

Where are industrial workers geographically concentrated?
""")

    industry_dist = (
        filtered_df.groupby(
            ["state_name","district_name","industry_sector"]
        )["total_workers"]
        .sum()
        .reset_index()
    )

    fig = px.treemap(
        industry_dist,
        path=["state_name","district_name","industry_sector"],
        values="total_workers",
        color="total_workers",
        color_continuous_scale="Sunset"
    )

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig,use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.info("""
Key Insight

Industrial workforce clusters are concentrated in specific districts.

Policy Recommendation

Develop industrial corridors and infrastructure in low-employment regions.
""")

# -------------------------------------------------
# SECTION 4
# GENDER WORKFORCE
# -------------------------------------------------

elif section == "Gender Workforce":

    st.header("4️⃣ Gender Workforce Analysis")

    st.markdown("""
**Business Question**

How balanced is workforce participation between male and female workers?
""")

    gender_data = pd.DataFrame({

        "Gender":[
        "Male","Male","Female","Female"
        ],

        "Location":[
        "Rural Male",
        "Urban Male",
        "Rural Female",
        "Urban Female"
        ],

        "Workers":[
        filtered_df["main_rural_males"].sum(),
        filtered_df["main_urban_males"].sum(),
        filtered_df["main_rural_females"].sum(),
        filtered_df["main_urban_females"].sum()
        ]

    })

    fig = px.sunburst(
        gender_data,
        path=["Gender","Location"],
        values="Workers",
        color="Gender"
    )

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig,use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.info("""
Key Insight

Female workforce participation remains significantly lower than male participation.

Business Recommendation

Promote women skill training programs and safe workplace policies to increase female workforce engagement.
""")

# -------------------------------------------------
# SECTION 5
# STRATEGIC INSIGHTS
# -------------------------------------------------

elif section == "Strategic Insights":

    st.header("5️⃣ Strategic Insights")

    st.markdown("""
### Policy Recommendations

1️⃣ Expand industrial development in emerging states  

2️⃣ Encourage sector diversification  

3️⃣ Improve female workforce participation  

4️⃣ Invest in rural industrial clusters  

5️⃣ Strengthen infrastructure for balanced regional growth
""")