import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import warnings
warnings.filterwarnings('ignore')


def pie(labels,values,title=''):
    

    # pull is given as a fraction of the pie radius
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.7)])
    fig.update_layout(clickmode='event+select',title=title, title_x=0.2)
    st.plotly_chart(fig, use_container_width=True)

def plot(df,x,y,title):
    fig = px.line(df, x=x, y=y, markers=True)
    fig.update_layout(clickmode='event+select')
    fig.update_layout(
    title=title,
    title_x=0.5,  # Set the title's x position to 0.5 for centering
)
    st.plotly_chart(fig, use_container_width=True)
    

def scatter(df,x,y,title='',hover_name=None,  log_x=False, marker_color=None):
    fig = px.scatter(df, x=x, y=y, hover_name=hover_name, log_x=log_x, color=marker_color)
    fig.update_layout(clickmode='event+select',title=title,title_x=0.2)
    st.plotly_chart(fig, use_container_width=True)

def gauge(value,suffix,title,font= {'color': "white", 'family': "Arial"}, height=190, margin=dict(l=10, r=10, t=50, b=10, pad=8)):
    fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = value,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    number={
                                "suffix": suffix,
                                "valueformat": ".2f"
                            },
                    title = {'text': title},
                    gauge = {'axis': {'range': [None, 100]},
                             'bar': {'color': '#F63366'}}))
    fig.update_layout(font = font, height=height, margin=margin)
    st.plotly_chart(fig, use_container_width=True)