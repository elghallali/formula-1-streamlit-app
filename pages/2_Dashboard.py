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
from etl.factTable import factTable
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
    page_title='Formula 1 | Dashboard',
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

data = factTable()


                ##################################################################################################
                ##                                                                                              ##
                ##                                                                                              ##
                ##################################################################################################

def component(title,name, value):
    st.markdown(f"""
        **{title}**
        >
        > {name}
        >
        > {value}
                    """, unsafe_allow_html=True)

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
            col1,col2,col3 = st.columns([1,1,2])
            with col1:
                
                year_values = st.slider(
                '**Seasons:**',
                1950, 2023, (1950, 2023),
                key='divers_slider')
            if year_values[0] <= year_values[1]:
                selected_start_year_driver, selected_end_year_driver = year_values
                with col2:
                    col4,col5 = st.columns(2)
                    with col4:
                        total_driver = duckdb.sql(f"""
                            SELECT COUNT(DISTINCT driverName) AS driver FROM data
                            WHERE DATE_PART('year', year) BETWEEN {selected_start_year_driver} AND {selected_end_year_driver}
                        """).df()
                        component("**Total Driver**", "<br>", total_driver.loc[0,'driver'])
                    with col5:
                        # Validate and use the selected years
                        if year_values[0] <= year_values[1]:
                            selected_start_year, selected_end_year = year_values
                            total_races = f"""
                                SELECT
                                    DATE_PART('year', year) AS year,
                                    COUNT(DISTINCT GPName) AS total_GP
                                FROM
                                    data
                                WHERE
                                    DATE_PART('year', year) BETWEEN {selected_start_year} AND {selected_end_year}
                                GROUP BY DATE_PART('year', year)
                            """
                            result_df = duckdb_connection.execute(total_races).df()
                            # Calculate the total GP count by summing the counts for each year
                            total_gp_count = result_df['total_GP'].sum()
                            component("**Total Races**", "<br>", total_gp_count)
                with col3:
                    col6,col7,col8 = st.columns([2,3,2])
                    with col6:
                        query_most_winner = f"""
                            SELECT
                                COUNT(positionOrder) AS TotalWin,
                                driverName AS Winner
                            FROM
                                data
                            WHERE
                                positionOrder = 1 AND ( DATE_PART('year', year) BETWEEN {selected_start_year} AND {selected_end_year})
                            GROUP BY Winner
                            ORDER BY COUNT(positionOrder) DESC
                        """

                        # Execute the query
                        most_winner = duckdb_connection.execute(query_most_winner).df()
                        component("Most Winning Racer",most_winner.loc[0,'Winner'], most_winner.loc[0,'TotalWin'])
                    with col7:
                        query_most_participating = f"""
                            SELECT
                                COUNT(driverName) AS MaxParticipation,
                                driverName AS MostParticipating
                            FROM
                                data
                            WHERE DATE_PART('year', year) BETWEEN {selected_start_year} AND {selected_end_year}
                            GROUP BY driverName
                            ORDER BY MaxParticipation DESC
                            LIMIT 1
                        """

                        # Execute the query
                        most_participating = duckdb_connection.execute(query_most_participating).df()
                        component("Most Participating Racer",most_participating.loc[0,'MostParticipating'], most_participating.loc[0,'MaxParticipation'])
                    with col8:
                        query_top_speed = f"""
                            SELECT
                                MAX(fastestLapSpeed) AS MaxSpeed,
                                driverName AS MaxSpeedDriver
                            FROM 
                                data
                            WHERE EXTRACT(year FROM year) BETWEEN {selected_start_year} AND {selected_end_year}
                            GROUP BY driverName
                            ORDER BY MaxSpeed DESC
                            LIMIT 1
                            """
                        top_speed = duckdb_connection.execute(query_top_speed).df()
                        component("Top Speed Record",top_speed.loc[0,'MaxSpeedDriver'], top_speed.loc[0,'MaxSpeed'])
                with st.container():
                    col1,col2,col_3 = st.columns([2,3,3])
                    with col1:
                        labels = ['Oxygen','Hydrogen','Carbon_Dioxide','Nitrogen']
                        values = [4500, 2500, 1053, 1500]
                        # Use `hole` to create a donut-like pie chart
                        pie(labels,values)
                    with col2:
                            # Using string formatting (be cautious about SQL injection)
                            query = f"""
                                SELECT
                                    COUNT(DISTINCT driverName) AS Driver,
                                    DATE_PART('year', year) as Season
                                FROM
                                    data

                                WHERE Season BETWEEN {selected_start_year} AND {selected_end_year}
                                GROUP BY DATE_PART('year', year)
                                ORDER BY DATE_PART('year', year)
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
                                driverName AS Name,
                                driverNationality AS Nationality,
                                SUM(points) AS Points
                            FROM
                                data
                            WHERE DATE_PART('year', year) BETWEEN {selected_start_year_driver} AND {selected_end_year_driver}
                            GROUP BY
                                driverName, driverNationality
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
                                status as Status,
                                COUNT(driverName) AS Driver
                            FROM
                                data
                            WHERE
                                status IN ('Accident','Engine', 'Did not qualify', 'Collision', 'Gearbox', 'Spun off', 'Suspension', 'Did not prequalify', 'Transmission', 'Electrical')
                                AND (DATE_PART('year', year) BETWEEN {selected_start_year_driver} AND {selected_end_year_driver})
                            GROUP BY status
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
                                (SELECT COUNT(driverName) FROM data) AS All_Drivers,
                                (COUNT(driverName) * 100.0 / (SELECT COUNT(driverName) FROM data)) AS Percentage_Finished
                            FROM
                                data
                            WHERE status IN ('Finished') 
                                AND (DATE_PART('year', year) BETWEEN {selected_start_year_driver} AND {selected_end_year_driver});
                        """).df()
                        gauge(finished_race.loc[0,'Percentage_Finished']," %","Finished Race (%)")
                        ##################################################################################################
                        ##                                                                                              ##
                        ##                                                                                              ##
                        ##################################################################################################
                        accident_race = duckdb.sql(f"""
                            SELECT 
                                (SELECT COUNT(driverName) FROM data) AS All_Drivers,
                                (COUNT(driverName) * 100.0 / (SELECT COUNT(driverName) FROM data)) AS Percentage_Accident
                            FROM
                                data
                            WHERE status IN ('Accident')
                                AND (DATE_PART('year', year) BETWEEN {selected_start_year_driver} AND {selected_end_year_driver});
                        """).df()
                        gauge(accident_race.loc[0,'Percentage_Accident']," %","Accident (%)")
                    with col4:
                        df = px.data.tips()
                        scatter(df, x="total_bill", y="tip")
                ##################################################################################################
                ##                                                                                              ##
                ##                          Tab 2: Is for teams                                                 ##
                ##################################################################################################
    with tab_2:
        with st.container():
            col1,col2,col3 = st.columns([1,1,2])
            with col1:
                year_start, year_end = st.slider(
                '**Seasons:**',
                1950, 2023, (1950, 2023),
                key ='teams_slider')
            # Validate and use the selected years
            if year_start <= year_end:
                selected_start_year, selected_end_year = year_start,year_end
                with col2:
                    col4,col5 = st.columns(2)
                    with col4:
                        total_brands = duckdb.sql(f"""
                            SELECT COUNT(DISTINCT brand) AS Brand From data
                            WHERE DATE_PART('year', year) BETWEEN {selected_start_year} AND {selected_end_year}
                        """).df()
                        component("Total Brands", '<br>', total_brands.loc[0,'Brand'])
                    with col5:
                            total_races = f"""
                                SELECT
                                    DATE_PART('year', year) AS year,
                                    COUNT(DISTINCT GPName) AS total_GP
                                FROM
                                    data
                                WHERE
                                    DATE_PART('year', year) BETWEEN {selected_start_year} AND {selected_end_year}
                                GROUP BY DATE_PART('year', year)
                            """
                            result_df = duckdb_connection.execute(total_races).df()
                            # Calculate the total GP count by summing the counts for each year
                            total_gp_count = result_df['total_GP'].sum()
                            component("**Total Races**", "<br>", total_gp_count)
                with col3:
                    col6,col7,col8 = st.columns(3)
                    with col6:
                        most_winning_brand_query=f"""
                            SELECT
                                COUNT(positionOrder) AS TotalWin,
                                brand AS Brand
                            FROM
                                data
                            WHERE
                                positionOrder = 1 AND ( DATE_PART('year', year) BETWEEN {selected_start_year} AND {selected_end_year})
                            GROUP BY Brand
                            ORDER BY COUNT(positionOrder) DESC
                        """
                        most_winning_brand = duckdb_connection.execute(most_winning_brand_query).df()
                        component("Most Winning Brand",most_winning_brand.loc[0,'Brand'], most_winning_brand.loc[0,'TotalWin'])
                    with col7:
                        most_participating_brand_query=f"""
                            SELECT
                                COUNT(brand) AS MaxParticipation,
                                brand AS MostParticipating
                            FROM
                                data
                            WHERE DATE_PART('year', year) BETWEEN {selected_start_year} AND {selected_end_year}
                            GROUP BY brand
                            ORDER BY MaxParticipation DESC
                            LIMIT 1
                        """
                        most_participating_brand = duckdb_connection.execute(most_participating_brand_query).df()
                        component("Most Participating Brand",most_participating_brand.loc[0,'MostParticipating'], most_participating_brand.loc[0,'MaxParticipation'])
                    with col8:
                        top_speed_brand_query = f"""
                            SELECT
                                MAX(fastestLapSpeed) AS MaxSpeed,
                                brand AS MaxSpeedBrand
                            FROM 
                                data
                            WHERE EXTRACT(year FROM year) BETWEEN {selected_start_year} AND {selected_end_year}
                            GROUP BY brand
                            ORDER BY MaxSpeed DESC
                            LIMIT 1
                        """
                        top_speed_brand = duckdb_connection.execute(top_speed_brand_query).df()
                        component("Top Speed Record (Brand)",top_speed_brand.loc[0,'MaxSpeedBrand'], top_speed_brand.loc[0,'MaxSpeed'])
            

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
                        # Using string formatting (be cautious about SQL injection)
                        query2 = f"""
                            SELECT
                                COUNT(DISTINCT brand) AS Brand,
                                DATE_PART('year', year) as Season
                            FROM
                                data
                            WHERE Season BETWEEN {selected_start_year} AND {selected_end_year}
                            GROUP BY DATE_PART('year', year)
                            ORDER BY DATE_PART('year', year)
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
                                brand AS Name,
                                brandNationality AS Nationality,
                                SUM(points) AS Points
                            FROM
                                data
                            WHERE DATE_PART('year', year) BETWEEN {selected_start_year} AND {selected_end_year}
                            GROUP BY
                                brand, brandNationality
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
                finished_race = duckdb.sql(f"""
                    SELECT 
                        (SELECT COUNT(brand) FROM data) AS All_Brands,
                        (COUNT(brand) * 100.0 / (SELECT COUNT(brand) FROM data)) AS Percentage_Finished
                    FROM
                        data
                    WHERE status IN ('Finished') AND (DATE_PART('year', year) BETWEEN {selected_start_year} AND {selected_end_year});

                """).df()
                gauge(finished_race.loc[0,'Percentage_Finished']," %","Finished Race (%)")

                accident_race = duckdb.sql(f"""
                    SELECT 
                        (SELECT COUNT(brand) FROM data) AS All_Brands,
                        (COUNT(brand) * 100.0 / (SELECT COUNT(brand) FROM data)) AS Percentage_Accident
                    FROM
                        data
                    WHERE status IN ('Accident') AND (DATE_PART('year', year) BETWEEN {selected_start_year} AND {selected_end_year});

                """).df()
                gauge(accident_race.loc[0,'Percentage_Accident']," %","Accident (%)")
            with col4:
                fig = px.treemap(
                    names = ["Eve","Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura"],
                    parents = ["", "Eve", "Eve", "Seth", "Seth", "Eve", "Eve", "Awan", "Eve"]
                )
                fig.update_traces(root_color="lightgrey")
                fig.update_layout(margin = dict(t=50, l=25, r=25, b=25),clickmode='event+select')
                st.plotly_chart(fig, use_container_width=True)



