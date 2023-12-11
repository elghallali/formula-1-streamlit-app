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

circuits = Extracts(os.getcwd() +'/data/circuits.csv','csv').load_data()
laptimes = Extracts(os.getcwd() +'/data/lap_times.csv','csv').load_data()
pitstops = Extracts(os.getcwd() +'/data/pit_stops.csv','csv').load_data()
seasons = Extracts(os.getcwd() +'/data/seasons.csv' ,'csv').load_data()
status = Extracts(os.getcwd() +'/data/status.csv','csv').load_data()
constructor_standings = Extracts(os.getcwd() +'/data/constructor_standings.csv','csv').load_data()
constructors = Extracts(os.getcwd() +'/data/constructors.csv','csv').load_data()
driver_standings = Extracts(os.getcwd() +'/data/driver_standings.csv','csv').load_data()
drivers = Extracts(os.getcwd() +'/data/drivers.csv','csv').load_data()
races = Extracts(os.getcwd() +'/data/races.csv','csv').load_data()
constructor_results = Extracts(os.getcwd() +'/data/constructor_results.csv','csv').load_data()
results = Extracts(os.getcwd() +'/data/results.csv','csv').load_data()
qualifying = Extracts(os.getcwd() +'/data/qualifying.csv','csv').load_data()

#############################################################################
###                                                                       ###
###                            Transform Data                             ###
###                                                                       ###
#############################################################################
def factTable():

    races['GPName'] = races['name']

    constructors['brandNationality']= constructors['nationality']
    constructors['brand']= constructors['name']

    drivers['driverName']= drivers['forename']+ ' ' + drivers['surname']
    drivers['driverNationality']= drivers['nationality']

    
    df = Transforms(results, param0=races[['raceId','year','GPName','round']],param1='raceId',how='left').transform_state()
    df = Transforms(df, param0=drivers[['driverId', 'driverName','driverNationality']], param1='driverId', how='left').transform_state()
    df = Transforms(df, param0=constructors[['constructorId', 'brand', 'brandNationality']], param1='constructorId', how='left').transform_state()
    df = Transforms(df, param0=status, param1='statusId', how='left').transform_state()
    df = df.drop(['resultId','raceId','constructorId', 'driverId', 'statusId', 'number', 'position', 'positionText', 'laps', 'fastestLap','grid'], axis=1)
    df = df.sort_values(by=['year', 'round', 'positionOrder'], ascending=[False, True, True])
    df.time.replace('\\N',np.nan, inplace=True)
    df.milliseconds.replace('\\N',np.nan, inplace=True)
    df.fastestLapTime.replace('\\N',np.nan, inplace=True)
    df.fastestLapSpeed.replace('\\N',np.nan, inplace=True)
    df.fastestLapSpeed = df.fastestLapSpeed.astype(float)
    df.milliseconds =df.milliseconds.astype(float)
    return df