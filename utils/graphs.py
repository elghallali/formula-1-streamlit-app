import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import warnings
warnings.filterwarnings('ignore')


def pie(labels,values):
    

    # pull is given as a fraction of the pie radius
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.7, pull=[0, 0, 0.1, 0])])
    fig.update_layout(clickmode='event+select')
    st.plotly_chart(fig, use_container_width=True)

def plot(df,x,y,title):
    fig = px.line(df, x=x, y=y, markers=True)
    fig.update_layout(clickmode='event+select')
    fig.update_layout(
    title=title,
    title_x=0.5,  # Set the title's x position to 0.5 for centering
)
    st.plotly_chart(fig, use_container_width=True)
    

def scatter(df,x,y,hover_name=None, size_max=20, log_x=False):
    fig = px.scatter(df, x=x, y=y, hover_name=hover_name, log_x=log_x, size_max=size_max)
    fig.update_layout(clickmode='event+select')
    st.plotly_chart(fig, use_container_width=True)

def gauge(value,suffix,title,font= {'color': "darkblue", 'family': "Arial"}, height=200, margin=dict(l=10, r=10, t=50, b=10, pad=8)):
    fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = value,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    number={
                                "suffix": suffix,
                                "valueformat": ".2f"
                            },
                    title = {'text': title},
                    gauge = {'axis': {'range': [None, 100]}}))
    fig.update_layout(font = font, height=height, margin=margin)
    st.plotly_chart(fig, use_container_width=True)