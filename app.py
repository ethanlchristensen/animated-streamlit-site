import time

# pip install pandas
import pandas as pd

# pip install streamlit
import streamlit as st

# pip install plotly
import plotly.express as px

# pip install streamlit-extras
from streamlit_extras.colored_header import colored_header


# cache resource so we don't have to load the df
# each time we interact with the site
@st.cache_resource
def get_data():
    df = pd.read_csv('data.csv')
    return df


st.set_page_config(layout='wide', page_title='Animated Pie Chart Testing')


df = get_data()

# use the session state to sotre certain data
# we don't want to lose
if not st.session_state.get('chart_data'):
    st.session_state['chart_data'] = [[], []]
if st.session_state.get('go') is None:
    st.session_state['go'] = False

# add a header
colored_header(
    label='Animated Pie Chart Testings',
    description='Site to testing animating a pie chart in streamlit using plotly.',
    color_name='orange-100',
)

# button to launch the animation
go = st.button('Run Chart')

# text area to store row counter
text = st.text('')

# place to hold a pie chart
pie_chart = st.empty()

# place to hold a timeline chart
time_chart = st.empty()

if go:
    # if the button was clicked, set this variable
    # so the whole loop runs
    st.session_state['go'] = True

# if they clicked the go button
if st.session_state.get('go'):
    # loop and keep growing the df row by row
    for _ in range(1, len(df) + 1):
        text.text(f"Loaded {_} row/s")
        sub_df = df.head(_)
        
        # create a pie chart
        pie_fig = px.pie(
            data_frame=sub_df.groupby('wnd_dir').size().reset_index(name='count'),
            values='count',
            names='wnd_dir',
            title='Wind Direction Readings'
        )
        
        # create a line chart
        timeline_fig = px.line(sub_df, x='date', y=['temp', 'dew', 'rain'])
        
        # plot the chart in streamlit
        pie_chart.plotly_chart(figure_or_data=pie_fig, use_container_width=True)
        
        # plot the chart in streamlit
        time_chart.plotly_chart(figure_or_data=timeline_fig, use_container_width=True)

    # rest this variable
    st.session_state['go'] = False