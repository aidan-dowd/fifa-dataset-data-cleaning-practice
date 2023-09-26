#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 11:05:30 2023

@author: aidandowd
"""

import pandas as pd
import numpy as np
import re

fifa = pd.read_csv(par, low_memory=False)
colnames = list(fifa.columns)
# fifa.info()

# Transform "Joined" column from object to datetime

fifa.Joined = pd.to_datetime(fifa["Joined"], format = "%b %d, %Y")
fifa.Joined = fifa["Joined"].apply(lambda x: x.date())

# Separate "Joined column into Year, Month, and Day column
fifa["Joined"] = fifa["Joined"].astype(str)
fifa[["Year", "Month", "Day"]] = fifa["Joined"].str.split("-", expand = True)

# Change "Height" and "Weight" dtypes
fifa["Height"].value_counts()

fifa.Height = fifa["Height"].astype(str)
fifa[["feet", "inches"]] = fifa["Height"].str.strip('"').str.split("'", expand = True)
fifa.Height = fifa.feet.astype(int)*12  + fifa.inches.astype(int)

fifa.Weight = fifa.Weight.astype(str).str.strip("lbs")
fifa.Weight = fifa.Weight.astype(int)

# Seperating "Team & Contract" Column into "Team" and "Contract

fifa["Team & Contract"] = fifa["Team & Contract"].astype(str)
fifa["Team & Contract"] = fifa["Team & Contract"].str.strip("\n").str.split("\n")
fifa[["Team", "Contract"]] = pd.DataFrame(fifa["Team & Contract"].tolist())
fifa = fifa.drop("Team & Contract", axis=1)


# Changing the "Team" for each free agent player
fifa.loc[fifa['Contract'] == 'Free', 'Team'] = 'None'

#Transforming data types of numerical data columns
def actual_value(money: str):
    value = pd.to_numeric(re.findall(pattern=r"\d+\.?\d+|\d", string=money))[0]
    if value == np.nan: value = 0
    if "M" in money:
        value *= 1000000
    elif "K" in money:
        value *= 1000
    return str(int(value))
    

fifa.Value = pd.to_numeric(fifa.Value.apply(actual_value))
fifa.Wage = pd.to_numeric(fifa.Wage.apply(actual_value))
fifa['Release Clause'] = pd.to_numeric(fifa['Release Clause'].apply(actual_value))

fifa.Hits = pd.to_numeric(fifa.Hits.apply(actual_value))





