import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import warnings
warnings.filterwarnings('ignore')


def pie(labels,values):
    # Use `hole` to create a donut-like pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.7)])
    fig.update_layout(clickmode='event+select')
    st.plotly_chart(fig, use_container_width=True)

def plot(df,x,y,title):
    fig = px.line(df, x=x, y=y, title=title)
    fig.update_layout(clickmode='event+select')
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
                            },
                    title = {'text': title}))
    fig.update_layout(font = font, height=height, margin=margin)
    st.plotly_chart(fig, use_container_width=True)