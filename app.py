import streamlit as st
from PIL import Image
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import os
import io
import warnings

warnings.filterwarnings('ignore')

path_file = os.getcwd() + '/images/f1_logo.png'
logo = Image.open(path_file)

st.set_page_config(
    page_title='Formula 1 | Home',
    page_icon=logo,
    layout='wide'
)

st.markdown('# <img src="https://raw.githubusercontent.com/elghallali/formula-1-streamlit-app/master/images/f1_logo.png" alt="Formula 1 Logo" width=100/> Formula 1 Application',unsafe_allow_html=True)
st.markdown('<style> div.block-container {padding-top: 0.1rem;}</style>',unsafe_allow_html=True)
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

with st.container():
    col_img0, col_img1, col_img2, col_img3 = st.columns([1,4,4,1])
    with col_img1:
        st.image('https://e0.365dm.com/23/02/768x432/skysports-mercedes-f1-2023_6058037.jpg?20230215093406')
    with col_img2:
        st.image('https://e0.365dm.com/23/02/768x432/skysports-f1-2023-car-launch_6058047.jpg?20230215093508')

with st.container():
    
    col_team0, col_team1, col_team2, col_team3 = st.columns([1,4,4,1])
    with col_team1:
        st.markdown("""
                <style>
                    .centered-header {
                        text-align: center;
                    }
                </style>
            """, unsafe_allow_html=True)
        st.markdown('<h2 class="centered-header">Team</h2>', unsafe_allow_html=True)
        team = pd.DataFrame({'Name':['Yassine EL GHALLALI', 'Rabia SLAOUI', 'Issam EL MEHDI']})
        fig = ff.create_table(team, height_constant=30, colorscale=[[0, '#4d004c'],[.5, '#f2e5ff'],[1, '#ffffff']])
        fig.update_layout(font=dict(size=20))
        st.plotly_chart(fig, use_container_width=True)
        
    with col_team2:
        st.markdown("""
                <style>
                    .centered-header {
                        text-align: center;
                    }
                </style>
            """, unsafe_allow_html=True)
        st.markdown('<h2 class="centered-header">Proposed by</h2>', unsafe_allow_html=True)
        #st.header('Encadrant', divider='violet')
        team = pd.DataFrame({'Prof':['Anass BENANI']})
        fig = ff.create_table(team, height_constant=30, colorscale=[[0, '#4d004c'],[.5, '#f2e5ff'],[1, '#ffffff']])
        fig.update_layout(font=dict(size=30))
        st.plotly_chart(fig, use_container_width=True)
    st.header('Description')