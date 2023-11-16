import streamlit as st
from PIL import Image
import pandas as pd
import plotly.express as px
import os
import glob
import io
import warnings

warnings.filterwarnings('ignore')
path_file = os.getcwd()+ '/images/f1_logo.png'
logo = Image.open(path_file)

st.set_page_config(
    page_title='Formula 1 Prediction | ELT',
    page_icon=logo,
    layout='wide'
)
@st.cache_data
def load_data(path:str):
    data = pd.read_csv(path)
    return data

csv_files = glob.glob('data/*.csv')

st.markdown(f'# <img src="https://raw.githubusercontent.com/elghallali/formula-1-streamlit-app/master/images/f1_logo.png" alt="Formula 1 Logo" width=100/> Formula 1 EDA',unsafe_allow_html=True)
st.markdown('<style> div.block-container {padding-top: 0.1rem;}</style>',unsafe_allow_html=True)
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


for file in csv_files:
    df = pd.read_csv(file, index_col=0)
    title = file.split('\\')[-1].split('.')[0].replace('_',' ').capitalize()
    st.write(f"### {title}")
    df = load_data(file)

    with st.expander("Data Preview"):
        tab1, tab2, tab3, tab4,tab5 = st.tabs([":card_file_box: Data", "Types", 'NAN', 'Info', 'Unique Values'])
        tab1.subheader("A tab with a data")
        tab1.dataframe(df,
                     column_config={
                         "year": st.column_config.NumberColumn(format="%d")
                     })
        tab2.subheader("Column type :")
        tab2.text(df.dtypes)
        tab3.subheader("Null values :")
        tab3.text(df.isna().sum())
        tab4.subheader('DataFrame Info')
        buffer = io.StringIO()
        df.info(buf=buffer)
        s = buffer.getvalue()
        tab4.text(s)
        tab5.subheader('')
        tab5.write("H")
    


st.markdown('<style> div.block-container {padding-top: 1rem;}</style>',unsafe_allow_html=True)


