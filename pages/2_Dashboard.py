                ##################################################################################################
                ##                                                                                              ##
                ##                                                                                              ##
                ##                                                                                              ##
                ##################################################################################################
from functools import partial
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
from etl.data import factTable,qualifying,results
from utils.graphs import gauge, pie, plot, scatter

                ##################################################################################################
                ##                                                                                              ##
                ##                                                                                              ##
                ##                                                                                              ##
                ##################################################################################################
warnings.filterwarnings('ignore')

                ##################################################################################################
                ##                                                                                              ##
                ##                                                                                              ##
                ##                                                                                              ##
                ##################################################################################################
qualifying0 = qualifying[0] 
results0 = results[0]
                ##################################################################################################
                ##                                                                                              ##
                ##                                                                                              ##
                ##                                                                                              ##
                ##################################################################################################

path_file = os.getcwd()+ '/images/f1_logo.png'
logo = Image.open(path_file)

                ##################################################################################################
                ##                                                                                              ##
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
                ##                                                                                              ##
                ##################################################################################################

data = factTable()


                ##################################################################################################
                ##                                                                                              ##
                ##                                                                                              ##
                ##                                                                                              ##
                ##################################################################################################

def component(title,name, value):
    st.markdown(f"""
        **{title}**

        <div style="border-left: 5px solid red;">
            <span style="font-size: 20px; padding-left: 15px;"><b>{name}</b></span>
            <br>
            <span style="font-size: 20px; padding-left: 20px;">{value}</span>
            <br>
        </div>
        
                    """, unsafe_allow_html=True)

                ##################################################################################################
                ##                                                                                              ##
                ##                                                                                              ##
                ##                                                                                              ##
                ##################################################################################################

def component2(title,value):
    st.markdown(f"""
        <div style="text-align: center;">
        <span style="font-size: 50px; text-align: center;">{value}</span>
        <br>
        <span style="font-size: 20px; text-align: center; "><b>{title}</b></span>
        <br>
        </div>
        """, unsafe_allow_html=True)
    
                ##################################################################################################
                ##                                                                                              ##
                ##                                                                                              ##
                ##                                                                                              ##
                ##################################################################################################
def check_change(text,expander_label,data_unique):
    if st.session_state[f"all_option_{text}{expander_label}"]:
        st.session_state[f"selected_options_{text}{expander_label}"] = list(data_unique.unique())
    else:
        st.session_state[f"selected_options_{text}{expander_label}"] = []
    return

def multi_change(text,expander_label,data):

    if len(st.session_state[f"selected_options_{text}{expander_label}"]) == len(list(data.unique())):
        st.session_state[f"all_option_{text}{expander_label}"] = True
    else:
        st.session_state[f"all_option_{text}{expander_label}"] = False
    return

def parameterize_SQL_in_statement(items):
    return f"""('{"', '".join(items)}')"""

                ##################################################################################################
                ##                                                                                              ##
                ##                                     Dashboard Page Body                                      ##
                ##                                                                                              ##
                ##################################################################################################


