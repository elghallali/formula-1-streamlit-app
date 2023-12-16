import pandas as pd
import numpy as np
import os

from etl.extracts import Extracts
from etl.transforms import Transforms

#############################################################################
###                                                                       ###
###                             Extracts data                             ###
###                                                                       ###
#############################################################################

circuits = Extracts(os.getcwd() +'/data/circuits.csv').load_data()
laptimes = Extracts(os.getcwd() +'/data/lap_times.csv').load_data()
pitstops = Extracts(os.getcwd() +'/data/pit_stops.csv').load_data()
seasons = Extracts(os.getcwd() +'/data/seasons.csv').load_data()
status = Extracts(os.getcwd() +'/data/status.csv').load_data()
constructor_standings = Extracts(os.getcwd() +'/data/constructor_standings.csv').load_data()
constructors = Extracts(os.getcwd() +'/data/constructors.csv').load_data()
driver_standings = Extracts(os.getcwd() +'/data/driver_standings.csv').load_data()
drivers = Extracts(os.getcwd() +'/data/drivers.csv').load_data()
races = Extracts(os.getcwd() +'/data/races.csv').load_data()
constructor_results = Extracts(os.getcwd() +'/data/constructor_results.csv').load_data()
results = Extracts(os.getcwd() +'/data/results.csv').load_data()
qualifying = Extracts(os.getcwd() +'/data/qualifying.csv').load_data()

#############################################################################
###                                                                       ###
###                            Transform Data                             ###
###                                                                       ###
#############################################################################
def factTable():

    races[0]['GPName'] = races[0]['name']

    constructors[0]['brandNationality']= constructors[0]['nationality']
    constructors[0]['brand']= constructors[0]['name']

    drivers[0]['driverName']= drivers[0]['forename']+ ' ' + drivers[0]['surname']
    drivers[0]['driverNationality']= drivers[0]['nationality']
    qualifying[0]['startingPosition'] = qualifying[0]['position']
    df_pitstop = pitstops[0].groupby(['raceId', 'driverId']).agg(duration=('milliseconds', 'sum')).reset_index()
    
    df = Transforms(results[0], param0=races[0][['raceId','year','GPName','round']],param1='raceId',how='left').transform_state()
    df = Transforms(df, param0=drivers[0][['driverId', 'driverName','driverNationality']], param1='driverId', how='left').transform_state()
    df = Transforms(df, param0=constructors[0][['constructorId', 'brand', 'brandNationality']], param1='constructorId', how='left').transform_state()
    df = Transforms(df, param0=status[0], param1='statusId', how='left').transform_state()
    df = Transforms(df, param0=qualifying[0][['raceId', 'driverId','startingPosition']], param1=['raceId', 'driverId'], how='left').transform_state()
    df = Transforms(df, param0=df_pitstop[['raceId', 'driverId','duration']], param1=['raceId', 'driverId'], how='left').transform_state()
    df = df.drop(['number', 'position', 'positionText', 'laps', 'fastestLap','grid'], axis=1)
    df = df.sort_values(by=['year', 'round', 'positionOrder'], ascending=[False, True, True])
    df['driverName'] = df['driverName'].str.replace("'", "", regex=True)
    df.time.replace('\\N',np.nan, inplace=True)
    df.milliseconds.replace('\\N',np.nan, inplace=True)
    df.fastestLapTime.replace('\\N',np.nan, inplace=True)
    df.fastestLapSpeed.replace('\\N',np.nan, inplace=True)
    df.fastestLapSpeed = df.fastestLapSpeed.astype(float)
    df.milliseconds =df.milliseconds.astype(float)
    return df