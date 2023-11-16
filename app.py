import streamlit as st
from PIL import Image
import pandas as pd
import plotly.express as px
import os
import glob
import io
import warnings
warnings.filterwarnings('ignore')

path_file = os.getcwd() + '/images/f1_logo.png'
logo = Image.open(path_file)

st.set_page_config(
    page_title='Formula 1 Prediction | Home',
    page_icon=logo,
    layout='wide'
)

csv_files = glob.glob('data/*.csv')

st.markdown('# <img src="https://raw.githubusercontent.com/elghallali/formula-1-streamlit-app/master/images/f1_logo.png" alt="Formula 1 Logo" width=200/> App for Formula 1',unsafe_allow_html=True)
st.markdown('<style> div.block-container {padding-top: 0.1rem;}</style>',unsafe_allow_html=True)
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)