with st.container():

                ##################################################################################################
                ##                                                                                              ##
                ##                               Creating Two Tabs Drivers & Teams                              ##
                ##                                                                                              ##
                ##################################################################################################
    tab_1, tab_2 = st.tabs(['Drivers', 'Teams'])

    with tab_1:
        duckdb_connection = duckdb.connect()
        with st.container():
            cols = st.columns(5)
            where_dict = {}
            for i in range(len(cols)):
                with cols[i]:
                    if i == 0:
                        expander_label = "Race_Name"
                        column_data = data['GPName']
                        text = ''
                    elif i == 1:
                        expander_label = "Driver_Name"
                        column_data = data['driverName']
                        text = ''
                    elif i == 2:
                        expander_label = "Driver_Nationality"
                        column_data = data['driverNationality']
                        text = ''
                    elif i == 3:
                        expander_label = "Brand_Name"
                        column_data = data['brand']
                        text = ''
                    elif i == 4:
                        expander_label = "Brand_Nationality"
                        column_data = data['brandNationality']
                        text = ''
                    
                    with st.expander(expander_label.replace('_',' ')):
                        # Get unique items in the column
                        unique_items = column_data.unique()

                        # Display the selected items
                        if f"all_option_{text}{expander_label}" not in st.session_state:
                            st.session_state[f"all_option_{text}{expander_label}"] = True
                            st.session_state[f"selected_options_{text}{expander_label}"] = list(unique_items)

                        # Display the selected items
                        all = st.checkbox("Select all", key=f"all_option_{text}{expander_label}",on_change= partial(check_change, text, expander_label, column_data))
                        options = st.multiselect('',list(unique_items),key=f"selected_options_{text}{expander_label}", on_change=partial(multi_change, text, expander_label, column_data))
                        where_dict[expander_label]= st.session_state[f'selected_options_{text}{expander_label}']
                        st.markdown(
                            """
                            <style>
                                [data-testid="stExpanderDetails"] {
                                    max-height: 200px;
                                    overflow-y: auto;
                                }
                            </style>
                            """,
                            unsafe_allow_html=True
                        )
            
            col1,col2,col3 = st.columns([3,3,8])
            with col1:
                
                year_values = st.slider(
                '**Seasons:**',
                1950, 2023, (1950, 2023),
                key='divers_slider')
            if year_values[0] <= year_values[1]:
                selected_start_year_driver, selected_end_year_driver = year_values
                
                driverNames = parameterize_SQL_in_statement(where_dict["Driver_Name"])
                driverNationalities = parameterize_SQL_in_statement(where_dict["Driver_Nationality"])
                brands =  parameterize_SQL_in_statement(where_dict["Brand_Name"])
                brandNationalities = parameterize_SQL_in_statement(where_dict["Brand_Nationality"])
                raceNames = parameterize_SQL_in_statement(where_dict["Race_Name"])
                where = f"""
                    (year BETWEEN {selected_start_year_driver} AND {selected_end_year_driver})
                    AND driverName IN {driverNames}
                    AND driverNationality IN {driverNationalities}
                    AND brand IN {brands}
                    AND brandNationality IN {brandNationalities}
                    AND GPName IN {raceNames}
                """
                
                with col2:
                    col4,col5 = st.columns(2)
                    with col4:
                ##################################################################################################
                ##                                                                                              ##
                ##                                         Total Driver                                         ##
                ##                                                                                              ##
                ##################################################################################################
                        total_driver_query = f"""
                            SELECT COUNT(DISTINCT driverName) AS driver FROM data
                            WHERE {where}
                                
                                
                        """
                        total_driver = duckdb_connection.execute(total_driver_query).df()
                        component2("Total Driver",total_driver.loc[0,'driver'])
                    with col5:
                        
                ##################################################################################################
                ##                                                                                              ##
                ##                                      Total Races (Driver)                                    ##
                ##                                                                                              ##
                ##################################################################################################
                            total_races = f"""
                                SELECT
                                    year,
                                    COUNT(DISTINCT GPName) AS total_GP
                                FROM
                                    data
                                WHERE {where}
                                GROUP BY  year
                            """
                            result_df = duckdb_connection.execute(total_races).df()
                            # Calculate the total GP count by summing the counts for each year
                            total_gp_count = result_df['total_GP'].sum()
                            component2("Total Races", total_gp_count)
                with col3:
                    col6,col7,col8 = st.columns(3)
                    with col6:

                ##################################################################################################
                ##                                                                                              ##
                ##                                      Most Winning Racer                                      ##
                ##                                                                                              ##
                ##################################################################################################
                        query_most_winner = f"""
                            SELECT
                                COUNT(positionOrder) AS TotalWin,
                                driverName AS Winner
                            FROM
                                data
                            WHERE
                                positionOrder = 1 AND {where}
                            GROUP BY Winner
                            ORDER BY COUNT(positionOrder) DESC
                        """

                        # Execute the query
                        most_winner = duckdb_connection.execute(query_most_winner).df()
                        if not most_winner.empty:
                            winner = most_winner.loc[0,'Winner']
                            totalWin = most_winner.loc[0,'TotalWin']
                        else:
                            winner = ''
                            totalWin = ''
                        component("Most Winning Racer",winner, totalWin)
                    with col7:
                
                ##################################################################################################
                ##                                                                                              ##
                ##                                   Most Participating Racer                                   ##
                ##                                                                                              ##
                ##################################################################################################
                        query_most_participating = f"""
                            SELECT
                                COUNT(driverName) AS MaxParticipation,
                                driverName AS MostParticipating
                            FROM
                                data
                            WHERE {where}
                            GROUP BY driverName
                            ORDER BY MaxParticipation DESC
                            LIMIT 1
                        """

                        # Execute the query
                        most_participating = duckdb_connection.execute(query_most_participating).df()
                        if not most_participating.empty:
                            most_participating_racer = most_participating.loc[0, 'MostParticipating']
                            participation_count = most_participating.loc[0, 'MaxParticipation']
                        else:
                            most_participating_racer = '' 
                            participation_count = ''  

                        component("Most Participating Racer", most_participating_racer, participation_count)
                    with col8:

                ##################################################################################################
                ##                                                                                              ##
                ##                                   Top Speed Record (Driver)                                  ##
                ##                                                                                              ##
                ##################################################################################################

                        query_top_speed = f"""
                            SELECT
                                MAX(fastestLapSpeed) AS MaxSpeed,
                                driverName AS MaxSpeedDriver
                            FROM 
                                data
                            WHERE {where}
                            GROUP BY driverName
                            ORDER BY MaxSpeed DESC
                            LIMIT 1
                            """
                        top_speed = duckdb_connection.execute(query_top_speed).df()
                        component("Top Speed Record",top_speed.loc[0,'MaxSpeedDriver'] if top_speed['MaxSpeed'].notna().any() else '', str(top_speed.loc[0, 'MaxSpeed']) + ' Km/h' if top_speed['MaxSpeed'].notna().any() else '')
                with st.container():
                    st.markdown("<br><br>",unsafe_allow_html=True)
                    col1,col2,col_3 = st.columns(3)
                    with col1:

                ##################################################################################################
                ##                                                                                              ##
                ##                                  Where to Find Good Drivers                                  ##
                ##                                                                                              ##
                ##################################################################################################

                        driver_nationality_query = f"""
                            SELECT 
                                driverNationality AS Nationality,
                                COUNT(DISTINCT driverName) AS Count,
                                (COUNT(DISTINCT driverName) * 100.0 / Total) AS Percentage

                            FROM
                                data,
                                (SELECT COUNT(DISTINCT driverName) AS Total 
                                FROM data 
                                WHERE {where})

                            WHERE {where}
                            GROUP BY driverNationality, Total
                            ORDER BY Percentage DESC
                            LIMIT 4
                            """

                        driver_nationality = duckdb_connection.execute(driver_nationality_query).df()
                        labels = driver_nationality['Nationality']
                        values = driver_nationality['Percentage']
                        # Use `hole` to create a donut-like pie chart
                        pie(labels,values,'Where to Find Good Drivers')
                    with col2:
                            
                ##################################################################################################
                ##                                                                                              ##
                ##                                         Total Driver                                         ##
                ##                                                                                              ##
                ##################################################################################################     

                            # Using string formatting (be cautious about SQL injection)
                            query = f"""
                                SELECT
                                    COUNT(DISTINCT driverName) AS Driver,
                                    year as Season
                                FROM
                                    data

                                WHERE {where}
                                GROUP BY year
                                ORDER BY year
                            """
                            # Execute the query
                            total_drivers_years = duckdb_connection.execute(query).df()
                            plot(total_drivers_years, x="Season", y="Driver", title='Total Driver')
                    with col_3:

                ##################################################################################################
                ##                                                                                              ##
                ##                            Starting Position Affect Result (Driver)                          ##
                ##                                                                                              ##
                ##################################################################################################

                        starting_position_affect_result_query = f"""
                            SELECT
                                startingPosition AS 'Starting Position', 
                                driverName AS DriverName,
                                points AS Points
                            FROM
                                data
                            WHERE {where}
                            GROUP BY startingPosition, raceId, driverName, points
                        """
                        starting_position_affect_result = duckdb_connection.execute(starting_position_affect_result_query).df()
                        scatter(starting_position_affect_result, x="Starting Position", y="Points",marker_color='DriverName',title='How Starting Position Duration Affect Result')
                with st.container():
                    st.markdown("<br><br>",unsafe_allow_html=True)
                    col1,col2,col3 = st.columns(3)
                    with col1:

                ##################################################################################################
                ##                                                                                              ##
                ##                                          Top Racers                                          ##
                ##                                                                                              ##
                ##################################################################################################

                        top_racers_with_points_query = f"""
                            SELECT
                                driverName AS Name,
                                driverNationality AS Nationality,
                                SUM(points) AS Points
                            FROM
                                data
                            WHERE {where}
                            GROUP BY
                                driverName, driverNationality
                            ORDER BY
                                Points DESC
                            """
                        top_racers_with_points = duckdb_connection.execute(top_racers_with_points_query).df()
                        fig = ff.create_table(top_racers_with_points.head(10), height_constant=40)
                        fig.layout.margin.update({'t':75})
                        fig.layout.update({'title': 'Top 10 Racers','title_x':0.3})
                        st.plotly_chart(fig, use_container_width=True)
                    with col2:
                ##################################################################################################
                ##                                                                                              ##
                ##                            Most Reason Driver Don't Finished Race                            ##
                ##                                                                                              ##
                ##################################################################################################
                        reason_driver_not_finish_races_query = f"""
                            SELECT 
                                status as Status,
                                COUNT(driverName) AS Driver
                            FROM
                                data
                            WHERE
                                status IN ('Accident','Engine', 'Did not qualify', 'Collision', 'Gearbox', 'Spun off', 'Suspension', 'Did not prequalify', 'Transmission', 'Electrical')
                                AND {where}
                            GROUP BY status
                            ORDER BY Driver ASC
                            """
                        reason_driver_not_finish_races = duckdb_connection.execute(reason_driver_not_finish_races_query).df()
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
                            title_x=0.1,
                            clickmode='event+select'
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    with col3:

                ##################################################################################################
                ##                                                                                              ##
                ##                                   Finished Race (%) Driver                                   ##
                ##                                                                                              ##
                ##################################################################################################
                        finished_race_query = f"""
                            SELECT 
                                (SELECT COUNT(driverName) FROM data) AS All_Drivers,
                                (COUNT(driverName) * 100.0 / (SELECT COUNT(driverName) FROM data WHERE {where})) AS Percentage_Finished
                            FROM
                                data
                            WHERE status IN ('Finished') 
                                AND {where};
                        """
                        finished_race = duckdb_connection.execute(finished_race_query).df()
                        gauge(finished_race.loc[0,'Percentage_Finished']," %","Finished Race (%)")

                ##################################################################################################
                ##                                                                                              ##
                ##                                      Accident (%) Driver                                     ##
                ##                                                                                              ##
                ##################################################################################################
                        accident_race_query = f"""
                            SELECT 
                                (SELECT COUNT(driverName) FROM data) AS All_Drivers,
                                (COUNT(driverName) * 100.0 / (SELECT COUNT(driverName) FROM data WHERE {where})) AS Percentage_Accident
                            FROM
                                data
                            WHERE status IN ('Accident')
                                AND {where};
                        """
                        accident_race = duckdb_connection.execute(accident_race_query).df()
                        gauge(accident_race.loc[0,'Percentage_Accident']," %","Accident (%)")
                    #with col4:

                ##################################################################################################
                ##                                                                                              ##
                ##                             How Pit Stop Duration Affect Result                              ##
                ##                                                                                              ##
                ##################################################################################################
                    #    # Your SQL query
                    #    duration_affect_result_query = f"""
                    #        SELECT duration AS Duration,
                    #            driverName AS DriverName,
                    #            points AS Points
                    #        FROM data
                    #        WHERE {where}
                    #        GROUP BY duration, raceId, driverName, points
                    #    """
