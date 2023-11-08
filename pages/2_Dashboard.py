import streamlit as st
import pandas as pd
import plotly.express as px
import os
import glob
import io
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title='Formula 1 Prediction | Dashboard',
    page_icon=':bar_chart:',
    layout='wide'
)

st.title(':bar_chart: Dashboard')
st.markdown('<style> div.block-container {padding-top: 1rem;}</style>',unsafe_allow_html=True)