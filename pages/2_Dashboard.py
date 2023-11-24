                ##################################################################################################
                ##                                                                                              ##
                ##                                                                                              ##
                ##################################################################################################

import streamlit as st
from PIL import Image
import pandas as pd
import duckdb
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import os
import io
import warnings
from utils.graphs import gauge, pie, plot, scatter

                ##################################################################################################
                ##                                                                                              ##
                ##                                                                                              ##
                ##################################################################################################
warnings.filterwarnings('ignore')

                ##################################################################################################
                ##                                                                                              ##
                ##                                                                                              ##
                ##################################################################################################

path_file = os.getcwd()+ '/images/f1_logo.png'
logo = Image.open(path_file)

                ##################################################################################################
                ##                                                                                              ##
                ##                                                                                              ##
                ##################################################################################################

st.set_page_config(
    page_title='Formula 1 Prediction | Dashboard',
    page_icon=logo,
    layout='wide'
)

                ##################################################################################################
                ##                                                                                              ##
                ##                                                                                              ##
                ##################################################################################################

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

                ##################################################################################################
                ##                                                                                              ##
                ##                                                                                              ##
                ##################################################################################################

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


                ##################################################################################################
                ##                                                                                              ##
                ##                                                                                              ##
                ##################################################################################################

def component(title,name, value):
    st.markdown(f"""
        **{title}**

        > {name}
        >
        > {value}
                    """, unsafe_allow_html=True)
    





                ##################################################################################################
                ##                                                                                              ##
                ##                                                                                              ##
                ##################################################################################################



                ##################################################################################################
                ##                                                                                              ##
                ##                                                                                              ##
                ##################################################################################################



                ##################################################################################################
                ##                                                                                              ##
                ##                                                                                              ##
                ##################################################################################################