#
                    #    # Execute the query and fetch the results into a DataFrame
                    #    duration_affect_result = duckdb_connection.execute(duration_affect_result_query).df()
#
                    #    # Create a scatter plot using plotly express
                    #    scatter(duration_affect_result, x="Duration", y="Points",title='How Pit Stop Duration Affect Result',marker_color='DriverName')
#
                ##################################################################################################
                ##                                                                                              ##
                ##                          Tab 2: Is for teams                                                 ##
                ##                                                                                              ##
                ##################################################################################################
    with tab_2:
        with st.container():
            cols = st.columns(5)
            where_team_dict = {}
            for i in range(len(cols)):
                with cols[i]:
                    if i == 0:
                        expander_label = "Race_Name"
                        column_data = data['GPName']
                        text = 'team_'
                    elif i == 1:
                        expander_label = "Driver_Name"
                        column_data = data['driverName']
                        text = 'team_'
                    elif i == 2:
                        expander_label = "Driver_Nationality"
                        column_data = data['driverNationality']
                        text = 'team_'
                    elif i == 3:
                        expander_label = "Brand_Name"
                        column_data = data['brand']
                        text = 'team_'
                    elif i == 4:
                        expander_label = "Brand_Nationality"
                        column_data = data['brandNationality']
                        text = 'team_brand_'

                    with st.expander(expander_label.replace('_',' ')):
                        # Get unique items in the column
                        unique_items = column_data.unique()

                        # Display the selected items
                        if f"all_option_{text}{expander_label}" not in st.session_state:
                            st.session_state[f"all_option_{text}{expander_label}"] = True
                            st.session_state[f"selected_options_{text}{expander_label}"] = list(unique_items)

                        # Display the selected items
                        all = st.checkbox("Select all", key=f"all_option_{text}{expander_label}",on_change= partial(check_change, text, expander_label, column_data))
                        options = st.multiselect('',list(unique_items),key=f"selected_options_{text}{expander_label}", on_change=partial(multi_change, text, expander_label, column_data))
                        where_team_dict[expander_label]= st.session_state[f'selected_options_{text}{expander_label}']

                        st.markdown(
                            """
                            <style>
                                [data-testid="stExpanderDetails"] {
                                    max-height: 200px;
                                    overflow-y: auto;
                                }
                            </style>
                            """,
                            unsafe_allow_html=True
                        )
            col1,col2,col3 = st.columns([3,3,8])
            with col1:
                ##################################################################################################
                ##                                                                                              ##
                ##                                        Teams Slider                                          ##
                ##                                                                                              ##
                ##################################################################################################
                year_values_brand = st.slider(
                '**Seasons:**',
                1950, 2023, (1950, 2023),
                key ='teams_slider')
            # Validate and use the selected years
            if year_values_brand[0] <= year_values_brand[1]:
                selected_start_year, selected_end_year = year_values_brand
                driverNamesTeam = parameterize_SQL_in_statement(where_team_dict["Driver_Name"])
                driverNationalitiesTeam = parameterize_SQL_in_statement(where_team_dict["Driver_Nationality"])
                brandsTeam =  parameterize_SQL_in_statement(where_team_dict["Brand_Name"])
                brandNationalitiesTeam = parameterize_SQL_in_statement(where_team_dict["Brand_Nationality"])
                raceNamesTeam = parameterize_SQL_in_statement(where_team_dict["Race_Name"])
                where_team = f"""
                    (year BETWEEN {selected_start_year} AND {selected_end_year})
                    AND driverName IN {driverNamesTeam}
                    AND driverNationality IN {driverNationalitiesTeam}
                    AND brand IN {brandsTeam}
                    AND brandNationality IN {brandNationalitiesTeam}
                    AND GPName IN {raceNamesTeam}
                """
                with col2:
                    col4,col5 = st.columns(2)
                    with col4:

                ##################################################################################################
                ##                                                                                              ##
                ##                                         Total Brands                                         ##
                ##                                                                                              ##
                ##################################################################################################

                        total_brands = duckdb.sql(f"""
                            SELECT COUNT(DISTINCT brand) AS Brand From data
                            WHERE {where_team}
                        """).df()
                        component2("Total Brands", total_brands.loc[0,'Brand'])
                    with col5:
                    
                ##################################################################################################
                ##                                                                                              ##
                ##                                          Total Races                                         ##
                ##                                                                                              ##
                ##################################################################################################

                            total_races = f"""
                                SELECT
                                    year,
                                    COUNT(DISTINCT GPName) AS total_GP
                                FROM
                                    data
                                WHERE {where_team}
                                GROUP BY year
                            """
                            result_df = duckdb_connection.execute(total_races).df()
                            # Calculate the total GP count by summing the counts for each year
                            total_gp_count = result_df['total_GP'].sum()
                            component2("Total Races", total_gp_count)
                with col3:
                    col6,col7,col8 = st.columns(3)
                    with col6:

                ##################################################################################################
                ##                                                                                              ##
                ##                                      Most Winning Brand                                      ##
                ##                                                                                              ##
                ##################################################################################################

                        most_winning_brand_query=f"""
                            SELECT
                                COUNT(positionOrder) AS TotalWin,
                                brand AS Brand
                            FROM
                                data
                            WHERE
                                positionOrder = 1 AND {where_team}
                            GROUP BY Brand
                            ORDER BY COUNT(positionOrder) DESC
                        """
                        most_winning_brand = duckdb_connection.execute(most_winning_brand_query).df()
                        if not most_winning_brand.empty:
                            mostWinningBrand = most_winning_brand.loc[0,'Brand']
                            totalBrandWin = most_winning_brand.loc[0,'TotalWin']
                        else:
                            mostWinningBrand = ''
                            totalBrandWin = ''
                        component("Most Winning Brand",mostWinningBrand, totalBrandWin)
                    with col7:

                ##################################################################################################
                ##                                                                                              ##
                ##                                   Most Participating Brand                                   ##
                ##                                                                                              ##
                ##################################################################################################

                        most_participating_brand_query=f"""
                            SELECT
                                COUNT(brand) AS MaxParticipation,
                                brand AS MostParticipating
                            FROM
                                data
                            WHERE {where_team}
                            GROUP BY brand
                            ORDER BY MaxParticipation DESC
                            LIMIT 1
                        """
                        most_participating_brand = duckdb_connection.execute(most_participating_brand_query).df()
                        if not most_participating_brand.empty:
                            mostBrandParticipating = most_participating_brand.loc[0,'MostParticipating']
                            maxBrandParticipating = most_participating_brand.loc[0,'MaxParticipation']
                        else:
                            mostBrandParticipating = ''
                            maxBrandParticipating = ''
                        component("Most Participating Brand", mostBrandParticipating, maxBrandParticipating)
                    with col8:

                ##################################################################################################
                ##                                                                                              ##
                ##                                       Top Speed Brand                                        ##
                ##                                                                                              ##
                ##################################################################################################

                        top_speed_brand_query = f"""
                            SELECT
                                MAX(fastestLapSpeed) AS MaxSpeed,
                                brand AS MaxSpeedBrand
                            FROM 
                                data
                            WHERE {where_team}
                            GROUP BY brand
                            ORDER BY MaxSpeed DESC
                            LIMIT 1
                        """
                        top_speed_brand = duckdb_connection.execute(top_speed_brand_query).df()
                        component("Top Speed Record (Brand)",top_speed_brand.loc[0,'MaxSpeedBrand'] if top_speed_brand['MaxSpeed'].notna().any() else '', str(top_speed_brand.loc[0,'MaxSpeed']) + ' Km/h' if top_speed_brand['MaxSpeed'].notna().any() else '')
            

                with st.container():
                    st.markdown("<br><br>",unsafe_allow_html=True)
                    col1,col2,col_3 = st.columns(3)
                    with col1:

                ##################################################################################################
                ##                                                                                              ##
                ##                                   Where to Find Good Brand                                   ##
                ##                                                                                              ##
                ##################################################################################################

                        brand_nationality_query = f"""
                            SELECT 
                                brandNationality AS Nationality,
                                COUNT(DISTINCT brand) AS Count,
                                (COUNT(DISTINCT brand) * 100.0 / Total) AS Percentage
                                
                            FROM
                                data,
                                (SELECT COUNT(DISTINCT brand) AS Total 
                                FROM data 
                                WHERE {where_team})

                            WHERE {where_team}
                            GROUP BY brandNationality, Total
                            ORDER BY Percentage DESC
                            LIMIT 4
                            """

                        brand_nationality = duckdb_connection.execute(brand_nationality_query).df()
                        labels = brand_nationality['Nationality']
                        values = brand_nationality['Percentage']
                        pie(labels,values,'Where to Find Good Brand')
                    with col2:

                ##################################################################################################
                ##                                                                                              ##
                ##                                   Total Driver (Team Tabs)                                   ##
                ##                                                                                              ##
                ##################################################################################################
                        # Using string formatting (be cautious about SQL injection)
                        total_drivers_years_team_query = f"""
                            SELECT
                                COUNT(DISTINCT brand) AS Brand,
                                year as Season
                            FROM
                                data
                            WHERE {where_team}
                            GROUP BY year
                            ORDER BY year
                        """
                        # Execute the query
                        total_drivers_years_team = duckdb_connection.execute(total_drivers_years_team_query).df()
                        plot(total_drivers_years_team, x="Season", y="Brand", title='Total Brand')
                    with col_3:

                ##################################################################################################
                ##                                                                                              ##
                ##                          Starting Position Affect Result for Brands                          ##
                ##                                                                                              ##
                ##################################################################################################

                        starting_position_affect_result_query = f"""
                            SELECT
                                startingPosition AS 'Starting Position', 
                                brand AS Brand,
                                points AS Points
                            FROM data
                            WHERE {where_team}
                            GROUP BY startingPosition, raceId, brand, points
                        """
                        starting_position_affect_result = duckdb_connection.execute(starting_position_affect_result_query).df()
                        scatter(starting_position_affect_result, x="Starting Position", y="Points",marker_color='Brand',title='How Starting Position Duration Affect Result')
                with st.container():
                    st.markdown("<br><br>",unsafe_allow_html=True)
                    col1, col2, col3 = st.columns(3)
                    with col1:
                
                ##################################################################################################
                ##                                                                                              ##
                ##                                          Top Brands                                          ##
                ##                                                                                              ##
                ##################################################################################################

                        top_brands_with_points_query = f"""
                            SELECT
                                brand AS Name,
                                brandNationality AS Nationality,
                                SUM(points) AS Points
                            FROM
                                data
                            WHERE {where_team}
                            GROUP BY
                                brand, brandNationality
                            ORDER BY
                                Points DESC
                        """
                        top_brands_with_points = duckdb_connection.execute(top_brands_with_points_query).df()
                        fig = ff.create_table(top_brands_with_points.head(10), height_constant=50)
                        fig.layout.margin.update({'t':75})
                        fig.layout.update({'title': 'Top 10 Brands','title_x':0.3})
                        st.plotly_chart(fig, use_container_width=True)

                    
                    

                    with col2:

                ##################################################################################################
                ##                                                                                              ##
                ##                                  Brand Performance Status                                    ##
                ##                                                                                              ##
                ##################################################################################################

                        brand_performance_status_query = f"""
                            SELECT 
                                status as Status,
                                COUNT(brand) AS Brand
                            FROM
                                data
                            WHERE
                                status IN ('Finished','Accident','Engine', 'Did not qualify', 'Collision', 'Gearbox', 'Spun off', 'Did not prequalify', 'Transmission')
                                AND {where_team}
                            GROUP BY status
                            ORDER BY Brand ASC
                        """
                        brand_performance_status = duckdb_connection.execute(brand_performance_status_query).df()
                        fig = go.Figure()
                        fig.add_trace(go.Bar(
                            y=brand_performance_status['Status'],
                            x=brand_performance_status['Brand'],
                            orientation='h'
                        ))
                        fig.update_layout(
                            title='Brands Performance Status',
                            xaxis_title='Brand',
                            yaxis_title='Status',
                            title_x=0.3,
                            clickmode='event+select'
                        )
                        fig.update_xaxes(tickformat=".2s")
                        st.plotly_chart(fig, use_container_width=True)
                    

                    with col3:
            
                ##################################################################################################
                ##                                                                                              ##
                ##                                     Finished Race (%) Brand                                  ##
                ##                                                                                              ##
                ##################################################################################################
                        finished_race_brand_query = f"""
                            SELECT 
                                (SELECT COUNT(brand) FROM data WHERE {where_team}) AS All_Brands,
                                (COUNT(brand) * 100.0 / (SELECT COUNT(brand) FROM data WHERE {where_team})) AS Percentage_Finished
                            FROM
                                data
                            WHERE status IN ('Finished') AND {where_team};

                        """
                        finished_race_brand = duckdb_connection.execute(finished_race_brand_query).df()
                        gauge(finished_race_brand.loc[0,'Percentage_Finished']," %","Finished Race (%)")

                ##################################################################################################
                ##                                                                                              ##
                ##                                       Accident (%) Brand                                     ##
                ##                                                                                              ##
                ##################################################################################################

                        accident_race_brand_query = f"""
                            SELECT 
                                (SELECT COUNT(brand) FROM data) AS All_Brands,
                                (COUNT(brand) * 100.0 / (SELECT COUNT(brand) FROM data WHERE {where_team})) AS Percentage_Accident
                            FROM
                                data
                            WHERE status IN ('Accident') AND {where_team};

                        """
                        accident_race_brand = duckdb_connection.execute(accident_race_brand_query).df()
                        gauge(accident_race_brand.loc[0,'Percentage_Accident']," %","Accident (%)")

                ##################################################################################################
                ##                                                                                              ##
                ##                                                                                              ##
                ##                                                                                              ##
                ##################################################################################################