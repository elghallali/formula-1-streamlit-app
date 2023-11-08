import streamlit as st
import pandas as pd
import plotly.express as px
import os
import glob
import io
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title='Formula 1 Prediction | Home',
    page_icon=':bar_chart:',
    layout='wide'
)

csv_files = glob.glob('data/*.csv')

st.title(':bar_chart: App for Formula 1')
st.markdown('<style> div.block-container {padding-top: 1rem;}</style>',unsafe_allow_html=True)

"Hello World!"
df = pd.DataFrame(data={"col1":[3,5,6],"col2":[4,7,9],"col3":[2,6,0]}, index=["l1","l2","l3"])
df
