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
from PIL import Image

########################### Initial settings for the dashboard ####################################################


st.set_page_config(page_title = 'Citibike NY Bikes Strategy Dashboard', layout='wide')
st.title("Citibike NY Bikes Strategy Dashboard")
st.markdown("The dashboard will help with the distribution and seasonal trends of bike-rental to give insights into seasonal trends and optimal bike-distribution")
st.markdown("Citibike has been gaining popularity in New York since 2013. This has led to distribution problems such as fewer bikes in popular stations or bikes congregated in areas that are not popular. This analysis has been broken down into four sections")

# Define side bar
st.sidebar.title("Aspect Selector")
page = st.sidebar.selectbox('Select an aspect of the analysis',
  ["Intro page","Weather component and bike usage",
   "Most popular stations",
    "Interactive map with aggregated bike trips", "Recommendations"])


########################## Import data ###########################################################################################

path = r"C:\Users\ryani\Desktop\JupyterLab\NY_Citibike_2022"
df = pd.read_csv(os.path.join(path, '02_Prepared_Data', 'sampled_24mb.csv'), index_col = 0)
top20 = pd.read_csv(os.path.join(path, '02_Prepared_Data', 'top20.csv'), index_col = 0)
df_top = pd.read_csv(os.path.join(path, '02_Prepared_Data', 'sampled_top_trips.csv'), index_col = 0)

######################################### DEFINE THE PAGES #####################################################################


### Intro page

if page == "Intro page":
    st.markdown("#### This dashboard aims at providing helpful insights on the expansion problems Citibike currently faces.")
    st.markdown("Right now, Citibike runs into a situation where customers complain about bikes not being available at certain times. This analysis will look at the potential reasons behind this. The dashboard is separated into 4 sections:")
    st.markdown("- Most popular stations")
    st.markdown("- Weather component and bike usage")
    st.markdown("- Interactive map with aggregated bike trips")
    st.markdown("- Recommendations")
    st.markdown("The dropdown menu on the left 'Aspect Selector' will take you to the different aspects of the analysis.")

    myImage = Image.open("BIKEIMAGE.png") #source: https://perchance.org/ai-text-to-image-generator
    st.image(myImage)


# ######################################### DEFINE THE CHARTS #####################################################################

elif page == 'Most popular stations':

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

    st.markdown("These stations are the most-used bike stations by citibike customers. The top Three consist of 'W 21 & 6 Ave', 'W St & Chambers St', and 'Broadway & W 58 St'. A full interactive map of the most popular stations and trips can be accessed in the interactive map, accessible throught the 'Aspect Selector'")
    
################################################## Line Chart ############################################################################

elif page == 'Weather component and bike usage':
    
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

    st.markdown("There are two main points which this analyses reveals about Citibike and its customers:")
    st.markdown(" - The amount of rentals are affected by the time of year. There is a peak in rentals around May which continues to be elevated until around November.")
    st.markdown(" - The peak in rentals is accompanied by a peak in average temperature. While this does not neccessarily mean that increaed temperatures will definately yield increased rentals, the correlation is noticeable.")  
       
################################### Add the map ##################################
elif page == 'Interactive map with aggregated bike trips':
                
    st.write("Interactive map showing most popular stations and Citibike bike-trips in NY 2022")

    path_to_html = "NY_Citibike_2022_top.html" 

    # Read file and keep in variabl
    with open('NY_Citibike_2022_top.html', 'r', encoding='utf-8') as f:
        html_data = f.read()


    ## Show in webpage
    st.header("Aggregated Bike Trips in NY 2022")
    st.components.v1.html(html_data,height=1000)
    st.markdown("# Zooming into the map by scrolling we can see where bikes are being rented-from and deposited-to")
    st.markdown("Of particular note are the bike trips which are rented from an area of heavy-use and then deposited to an area of low-use. These stations will be deemed **Build-up stations** and include:")
    st.markdown(" -**W 22 & 8 Ave**")
    st.markdown(" -**1 Ave & E 68 St**")
    st.markdown(" -**S 4 St & Wythe Ave**")
    st.markdown(" -**Pier 40 - Hudson River Park**")

else:
    
    st.header("Conclusions and recommendations")
    bikes = Image.open("BIKEIMAGE.png")  #source: https://perchance.org/ai-text-to-image-generator
    st.image(bikes)
    st.markdown("### Our analysis has shown that Citibike should focus on the following objectives moving forward to address customer complaints about lack of rental bikes available:")
    st.markdown("- Be prepared for heavier bike-rental usage starting in May and going up until mid-November. If warmer temperatures are happeneing outside these months then heavier bike-usage may also happen")
    st.markdown("- Ensure that bike build-up is prevented as much as possible. This should focus on moving bikes from areas of low-rental/high drop-off to areas of high-rental. Stations to which bikes should be picked-up and droppoed-off can be seen in the table below. ")

    def main():
        st.set_page_config(page_title="Citibike Station Pairing", layout="wide")
    st.title("Citibike Station Pairing")

    # 1. Define your paired stations
    data = {
        "Stations to deposit bikes": [
            "West St & Chambers St",
            "W 21 St & 6 Ave",
            "E 33 St & 1 Ave",
            "W 31 St & 7 Ave",
            "Broadway & E 21 St",
            "University Pl & E 14 St",
            "Broadway & W 23 St",
            "Broadway & E 14 St",
            "1 Ave & E 68 St",
            "6 Ave & W 33 St",
            "Broadway & W 58 St",
            "8 Ave & W 33 St",
            "E 40 St & Park Ave",
            "Central Park S & 6 Ave",
            "Lafayette St & E 8 St",
            "11 Ave & W 41 St",
            "West St & Liberty St",
            "6 Ave & W 34 St",
            "12 Ave & W 40 St",
            "Cleveland Pl & Spring St"
        ],
        "Stations to retrieve bikes": [
            "W 22 & 8 Ave",
            "1 Ave & E 68 St",
            "S 4 St & Wythe Ave",
            "Pier 40 - Hudson River Park",
            "W 22 & 8 Ave",
            "W 22 & 8 Ave",
            "W 22 & 8 Ave",
            "W 22 & 8 Ave",
            "1 Ave & E 68 St",
            "W 22 & 8 Ave",
            "1 Ave & E 68 St",
            "W 22 & 8 Ave",
            "W 22 & 8 Ave",
            "1 Ave & E 68 St",
            "W 22 & 8 Ave",
            "W 22 & 8 Ave",
            "Pier 40 - Hudson River Park",
            "W 22 & 8 Ave",
            "W 22 & 8 Ave",
            "Pier 40 - Hudson River Park"
        ]
    }

    # 2. Build dataframe and display
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)


