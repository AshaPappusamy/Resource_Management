# Resource_Management
End-to-end data science project analyzing India's industrial workforce dataset with data preprocessing, NLP-based industry grouping, and interactive visualizations using Streamlit and Plotly.
# Resource Management Dashboard – India Industrial Workforce (2011)

## Project Overview

This project analyzes India's industrial workforce distribution using **Census 2011 industrial employment data**.
The goal is to understand workforce patterns across **states, districts, sectors, gender, and rural/urban divisions** and present them through an interactive **data storytelling dashboard**.

The project transforms raw census datasets into meaningful insights that can support **policy planning, industrial development, and workforce management strategies**.

---

## Business Problem

India's workforce is distributed unevenly across regions and sectors.
Without proper analysis, it is difficult for policymakers and organizations to identify:

* Which states have the highest workforce concentration
* Which industries generate the most employment
* Regional disparities in employment opportunities
* Gender imbalance in workforce participation
* Rural vs Urban employment distribution

This project builds a **data-driven dashboard** to answer these questions.

---

## Project Objectives

The main objectives of this project are:

1. Clean and transform raw census industrial workforce data
2. Structure the dataset for efficient analysis
3. Explore workforce distribution across industries and states
4. Analyze gender and rural/urban workforce patterns
5. Build an **interactive Streamlit dashboard** for visual insights
6. Provide **policy and business recommendations based on the analysis**

---

## Dataset

Dataset Source: **Indian Census 2011 – Industrial Workforce Data**

The dataset contains information such as:

* State and district names
* Industrial sector classification
* Total workers
* Main workers
* Marginal workers
* Male and female workforce
* Rural and urban workforce distribution

---

## Project Workflow

The project follows a structured data science pipeline.

### 1 Data Collection

Raw CSV files containing workforce data were collected from the Census dataset.

### 2 Data Cleaning

Data preprocessing steps included:

* Removing irrelevant columns
* Renaming columns for readability
* Handling missing values
* Standardizing state and district names
* Aggregating workforce metrics

Libraries used:

* pandas
* numpy

---

### 3 Data Transformation

The cleaned dataset was structured to support visualization and analysis:

* Total workforce calculation
* Rural vs Urban workforce aggregation
* Gender workforce distribution
* Industrial sector grouping

---

### 4 Exploratory Data Analysis

Key insights explored:

* Workforce distribution by state
* Industrial sector employment patterns
* Gender workforce imbalance
* Regional workforce concentration

Visualization libraries used:

* Plotly
* Matplotlib

---

### 5 Dashboard Development

An interactive dashboard was developed using **Streamlit**.

Features include:

* Interactive filters for states and districts
* Dynamic charts and hierarchical visualizations
* Workforce analysis by sector, gender, and geography
* Story-driven insights for better interpretation

---

## Dashboard Features

The dashboard includes the following analytical sections:

### Workforce Overview

Shows total workforce distribution and employment stability across regions.
<img width="1503" height="840" alt="Screenshot 2026-03-28 140411" src="https://github.com/user-attachments/assets/cb7c47a3-d369-40a5-bb5d-fe69a5f8feef" />

### Industrial Structure

Visualizes employment distribution across macro and industrial sectors.
<img width="1518" height="797" alt="image" src="https://github.com/user-attachments/assets/f8baf1fd-ee1d-4f9e-8162-f744b938b80b" />

### Regional Workforce Distribution

Highlights workforce concentration across states and districts.
<img width="1407" height="758" alt="image" src="https://github.com/user-attachments/assets/e5d1a6db-b27c-4c4b-b77a-15a0a8a0f692" />

### Gender Workforce Analysis

Analyzes participation differences between male and female workers.
<img width="1103" height="777" alt="image" src="https://github.com/user-attachments/assets/3f71c5c8-2341-4b53-873e-a2e1002f8a9f" />

### Strategic Insights

Provides policy recommendations derived from the data.

---

## Technologies Used

Python
Pandas
Plotly
Streamlit
GitHub

---

## Project Structure

```
Resource_Management
│
├── data
│   ├── raw
│   └── processed
│
├── notebooks
│   └── data_cleaning.ipynb
│
├── dashboard
│   └── app.py
│
├── README.md
│
└── requirements.txt
```

---

## How to Run the Project

### Step 1 Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/Resource_Management.git
```

### Step 2 Navigate to Project Folder

```bash
cd Resource_Management
```

### Step 3 Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4 Run the Dashboard

```bash
streamlit run app.py
```

The dashboard will open in your browser.

---

## Key Insights

* Workforce is concentrated in a few major industrial states.
* Some districts show strong industrial employment clusters.
* Female workforce participation is significantly lower than male participation.
* Rural workforce dominates certain industrial sectors.

---

## Business Recommendations

Based on the analysis:

* Encourage industrial investments in underdeveloped regions.
* Promote women skill development programs to increase workforce participation.
* Improve rural industrial infrastructure to generate employment.
* Support emerging industries to diversify job creation.

---

## Future Improvements

* Add geospatial workforce maps
* Integrate additional census datasets
* Include predictive workforce modeling
* Deploy dashboard on Streamlit Cloud

---

## Author

Asha P

Data Science Student

---

## License

This project is intended for educational and analytical purposes.
