import datetime
from dateutil.relativedelta import relativedelta
from pydsstools.heclib.dss import HecDss
import pandas as pd
import numpy as np
import time
import pickle

def single_file_pull(dss_file, target_ts_list, scenario_name):

    startDate = "31OCT1921 00:00:00"
    endDate = "30SEP2021 00:00:00"
    startDate_1 = datetime.date(1921, 10, 31)

    fid = HecDss.Open(dss_file)

    # getPathnamesDict returns a dict of pathnames. All CalSim outputs are contained in 'TS'
    pathNamesDict = fid.getPathnameDict()
    pathNames = np.array(list(pathNamesDict.values())[0])

    dfPaths = pd.DataFrame(pathNames, columns=["AllPaths"])
    dfPaths[['blank1', 'A', 'B', 'C', 'D', 'E', 'F', 'blank2']] = dfPaths['AllPaths'].str.split("/", expand=True)
    dfPaths = dfPaths.drop(columns=['AllPaths', 'blank1', 'blank2'])

    dfPaths = dfPaths.sort_values(by=['B', 'D'])
    dfPaths = dfPaths.drop_duplicates(subset=['B', 'C'])
    dfPaths = dfPaths.reset_index()
    dfPaths.drop('index', axis=1, inplace=True)
    len(pd.unique(dfPaths['B']))

    # use our list of variables to search the DSS File. For CS3, b parts are unique
    target_path_list = []
    for b_part in target_ts_list:
        c_part = dfPaths[dfPaths['B'] == b_part]['C'].iloc[0]
        target_pathName = f'/CALSIM/{b_part}/{c_part}//1MON/L2020A/'
        target_path_list.append(target_pathName)

    # Since we need units, keep this step separate from df creation for the moment
    ts_list = []
    unit_list = []
    for p in target_path_list:
        working_ts = fid.read_ts(p, window=(startDate, endDate), trim_missing=False)
        ts_list.append(working_ts)
        unit_list.append(working_ts.units)

    times = np.array([startDate_1])
    years = [startDate_1.year]
    months = [startDate_1.month]
    if startDate_1.month > 9:
        wy = [startDate_1.year + 1]
    else:
        wy = [startDate_1.year]

    if startDate_1.month < 3:
        dy = [startDate_1.year - 1]
    else:
        dy = startDate_1.year

    for i in range(1, len(ts_list[0].values)):
        current_time = times[i - 1] + relativedelta(days=+1) + relativedelta(months=+1) - relativedelta(days=+1)
        times = np.append(times, current_time)
        years = np.append(years, current_time.year)
        months = np.append(months, current_time.month)
        if current_time.month > 9:
            wy = np.append(wy, current_time.year + 1)
        else:
            wy = np.append(wy, current_time.year)

        if current_time.month < 3:
            dy = np.append(dy, current_time.year - 1)
        else:
            dy = np.append(dy, current_time.year)


    ## Add units to column titles and create duplicates of columns with swapped units

    # Add unit indicator in column name
    df_ts = pd.DataFrame(index=times)
    for t, ts in enumerate(target_ts_list):
        df_ts[f'{ts} ({unit_list[t]})'] = ts_list[t].values

    # Duplicate columns with other (cfs/taf) unit
    durations = [t.day for t in times]   # list of month durations for our timeframe of interest
    cfs_taf = np.multiply(durations, (24 * 3600 / 43560 / 1000))
    taf_cfs = np.divide((43560 * 1000 / 24 / 3600), durations)
    for series_name, series in df_ts.items():
        if series_name[-5:] == '(CFS)':
            flip_name = f'{series_name[:-5]}(TAF)'
            flip_series = np.multiply(series, cfs_taf)
            df_ts[flip_name] = flip_series
        elif series_name[-5:] == '(TAF)':
            flip_name = f'{series_name[:-5]}(CFS)'
            flip_series = np.multiply(series, cfs_taf)
            df_ts[flip_name] = flip_series
        else:
            pass

    df_ts.insert(0, 'DY', dy)
    df_ts.insert(0, 'WY', wy)
    df_ts.insert(0, 'Month', months)
    df_ts.insert(0, 'Year', years)
    df_ts.insert(0, 'Scenario', scenario_name)
    df_ts['Date'] = df_ts.index
    date_temp = df_ts.pop('Date')
    df_ts.insert(0, 'Date', date_temp)

    return df_ts