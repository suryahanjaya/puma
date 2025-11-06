import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("data/telemetry_with_anomaly.csv")

st.set_page_config(page_title="UAV DID 3.11 BLOS Dashboard", layout="wide")
st.title("UAV DID 3.11 BLOS — Advanced Flight Monitoring Dashboard")

# Sidebar filters
st.sidebar.header("Filters")
# Convert integer seconds to human-readable datetime anchored to today for display
base_day = pd.Timestamp.today().normalize()
df['dt'] = pd.to_datetime(df['timestamp'], unit='s', origin=base_day)

start_time, end_time = st.sidebar.slider(
    "Select Time Range",
    min_value=df['dt'].min().to_pydatetime(),
    max_value=df['dt'].max().to_pydatetime(),
    value=(df['dt'].min().to_pydatetime(), df['dt'].max().to_pydatetime()),
    format="HH:mm:ss"
)
show_anomalies = st.sidebar.checkbox("Show only anomalies", value=False)

df_filtered = df[(df['dt'] >= start_time) & (df['dt'] <= end_time)]
if show_anomalies:
    df_filtered = df_filtered[df_filtered['anomaly'] == -1]

# KPI / Performance Metrics
st.subheader("Flight Performance Metrics")
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Average Altitude (m)", f"{df_filtered['altitude'].mean():.2f}", "Altitude")
col2.metric("Average Speed (km/h)", f"{df_filtered['speed'].mean():.2f}", "Speed")
col3.metric("Average Battery (%)", f"{df_filtered['battery_level'].mean():.2f}", "Battery")
col4.metric("Anomaly Count", f"{(df_filtered['anomaly']==-1).sum()}", "Anomalies")
col5.metric("Data Points", f"{len(df_filtered)}", "Total Points")

# Graphs: Line chart and Scatter chart
st.subheader("Altitude & Speed Trends")
fig_line = px.line(
    df_filtered,
    x="dt",
    y=["altitude", "speed"],
    labels={"value":"Measurement", "dt":"Time"},
    title="Altitude & Speed over Time"
)
st.plotly_chart(fig_line, width="stretch")

st.subheader("Battery Level & Anomalies")
df_filtered["status"] = df_filtered['anomaly'].map({1:"Normal",-1:"Anomaly"})
fig_scatter = px.scatter(
    df_filtered,
    x="dt",
    y="battery_level",
    color="status",
    color_discrete_map={"Normal":"green","Anomaly":"red"},
    hover_data=["altitude","speed"],
    title="Battery Level with Anomaly Highlight"
)
st.plotly_chart(fig_scatter, width="stretch")

# Flight Map
st.subheader("Flight Path Map with Anomalies")
fig_map = px.scatter_map(
    df_filtered,
    lat="gps_lat",
    lon="gps_lon",
    color="status",
    color_discrete_map={"Normal":"blue","Anomaly":"red"},
    hover_data=["altitude","speed","battery_level"],
    zoom=13,
    height=500
)
fig_map.update_layout(mapbox_style="open-street-map")
st.plotly_chart(fig_map, width="stretch")

# Optional: Download filtered data
st.subheader("Download Filtered Data")
st.download_button(
    label="Download CSV",
    data=df_filtered.to_csv(index=False).encode('utf-8'),
    file_name='telemetry_filtered.csv',
    mime='text/csv'
)
