import os
import pandas as pd
import sqlite3


# Directory for CSV files
csv_directory = '/Users/huylegia/Coding-Projects/Python/nba-project/server/raw-data/teams'

for filename in os.listdir(csv_directory):
    print(filename)