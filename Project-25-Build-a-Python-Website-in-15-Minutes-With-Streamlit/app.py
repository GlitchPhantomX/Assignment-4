import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import BytesIO
import base64

# Set page configuration
st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

# Custom CSS for responsive design
st.markdown(
    """
    <style>
    /* Improve padding and font size for mobile devices */
    @media (max-width: 600px) {
        .stMetric {
            padding: 10px !important;
        }
        .stMetric label {
            font-size: 14px !important;
        }
        .stMetric value {
            font-size: 18px !important;
        }
        .stButton button {
            width: 100% !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header: Dashboard name and logo
st.title("📊 Dashboard Name")

# Key Metrics (KPIs) at the top of the dashboard
st.subheader("Key Metrics (KPIs)")

# Create columns to display KPIs side by side
col1, col2, col3, col4 = st.columns(4)

# Example KPI data (replace with actual data)
total_sales = 150000
average_revenue = 50000
number_of_orders = 1200
customer_growth_rate = "8.5%"

# Display KPIs
with col1:
    st.metric(label="Total Sales", value=f"${total_sales:,}")

with col2:
    st.metric(label="Average Revenue", value=f"${average_revenue:,}")

with col3:
    st.metric(label="Number of Orders", value=f"{number_of_orders:,}")

with col4:
    st.metric(label="Customer Growth Rate", value=customer_growth_rate)

# Sidebar: Filters and options
with st.sidebar:
    st.header("Filters")

    # Date range picker
    st.subheader("Date Range")
    date_range = st.date_input("Select date range", [pd.to_datetime("2023-01-01"), pd.to_datetime("2023-12-31")])

    # Dropdown for categories
    st.subheader("Category Filter")
    category_options = ["All", "Category A", "Category B", "Category C"]
    selected_category = st.selectbox("Select a category", category_options)

    # Dropdown for regions
    st.subheader("Region Filter")
    region_options = ["All", "Region 1", "Region 2", "Region 3"]
    selected_region = st.selectbox("Select a region", region_options)

    # Slider for numerical range
    st.subheader("Numerical Range Filter")
    numerical_range = st.slider("Select a numerical range", 0, 100, (25, 75))

    st.write("Adjust the filters to customize the data.")

# Sections: Data divided into sections
st.header("Overview")
st.write("This section provides a high-level overview of the data.")
# Example data for overview
overview_data = pd.DataFrame({
    "Metric": ["Total Users", "Active Users", "Revenue"],
    "Value": [1000, 750, 50000]
})
st.table(overview_data)

# Data Visualizations
st.header("Data Visualizations")

# Line Chart (for trends over time)
st.subheader("Line Chart: Trends Over Time")
trends_data = pd.DataFrame({
    "Date": pd.date_range(start="2023-01-01", end="2023-12-31", freq="M"),
    "Value": np.random.randint(100, 1000, size=12)
})
# Apply date range filter to trends data
filtered_trends_data = trends_data[
    (trends_data["Date"] >= pd.to_datetime(date_range[0])) &
    (trends_data["Date"] <= pd.to_datetime(date_range[1]))
]
st.line_chart(filtered_trends_data.set_index("Date"))

# Bar Chart (for comparisons)
st.subheader("Bar Chart: Category Comparison")
bar_chart_data = pd.DataFrame({
    "Category": ["Category A", "Category B", "Category C", "Category D"],
    "Value": [25, 50, 75, 100]
})
# Apply category filter to bar chart data
if selected_category != "All":
    bar_chart_data = bar_chart_data[bar_chart_data["Category"] == selected_category]
st.bar_chart(bar_chart_data.set_index("Category"))

# Pie Chart (for proportions)
st.subheader("Pie Chart: Proportion of Categories")
pie_chart_data = pd.DataFrame({
    "Category": ["Category A", "Category B", "Category C", "Category D"],
    "Value": [25, 50, 75, 100]
})
# Apply category filter to pie chart data
if selected_category != "All":
    pie_chart_data = pie_chart_data[pie_chart_data["Category"] == selected_category]
fig_pie = px.pie(pie_chart_data, values="Value", names="Category", title="Proportion of Categories")
st.plotly_chart(fig_pie)

# Map (for geographical data)
st.subheader("Map: Geographical Data")
map_data = pd.DataFrame({
    "City": ["New York", "Los Angeles", "Chicago", "Houston"],
    "Lat": [40.7128, 34.0522, 41.8781, 29.7604],
    "Lon": [-74.0060, -118.2437, -87.6298, -95.3698],
    "Value": [100, 200, 150, 300]
})
# Apply region filter to map data
if selected_region != "All":
    map_data = map_data[map_data["City"] == selected_region]
st.map(map_data)

# Data Export Options
st.header("Data Export Options")

# Download data as CSV/Excel
st.subheader("Download Data")
if st.button("Download Overview Data as CSV"):
    csv = overview_data.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="overview_data.csv">Download CSV</a>'
    st.markdown(href, unsafe_allow_html=True)

if st.button("Download Trends Data as Excel"):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        trends_data.to_excel(writer, index=False)
    b64 = base64.b64encode(output.getvalue()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="trends_data.xlsx">Download Excel</a>'
    st.markdown(href, unsafe_allow_html=True)

# Export charts as images or PDF
st.subheader("Export Charts")
if st.button("Export Line Chart as Image"):
    fig_line = px.line(filtered_trends_data, x="Date", y="Value", title="Trends Over Time")
    img_bytes = fig_line.to_image(format="png")
    st.download_button(label="Download Line Chart as PNG", data=img_bytes, file_name="line_chart.png", mime="image/png")

if st.button("Export Pie Chart as PDF"):
    fig_pie.write_image("pie_chart.pdf")
    with open("pie_chart.pdf", "rb") as file:
        btn = st.download_button(label="Download Pie Chart as PDF", data=file, file_name="pie_chart.pdf", mime="application/pdf")

# Insights Section
st.header("Insights")
st.write("This section provides insights and analysis.")
# Example data for insights
insights_data = pd.DataFrame({
    "Category": ["Category A", "Category B", "Category C", "Category D"],
    "Region": ["Region 1", "Region 2", "Region 3", "Region 1"],
    "Value": [25, 50, 75, 100]
})
# Apply category and region filters to insights data
if selected_category != "All":
    insights_data = insights_data[insights_data["Category"] == selected_category]
if selected_region != "All":
    insights_data = insights_data[insights_data["Region"] == selected_region]
st.bar_chart(insights_data.set_index("Category"))

# Whitespace: Content is spaced out to avoid clutter
st.write("")  # Adds an empty line for spacing
st.write("")  # Adds another empty line for spacing
st.write("Thank you for using the dashboard!")