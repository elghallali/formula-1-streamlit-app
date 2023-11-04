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

st.title(':bar_chart: Formula 1 EDA')
st.markdown('<style> div.block-container {padding-top: 1rem;}</style>',unsafe_allow_html=True)

for file in csv_files:
    df = pd.read_csv(file, index_col=0)
    title = file.split('\\')[1].split('.')[0].replace('_',' ').capitalize()
    st.markdown(f"## {title}" )
    tab1, tab2, tab3, tab4 = st.tabs([":card_file_box: Data", "Types", 'NAN', 'Info'])
    tab1.subheader("A tab with a data")
    tab1.dataframe(df)
    tab2.subheader("A tab with a Columns type")
    tab2.dataframe(df.dtypes)
    tab3.subheader("A tab with an info")
    tab3.dataframe(df.isna().sum())
    tab4.subheader('A tab with an Info')
    buffer = io.StringIO()
    df.info(buf=buffer)
    s = buffer.getvalue()
    tab4.text(s)
