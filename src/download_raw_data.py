#!/usr/bin/env python
"""
This script downloads the data needed for analysis from the ONS
API. It uses series that are in the yaml config file.
"""
import requests
import os
import pandas as pd
import yaml
import json


def grab_ons_time_series_data(dataset_id, timeseries_id):
    """ Grabs specified time series from the ONS API. """
    api_endpoint = "https://api.ons.gov.uk/"
    api_params = {
                  'dataset': dataset_id,
                  'timeseries': timeseries_id
                  }
    url = (api_endpoint +
           '/'.join([x+'/'+y for x, y in zip(api_params.keys(),
                                             api_params.values())][::-1]) +
           '/data')
    return requests.get(url).json()

# Read in config file
config = {k: v for d in yaml.load(open('config.yaml')) for k, v in d.items()}

# Retrieve all series and save to file with value name/key in title
for i, key in enumerate(config['timeSeries'].keys()):
    print('Downloading '+key)
    data = grab_ons_time_series_data(*config['timeSeries'][key])
    output_dir = os.path.join(config['data']['rawFilePath'], key+'_data.txt')
    with open(output_dir, 'w') as outfile:
        json.dump(data, outfile)
