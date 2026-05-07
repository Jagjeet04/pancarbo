
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="Pancarbo AI Dashboard",
    layout="wide"
)

st.title("Pancarbo Greenfuels Industrial AI Dashboard")

sensor_df = pd.DataFrame({
    "Time": range(50),
    "Temperature": np.random.uniform(100, 300, 50),
    "Steam_Output": np.random.uniform(10, 100, 50),
    "Oxygen": np.random.uniform(1, 10, 50)
})

fig = px.line(
    sensor_df,
    x="Time",
    y=["Temperature", "Steam_Output", "Oxygen"],
    title="Real-Time Industrial Sensors"
)

st.plotly_chart(fig, use_container_width=True)

st.success("Dashboard Running Successfully")
