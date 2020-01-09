#!/usr/bin/env python
"""
This script processes the data needed for analysis,
putting it into the same format and merging it
all together
"""
import os
import pandas as pd
import json
import src.utilities as utils


def clean_ons_time_series(key, dataset_id, timeseries_id):
    """
    Opens raw data (in json) as downloaded from ONS API
    and puts it into a clean monthly and tidy format.
    """
    config = utils.read_config()
    raw_file_name = os.path.join(config['data']['rawFilePath'],
                                 key+'_data.txt')
    with open(raw_file_name) as json_file:
        data = json.load(json_file)
    title_text = data['description']['title']
    print("Code output:\n")
    print(title_text)
    # Check if monthly data exist; if not go on to quarterly
    if data['months']:
        df = pd.DataFrame(pd.io.json.json_normalize(data['months']))
        df['date'] = pd.to_datetime(df['date']) + pd.offsets.MonthEnd(0)
        df = df.set_index('date')
        df['value'] = df['value'].astype(float)
    else:
        # Assume quarterly
        df = pd.DataFrame(pd.io.json.json_normalize(data['quarters']))
        df['date'] = (pd.to_datetime(df['date'].str.replace(' ', '')) +
                      pd.offsets.QuarterEnd(0))
        df = df.set_index('date')
        df['value'] = df['value'].astype(float)
        # Upscale to monthly
        df = df['value'].resample('M').interpolate(method='time')
        df = pd.DataFrame(df)
    cols_to_drop = [x for x in df.columns if x != 'value']
    df = df.drop(cols_to_drop, axis=1)
    df['timeseries_id'] = timeseries_id
    df['dataset_id'] = dataset_id
    df['value_name'] = key
    return df


def create_clean_data():
    """
    Master function which takes all raw series, cleans them,
    and outputs to a flat file
    """
    # Get config file
    config = utils.read_config()
    # Create empty list for vector of dataframes
    df_vec = []
    for key in list(config['timeSeries'].keys()):
        df_vec.append(clean_ons_time_series(key, *config['timeSeries'][key]))
    # Put this into tidy format
    df = pd.concat(df_vec, axis=0)
    # Write it to clean data
    df.to_csv(os.path.join(config['data']['clnFilePath'], 'ts_data.csv'))


if __name__ == "__main__":
    # Master function
    create_clean_data()
