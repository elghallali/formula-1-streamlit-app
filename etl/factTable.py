import pandas as pd
import numpy as np
import os


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

#############################################################################
###
###
#############################################################################
def factTable():

    races['GPName'] = races['name']

    constructors['brandNationality']= constructors['nationality']
    constructors['brand']= constructors['name']

    drivers['driverName']= drivers['forename']+ ' ' + drivers['surname']
    drivers['driverNationality']= drivers['nationality']


    df = pd.merge(results, races[['raceId','year','GPName','round']], on='raceId', how='left')
    df = pd.merge(df, drivers[['driverId', 'driverName','driverNationality']], on='driverId', how='left')
    df = pd.merge(df, constructors[['constructorId', 'brand', 'brandNationality']], on='constructorId', how='left')
    df = pd.merge(df, status, on='statusId', how='left')
    df = df.drop(['resultId','raceId','constructorId', 'driverId', 'statusId', 'number', 'position', 'positionText', 'laps', 'fastestLap','grid'], axis=1)
    df = df.sort_values(by=['year', 'round', 'positionOrder'], ascending=[False, True, True])
    df.time.replace('\\N',np.nan, inplace=True)
    df.milliseconds.replace('\\N',np.nan, inplace=True)
    df.fastestLapTime.replace('\\N',np.nan, inplace=True)
    df.fastestLapSpeed.replace('\\N',np.nan, inplace=True)
    df.fastestLapSpeed = df.fastestLapSpeed.astype(float)
    df.milliseconds =df.milliseconds.astype(float)
    return df