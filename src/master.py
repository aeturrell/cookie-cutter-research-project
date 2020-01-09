#!/usr/bin/env python
"""
This is the master script for recreating the results

It imports each of the key other scripts and
runs them one by one.

Run the whole thing from the root directory 
to replicate all of the python analysis

"""

import src.download_raw_data as dl_raw
import src.create_clean_data as cln_data
import src.analysis as analysis

dl_raw.download_raw_data()
cln_data.create_clean_data()
analysis.analysis()