with st.container():

                ##################################################################################################
                ##                                                                                              ##
                ##                                                                                              ##
                ##################################################################################################
    tab_1, tab_2 = st.tabs(['Drivers', 'Teams'])

    with tab_1:
        duckdb_connection = duckdb.connect()
        with st.container():
            col1,col2,col3 = st.columns([1,2,1])
            with col1:
                col4,col5 = st.columns(2)
                with col4:
                    total_driver = duckdb.sql(f"""
                        SELECT COUNT(driverId) AS driver FROM drivers
                    """).df()
                    component("**Total Driver**", "<br>", total_driver.loc[0,'driver'])
                with col5:
                    total_races = duckdb.sql(f"""
                            SELECT COUNT(raceId) AS races FROM races
                        """).df()
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
                
                year_values = st.slider(
                '**Seasons:**',
                1950, 2023, (1950, 2023),
                key='divers_slider')

        with st.container():

            col1,col2,col_3 = st.columns([2,3,3])
            with col1:
                labels = ['Oxygen','Hydrogen','Carbon_Dioxide','Nitrogen']
                values = [4500, 2500, 1053, 1500]
                # Use `hole` to create a donut-like pie chart
                pie(labels,values)
            with col2:
                # Validate and use the selected years
                if year_values[0] <= year_values[1]:
                    selected_start_year, selected_end_year = year_values

                    # Using string formatting (be cautious about SQL injection)
                    query = f"""
                        SELECT
                            COUNT(DISTINCT r.driverId) AS Driver,
                            DATE_PART('year', ra.year) as Season
                        FROM
                            results r
                        JOIN
                            races ra ON r.raceId = ra.raceId
                        WHERE Season BETWEEN {selected_start_year} AND {selected_end_year}
                        GROUP BY DATE_PART('year', ra.year)
                        ORDER BY DATE_PART('year', ra.year)
                    """

                    # Execute the query
                    total_drivers_years = duckdb_connection.execute(query).df()
                plot(total_drivers_years, x="Season", y="Driver", title='Total Driver')
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

                ##################################################################################################
                ##                                                                                              ##
                ##                                                                                              ##
                ##################################################################################################

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
                ##################################################################################################
                ##                                                                                              ##
                ##                                                                                              ##
                ##################################################################################################
                finished_race = duckdb.sql(f"""
                    SELECT 
                        (SELECT COUNT(driverId) FROM results) AS All_Drivers,
                        (COUNT(r.driverId) * 100.0 / (SELECT COUNT(driverId) FROM results)) AS Percentage_Finished
                    FROM
                        results AS r
                    JOIN
                        status s ON r.statusId = s.statusId
                    WHERE s.status IN ('Finished', '%Laps');

                """).df()
                gauge(finished_race.loc[0,'Percentage_Finished']," %","Finished Race (%)")

                ##################################################################################################
                ##                                                                                              ##
                ##                                                                                              ##
                ##################################################################################################
                accident_race = duckdb.sql(f"""
                    SELECT 
                        (SELECT COUNT(driverId) FROM results) AS All_Drivers,
                        (COUNT(r.driverId) * 100.0 / (SELECT COUNT(driverId) FROM results)) AS Percentage_Accident
                    FROM
                        results AS r
                    JOIN
                        status s ON r.statusId = s.statusId
                    WHERE s.status = 'Accident';

                """).df()
                gauge(accident_race.loc[0,'Percentage_Accident']," %","Accident (%)")
            with col4:
                df = px.data.tips()
                scatter(df, x="total_bill", y="tip")

                ##################################################################################################
                ##                                                                                              ##
                ##                                                                                              ##
                ##################################################################################################

    with tab_2:
        with st.container():
            col1,col2,col3 = st.columns([1,2,1])
            with col1:
                col4,col5 = st.columns(2)
                with col4:
                    total_brands = duckdb.sql(f"""
                        SELECT COUNT(constructorId) AS Brand From constructors
                    """).df()
                    component("Total Brands", '<br>', total_brands.loc[0,'Brand'])
                with col5:
                    total_races = duckdb.sql(f"""
                            SELECT COUNT(raceId) AS races FROM races
                                             
                        """).df()
                    component("**Total Races**", "<br>", total_races.loc[0,'races'])
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
                year_values_teams = st.slider(
                '**Seasons:**',
                1950, 2023, (1950, 2023),
                key ='teams_slider')

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
                # Validate and use the selected years
                if year_values_teams[0] <= year_values_teams[1]:
                    selected_start_year, selected_end_year = year_values_teams

                    # Using string formatting (be cautious about SQL injection)
                    query2 = f"""
                        SELECT
                            COUNT(DISTINCT r.constructorId) AS Brand,
                            DATE_PART('year', ra.year) as Season
                        FROM
                            results r
                        JOIN
                            races ra ON r.raceId = ra.raceId
                        WHERE Season BETWEEN {selected_start_year} AND {selected_end_year}
                        GROUP BY DATE_PART('year', ra.year)
                        ORDER BY DATE_PART('year', ra.year)
                    """

                    # Execute the query
                    total_drivers_years_team = duckdb_connection.execute(query2).df()
                plot(total_drivers_years_team, x="Season", y="Brand", title='Total Brand')
            with col_3:
                df = px.data.gapminder()
                fig = px.scatter(df.query("year==2007"), x="gdpPercap", y="lifeExp", size="pop", color="continent",
                                hover_name="country", log_x=True, size_max=60)
                fig.update_layout(clickmode='event+select')
                st.plotly_chart(fig, use_container_width=True)

        with st.container():
            col1,col2,col3,col4 = st.columns([3,3,2,3])
            with col1:
                top_brands_with_points = duckdb.sql(f"""
                    SELECT
                        c.name AS Name,
                        c.nationality AS Nationality,
                        SUM(r.points) AS Points
                    FROM
                        constructors c
                    JOIN
                        results r ON c.constructorId = r.driverId
                    GROUP BY
                        c.constructorId, c.name, c.nationality
                    ORDER BY
                        Points DESC
                """
                ).df()

                fig = ff.create_table(top_brands_with_points.head(15), height_constant=30)
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



