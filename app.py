import streamlit as st
import pandas as pd
import plotly.express as px
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title='Formula 1 Prediction | Home',
    page_icon=':bar_chart:',
    layout='wide'
)

st.title(':bar_chart: Formula 1 EDA')
st.markdown('<style> div.block-container {padding-top: 1rem;}</style>',unsafe_allow_html=True)

fl = st.file_uploader(':file_folder: Upload a file', type=['csv','txt','xlsx','xls'])

if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_csv(filename)
