import streamlit as st
from PIL import Image
import pandas as pd
import duckdb
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import os
import glob
import io
import warnings
from etl.extracts import Extracts

from utils.graphs import gauge, pie, plot, scatter
warnings.filterwarnings('ignore')

path_file = os.getcwd()+ '/images/f1_logo.png'
logo = Image.open(path_file)

st.set_page_config(
    page_title='Formula 1 Prediction | Dashboard',
    page_icon=logo,
    layout='wide'
)

st.markdown('# <img src="https://raw.githubusercontent.com/elghallali/formula-1-streamlit-app/master/images/f1_logo.png" alt="Formula 1 Logo" width=100/> Dashboard',unsafe_allow_html=True)
st.markdown('<style> div.block-container {padding-top: 0.1rem;}</style>', unsafe_allow_html=True)
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

circuits = pd.read_csv(os.getcwd() +'/data/circuits.csv')
laptimes = pd.read_csv(os.getcwd() +'/data/lap_times.csv')
pitstops = pd.read_csv(os.getcwd() +'/data/pit_stops.csv')
seasons = pd.read_csv(os.getcwd() +'/data/seasons.csv' , parse_dates = ['year'])
status = pd.read_csv(os.getcwd() +'/data/status.csv')
constructor_standings = pd.read_csv(os.getcwd() +'/data/constructor_standings.csv')
constructors = pd.read_csv(os.getcwd() +'/data/constructors.csv')
driver_standings = pd.read_csv(os.getcwd() +'/data/driver_standings.csv')
drivers = pd.read_csv(os.getcwd() +'/data/drivers.csv')
races = pd.read_csv(os.getcwd() +'/data/races.csv', parse_dates = ['year'])
constructor_results = pd.read_csv(os.getcwd() +'/data/constructor_results.csv')
results = pd.read_csv(os.getcwd() +'/data/results.csv')
qualifying = pd.read_csv(os.getcwd() +'/data/qualifying.csv')

    
def component(title,name, value):
    st.markdown(f"""
        **{title}**

        > {name}
        >
        > {value}
                    """, unsafe_allow_html=True)
    
def update_season_input_drivers():
    st.session_state.min_seasons_value_driver = st.session_state.divers_slider[0]
    st.session_state.max_seasons_value_driver = st.session_state.divers_slider[1]

def update_season_input_teams():
    st.session_state.min_seasons_value_teams = st.session_state.teams_slider[0]
    st.session_state.max_seasons_value_teams = st.session_state.teams_slider[1]

total_driver = duckdb.sql(
        f"""
        
        SELECT COUNT(driverId) AS driver FROM drivers
        """
    ).df()

total_races = duckdb.sql(
    f"""
    SELECT COUNT(raceId) AS races FROM races
    """
).df()



