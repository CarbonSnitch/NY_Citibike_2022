import os
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.io as pio
import matplotlib.pyplot as plt
from datetime import datetime as dt
from streamlit_keplergl import keplergl_static
from IPython.display import HTML, display
from IPython.display import IFrame

############################################ Settings for Dashboard #####################################################

st.set_page_config(page_title = 'Citibike Strategy Dashboard - NY 2022', layout='wide')
st.title("Citibike Strategy Dashboard")
st.markdown("The dashboard will help with the distribution and seasonal trends of bike-rental")
st.markdown("Citibike has been gaining popularity in New York since 2013. This has led to distribution problems such as fewer bikes in popular stations or bikes congregated in areas that are not popular.")

########################## Import data ###########################################################################################

path = r"C:\Users\ryani\Desktop\JupyterLab\NY_Citibike_2022"
df = pd.read_csv(os.path.join(path, '02_Prepared_Data', 'sampled_24mb.csv'), index_col = 0)
top20 = pd.read_csv(os.path.join(path, '02_Prepared_Data', 'top20.csv'), index_col = 0)
df_top = pd.read_csv(os.path.join(path, '02_Prepared_Data', 'sampled_top_trips.csv'), index_col = 0)

# ######################################### DEFINE THE CHARTS #####################################################################

## Bar chart
                    
fig = go.Figure(go.Bar(
    x=top20['start_station_name'],
    y=top20['value'],
    marker=dict(
        color=top20['value'],
        colorscale=[
            [0, 'rgb(0,128,128)'],   # Teal
            [1, 'rgb(0,255,255)']    # Aqua
        ],
        colorbar=dict(title='Trips')
    )
))

fig.update_layout(
    title='Top 20 most popular bike stations in NY 2022',
    title_font=dict(size=24),
    xaxis_title='Start stations',
    yaxis_title='Sum of trips',
    width=900,
    height=600)
fig.update_xaxes(tickfont=dict(size=10))
st.plotly_chart(fig, use_container_width=True)


################################################## Line Chart ############################################################################


daily = (
    df
    .groupby('date')
    .agg(
        trips_per_day=('trips_per_day', 'sum'),
        avgtemp=('avgtemp', 'mean')
    )
    .reset_index()
    .sort_values('date')
)

# 3. Build subplot with secondary y-axis
fig_2 = make_subplots(specs=[[{"secondary_y": True}]])

# 4. Trace: daily trips on primary y-axis
fig_2.add_trace(
    go.Scatter(
        x=daily['date'],
        y=daily['trips_per_day'],
        mode='lines+markers',
        name='Daily Trips',
        line=dict(color='teal'),
        hovertemplate='%{x|%Y-%m-%d}<br>Trips: %{y}<extra></extra>'
    ),
    secondary_y=False
)

# 5. Trace: avg temp on secondary y-axis
fig_2.add_trace(
    go.Scatter(
        x=daily['date'],
        y=daily['avgtemp'],
        mode='lines+markers',
        name='Avg Temp (°C)',
        line=dict(color='orange'),
        hovertemplate='%{x|%Y-%m-%d}<br>Temp: %{y:.1f}°C<extra></extra>'
    ),
    secondary_y=True
)

# 6. Update axes and layout
fig_2.update_xaxes(
    title_text="Date",
    tickformat="%b %d\n%Y",
    showgrid=False,
    rangeslider_visible=False
)

fig_2.update_yaxes(
    title_text="Number of Trips",
    secondary_y=False,
    showgrid=True,
    gridcolor='lightgray'
)
fig_2.update_yaxes(
    title_text="Average Temperature (°C)",
    secondary_y=True,
    showgrid=False
)

fig_2.update_layout(
    title="Daily Bike Trips vs. Daily Average Temperature",
    title_font=dict(size=24),
    legend=dict(x=0.02, y=0.98),
    margin=dict(l=50, r=50, t=80, b=50),
    template="plotly_white"
)

# 7. Render
st.plotly_chart(fig_2, use_container_width=True)  # for Streamlit


###################################Add the map #########################################################################################

### Add the map ###

path_to_html = r"C:\Users\ryani\Desktop\JupyterLab\NY_Citibike_2022\04_Visualisations\NY_Citibike_2022.html"

# Read file and keep in variable
with open(path_to_html, 'r', encoding='utf-8-sig') as f:
    html_data = f.read()

## Show in webpage
st.header("Most Popular Bike-Rental Trips and start/end station in NY 2022")
st.components.v1.html(html_data,height=2000)
