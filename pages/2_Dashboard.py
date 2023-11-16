import streamlit as st
from PIL import Image
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import os
import glob
import io
import warnings
warnings.filterwarnings('ignore')

path_file = os.getcwd()+ '/images/f1_logo.png'
logo = Image.open(path_file)

st.set_page_config(
    page_title='Formula 1 Prediction | Dashboard',
    page_icon=logo,
    layout='wide'
)


def plot_metric(label, value, prefix="", suffix="", show_graph=False, color_graph=""):
    fig = go.Figure()

    fig.add_trace(
        go.Indicator(
            value=value,
            gauge={"axis": {"visible": False}},
            number={
                "prefix": prefix,
                "suffix": suffix,
                "font.size": 28,
            },
            title={
                "text": label,
                "font": {"size": 24},
            },
        )
    )

    fig.update_xaxes(visible=False, fixedrange=True)
    fig.update_yaxes(visible=False, fixedrange=True)
    fig.update_layout(
        # paper_bgcolor="lightgrey",
        margin=dict(t=30, b=0),
        showlegend=False,
        plot_bgcolor="white",
        height=100,
    )

    st.plotly_chart(fig, use_container_width=True)

st.markdown('# <img src="https://raw.githubusercontent.com/elghallali/formula-1-streamlit-app/master/images/f1_logo.png" alt="Formula 1 Logo" width=200/> Dashboard',unsafe_allow_html=True)
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
    col1,col2,col3 = st.columns([1,2,1])
    with col1:
        col4,col5 = st.columns(2)
        with col4:
            plot_metric("Debt Equity", 1.10, prefix="", suffix=" %", show_graph=False)
        with col5:
            plot_metric("Debt Equity", 1.10, prefix="", suffix=" %", show_graph=False)
    with col2:
        col6,col7,col8,col9 = st.columns(4)
        with col6:
            st.write("Col6")
        with col7:
            st.write("Col7")
        with col8:
            st.write("Col8")
        with col9:
            st.write("Col9")
    with col3:
        values = st.slider(
        'Seasons',
        1950, 2023, (1950, 2010))
        st.write('Values:', values)

with st.container():
    col1,col2,col_3 = st.columns([2,3,3])
    with col1:
        labels = ['Oxygen','Hydrogen','Carbon_Dioxide','Nitrogen']
        values = [4500, 2500, 1053, 1500]

        # Use `hole` to create a donut-like pie chart
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.8)])
        fig.update_layout(clickmode='event+select')
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        df = px.data.gapminder().query("country=='Canada'")
        fig = px.line(df, x="year", y="lifeExp", title='Life expectancy in Canada')
        fig.update_layout(clickmode='event+select')
        st.plotly_chart(fig, use_container_width=True)
    with col_3:
        df = px.data.gapminder()
        fig = px.scatter(df.query("year==2007"), x="gdpPercap", y="lifeExp", size="pop", color="continent",
                        hover_name="country", log_x=True, size_max=60)
        fig.update_layout(clickmode='event+select')
        st.plotly_chart(fig, use_container_width=True)

with st.container():
    col1,col2,col3,col4 = st.columns([3,3,2,3])
    with col1:
        table_data = [['Name', 'Nationality', 'Point'],
              ['Montréal<br>Canadiens', 18, 4],
              ['Dallas Stars', 18, 5],
              ['NY Rangers', 16, 5],
              ['Boston<br>Bruins', 13, 8],
              ['Chicago<br>Blackhawks', 13, 8],
              ['LA Kings', 13, 8],
              ['Ottawa<br>Senators', 12, 5]]

        fig = ff.create_table(table_data, height_constant=40)

        
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        years = [1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
         2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012]

        fig = go.Figure()
        
        fig.add_trace(go.Bar(y=years,
                        x=[16, 13, 10, 11, 28, 37, 43, 55, 56, 88, 105, 156, 270,
                           299, 340, 403, 549, 499],
                        name='China',
                        marker_color='rgb(26, 118, 255)', orientation='h'
                        ))

        fig.update_layout(
            title='US Export of Plastic Scrap',
            yaxis_tickfont_size=14,
            xaxis=dict(
                title='USD (millions)',
                titlefont_size=16,
                tickfont_size=14,
            ),
            barmode='group',
            bargap=0.15, # gap between bars of adjacent location coordinates.
            bargroupgap=0.1, # gap between bars of the same location coordinate.
            clickmode='event+select'
        )
        st.plotly_chart(fig, use_container_width=True)
        

        
    with col3:
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = 270,
            domain = {'x': [0, 1], 'y': [0, 1]},
            number={
                        "suffix": " %",
                    },
            title = {'text': "Finished Race (%)"}))
        fig.update_layout(font = {'color': "darkblue", 'family': "Arial"}, height=200,
        margin=dict(l=10, r=10, t=50, b=10, pad=8))
        st.plotly_chart(fig, use_container_width=True)

        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = 270,
            domain = {'x': [0, 1], 'y': [0, 1]},
            number={
                        "suffix": " %",
                    },
            title = {'text': "Accident (%)"}))
        fig.update_layout(font = {'color': "darkblue", 'family': "Arial"}, height=200,
        margin=dict(l=10, r=10, t=50, b=10, pad=8))
        st.plotly_chart(fig, use_container_width=True)
    with col4:
        df = px.data.gapminder()
        fig = px.scatter(df.query("year==2007"), x="gdpPercap", y="lifeExp", size="pop", color="continent",
                        hover_name="country", log_x=True, size_max=60)
        fig.update_layout(clickmode='event+select')
        st.plotly_chart(fig, use_container_width=True)
