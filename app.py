import streamlit as st
from PIL import Image
import pandas as pd
import plotly.express as px
import os
import glob
import io
import warnings

from etl.extracts import Extracts
warnings.filterwarnings('ignore')

path_file = os.getcwd() + '/images/f1_logo.png'
logo = Image.open(path_file)

st.set_page_config(
    page_title='Formula 1 Prediction | Home',
    page_icon=logo,
    layout='wide'
)

csv_files = glob.glob('data/*.csv')

st.markdown('# <img src="https://raw.githubusercontent.com/elghallali/formula-1-streamlit-app/master/images/f1_logo.png" alt="Formula 1 Logo" width=100/> App for Formula 1',unsafe_allow_html=True)
st.markdown('<style> div.block-container {padding-top: 0.1rem;}</style>',unsafe_allow_html=True)
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.write("# Hello")


circuits = pd.read_csv(os.getcwd() +'/data/circuits.csv')
laptimes = pd.read_csv(os.getcwd() +'/data/lap_times.csv')
pitstops = pd.read_csv(os.getcwd() +'/data/pit_stops.csv')
seasons = pd.read_csv(os.getcwd() +'/data/seasons.csv' , parse_dates = ['year'])
status = pd.read_csv(os.getcwd() +'/data/status.csv')
constructor_standings = pd.read_csv(os.getcwd() +'/data/constructor_standings.csv')
constructors = pd.read_csv(os.getcwd() +'/data/constructors.csv')
driver_standings = pd.read_csv(os.getcwd() +'/data/driver_standings.csv')
drivers = pd.read_csv(os.getcwd() +'/data/drivers.csv')
races = pd.read_csv(os.getcwd() +'/data/races.csv', parse_dates = ['year'])
constructor_results = pd.read_csv(os.getcwd() +'/data/constructor_results.csv')
results = pd.read_csv(os.getcwd() +'/data/results.csv')
qualifying = pd.read_csv(os.getcwd() +'/data/qualifying.csv')

merged1 = pd.merge(drivers,results, on='driverId')
merged2 = pd.merge(merged1, races, on='raceId')

options = st.multiselect(
            'DataFrame Columns',
            list(merged2.columns),list(merged2.columns))
st.dataframe(merged2[options],
                     column_config={
                         "year": st.column_config.NumberColumn(format="%d")
                     })

uploaded_files = st.file_uploader('Add file', accept_multiple_files=True)
for uploaded_file in uploaded_files:
    uploaded_file_extension = uploaded_file.name.split('.')[-1]
    st.dataframe(Extracts(uploaded_file,uploaded_file_extension).load_data())