with st.container():
    tab_1, tab_2 = st.tabs(['Drivers', 'Teams'])

    with tab_1:
        with st.container():
            col_1,col_2,col_3,col_4,col_5,col_6,col_7,col_8 = st.columns([2,1,1,1,1,1,1,1])
            with col_2:
                st.markdown("**Race Name**")
                with st.expander("All"):
                    option_1 = st.checkbox('initial velocity (u)')
                    option_2 = st.checkbox('final velocity (v)')
                    option_3 = st.checkbox('acceleration (a)')
                    option_4 = st.checkbox('time (t)')
            with col_3:
                st.markdown("**Driver Name**")
                with st.expander("All"):
                    st.write("HI")
            with col_4:
                st.markdown("**Driver Nationality**")
                with st.expander("All"):
                    st.write("HI")
            with col_5:
                st.markdown("**Brand Name**")
                with st.expander("All"):
                    st.write("HI")
            with col_6:
                st.markdown("**Brand Nationality**")
                with st.expander("All"):
                    st.write("HI")
            with col_7:
                st.markdown("**Circuit Name**")
                with st.expander("All"):
                    st.write("HI")
            with col_8:
                st.markdown("**Circuit Country**")
                with st.expander("All"):
                    st.write("HI")


        with st.container():
            col1,col2,col3 = st.columns([1,2,1])
            with col1:
                col4,col5 = st.columns(2)
                with col4:
                    component("**Total Driver**", "<br>", total_driver.loc[0,'driver'])
                with col5:
                    component("**Total Races**", "<br>", total_races.loc[0,'races'])
            with col2:
                col6,col7,col8,col9 = st.columns([2,3,2,2])
                with col6:
                    component("Most Winning Racer","Good morning", 45)
                with col7:
                    component("Most Participating Racer","Good evening", 50)
                with col8:
                    component("Top Speed Record","Good night", 70)
                with col9:
                    component("Biggest Win Rate","Good afternoon", 40)
            with col3:
                col_input1,col_input2 = st.columns(2)
                with col_input1:
                    min_number = st.number_input(label='**Seasons**', min_value=1950, max_value=2023, value=1950, step=1, format=None, key='min_seasons_value_driver')
                with col_input2:
                    max_number = st.number_input(label='', min_value=min_number, max_value=2023, value=2023, step=1, format=None, key='max_seasons_value_driver')
                year_values = st.slider(
                '',
                1950, 2023, (min_number, max_number),
                key='divers_slider',
                on_change=update_season_input_drivers)

        with st.container():
            col1,col2,col_3 = st.columns([2,3,3])
            with col1:
                labels = ['Oxygen','Hydrogen','Carbon_Dioxide','Nitrogen']
                values = [4500, 2500, 1053, 1500]
                # Use `hole` to create a donut-like pie chart
                pie(labels,values)
            with col2:
                selected_start_year, selected_end_year = year_values
                total_drivers_years = duckdb.sql(f"""
                    SELECT
                        COUNT(r.driverId) AS Driver,
                        DATE_PART('year', ra.year) as Years
                    FROM
                        results r
                    JOIN
                        races ra ON r.raceId = ra.raceId
                    GROUP BY DATE_PART('year', ra.year)
                    ORDER BY DATE_PART('year', ra.year)
                """
                ).df()
                plot(total_drivers_years, x="Years", y="Driver", title='Total Driver')
            with col_3:
                df = px.data.gapminder()
                scatter(df.query("year==2007"), x="gdpPercap", y="lifeExp",  
                                hover_name="country", log_x=True, size_max=60)

        with st.container():
            col1,col2,col3,col4 = st.columns([3,3,2,3])
            with col1:
                top_racers_with_points = duckdb.sql(f"""
                    SELECT
                        d.forename || ' ' || d.surname AS Name,
                        d.nationality AS Nationality,
                        SUM(r.points) AS Points
                    FROM
                        drivers d
                    JOIN
                        results r ON d.driverId = r.driverId
                    GROUP BY
                        d.driverId, d.forename, d.surname, d.nationality
                    ORDER BY
                        Points DESC
                """
                ).df()

                fig = ff.create_table(top_racers_with_points.head(15), height_constant=30)


                st.plotly_chart(fig, use_container_width=True)
            with col2:
                reason_driver_not_finish_races = duckdb.sql(f"""
                    SELECT 
                        s.status as Status,
                        COUNT(r.driverId) AS Driver

                    FROM
                        results AS r
                    JOIN
                        status AS s ON r.statusId = s.statusId
                    WHERE
                        s.status IN ('Accident','Engine', 'Did not qualify', 'Collision', 'Gearbox', 'Spun off', 'Suspension', 'Did not prequalify', 'Transmission', 'Electrical')
                    GROUP BY s.status
                    ORDER BY Driver ASC
                """).df()
                
                fig = go.Figure()

                fig.add_trace(go.Bar(
                    y=reason_driver_not_finish_races['Status'],
                    x=reason_driver_not_finish_races['Driver'],
                    orientation='h'
                ))

                fig.update_layout(
                    title='Most Reason Driver Don\'t Finished Race',
                    xaxis_title='Driver',
                    yaxis_title='Status',
                    title_x=0.2,
                    clickmode='event+select'
                )
                fig.update_xaxes(tickformat=".2s")
                st.plotly_chart(fig, use_container_width=True)



            with col3:
                gauge(26.79," %","Finished Race (%)")
                gauge(4.08," %","Accident (%)")
            with col4:
                df = px.data.tips()
                scatter(df, x="total_bill", y="tip")



    with tab_2:
        with st.container():
            col_1,col_2,col_3,col_4,col_5,col_6,col_7,col_8 = st.columns([2,1,1,1,1,1,1,1])
            with col_2:
                st.markdown("**Race Name**")
                with st.expander("All"):
                    st.write("HI")
            with col_3:
                st.markdown("**Driver Name**")
                with st.expander("All"):
                    st.write("HI")
            with col_4:
                st.markdown("**Driver Nationality**")
                with st.expander("All"):
                    st.write("HI")
            with col_5:
                st.markdown("**Brand Name**")
                with st.expander("All"):
                    st.write("HI")
            with col_6:
                st.markdown("**Brand Nationality**")
                with st.expander("All"):
                    st.write("HI")
            with col_7:
                st.markdown("**Circuit Name**")
                with st.expander("All"):
                    st.write("HI")
            with col_8:
                st.markdown("**Circuit Country**")
                with st.expander("All"):
                    st.write("HI")


        with st.container():
            col1,col2,col3 = st.columns([1,2,1])
            with col1:
                col4,col5 = st.columns(2)
                with col4:
                    component("Good morning", '<br>', 45)
                with col5:
                    component("Good morning", '<br>', 45)
            with col2:
                col6,col7,col8,col9 = st.columns(4)
                with col6:
                    component("Hi","Good morning", 45)
                with col7:
                    component("Hi","Good evening", 50)
                with col8:
                    component("Hi","Good night", 70)
                with col9:
                    component("Hi","Good afternoon", 40)
            with col3:
                col_input1,col_input2 = st.columns(2)
                with col_input1:
                    min_number = st.number_input(label='**Seasons**', min_value=1950, max_value=2023, value=1950, step=1, format=None, key='min_seasons_value_teams')
                with col_input2:
                    max_number = st.number_input(label='', min_value=1950, max_value=2023, value=2023, step=1, format=None, key='max_seasons_value_teams')
                values = st.slider(
                '',
                1950, 2023, (min_number, max_number),
                key ='teams_slider',
                on_change=update_season_input_teams)

        with st.container():
            col1,col2,col_3 = st.columns([2,3,3])
            with col1:
                labels = ['Oxygen','Hydrogen','Carbon_Dioxide','Nitrogen']
                values = [4500, 2500, 1053, 1500]

                # Use `hole` to create a donut-like pie chart
                fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.7)])
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
                    value = 70,
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
                    value = 40,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    number={
                                "suffix": " %",
                            },
                    title = {'text': "Accident (%)"}))
                fig.update_layout(font = {'color': "darkblue", 'family': "Arial"}, height=200,
                margin=dict(l=10, r=10, t=50, b=10, pad=8))
                st.plotly_chart(fig, use_container_width=True)
            with col4:
                fig = px.treemap(
                    names = ["Eve","Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura"],
                    parents = ["", "Eve", "Eve", "Seth", "Seth", "Eve", "Eve", "Awan", "Eve"]
                )
                fig.update_traces(root_color="lightgrey")
                fig.update_layout(margin = dict(t=50, l=25, r=25, b=25),clickmode='event+select')
                st.plotly_chart(fig, use_container_width=True)



