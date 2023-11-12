import streamlit as st
import pandas as pd
import plotly.express as px
import os
import glob
import io
import warnings

warnings.filterwarnings('ignore')

st.set_page_config(
    page_title='Formula 1 Prediction | ELT',
    page_icon=':bar_chart:',
    layout='wide'
)
@st.cache_data
def load_data(path:str):
    data = pd.read_csv(path)
    return data

csv_files = glob.glob('data/*.csv')

st.title(':bar_chart: Formula 1 EDA')


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
        tab5.write("HI")
    


st.markdown('<style> div.block-container {padding-top: 1rem;}</style>',unsafe_allow_html=True)


