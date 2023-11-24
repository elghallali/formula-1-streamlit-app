import streamlit as st
from PIL import Image
import pandas as pd
import os
import glob
import io
import warnings


from etl.extracts import Extracts

warnings.filterwarnings('ignore')

path_file = os.getcwd()+ '/images/f1_logo.png'
logo = Image.open(path_file)

st.set_page_config(
    page_title='Formula 1 Prediction | ETL',
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

data = {}
for file in csv_files:
    title = file.replace('\\','/').split('/')[-1].split('.')[0].replace('_',' ').capitalize()
    extension = file.replace('\\','/').split('/')[-1].split('.')[-1]
    df = Extracts(file, extension).load_data()
    data[title]= df

def visualDataFrame(df):
    with st.expander("Data Preview"):
        options = st.multiselect(
            'DataFrame Columns',
            list(df.columns),list(df.columns))

        tab1, tab2, tab3, tab4,tab5 = st.tabs([":card_file_box: Data", "Types", 'NAN', 'Info', 'Unique Values'])
        with tab1:
            st.subheader("A tab with a data")
            st.dataframe(df[options],
                     column_config={
                         "year": st.column_config.NumberColumn(format="%d")
                     })

        with tab2:
            st.subheader("Column type :")
            st.text(df[options].dtypes)
        with tab3:
            st.subheader("Null values :")
            st.text(df[options].isna().sum())
        with tab4:
            st.subheader('DataFrame Info')
            buffer = io.StringIO()
            df[options].info(buf=buffer)
            s = buffer.getvalue()
            st.text(s)
        with tab5:
            st.subheader('')
            st.write("H")

    
data_set = st.multiselect(
        '**Data Frames**',
        list(data.keys()),list(data.keys()))

for dataset in data_set:
    st.write(f"### {dataset}")
    visualDataFrame(data[dataset])