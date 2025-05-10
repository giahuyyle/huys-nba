"""
Load data into one single SQLite database from .csv files
Each .csv file is one table in the DB
"""

import os
import pandas as pd
import sqlite3
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Directory for CSV files
csv_directory = os.getenv("CSV_DIR")
output_database = os.getenv("OUTPUT_DB")  # Path to the single output .db file

# Create a single SQLite DB connection
conn = sqlite3.connect(output_database)

for filename in os.listdir(csv_directory):
    if filename.endswith('.csv'):
        # Use the filename (without extension) as the table name
        table_name = os.path.splitext(filename)[0]  # e.g., "lakers"
        csv_path = os.path.join(csv_directory, filename)

        # Read CSV into DataFrame
        df = pd.read_csv(csv_path)

        # Rename the last column to 'additionals' if its name is '-9999'
        if df.columns[-1] == '-9999':
            df.rename(columns={df.columns[-1]: 'additionals'}, inplace=True)

        # Save the DataFrame into the DB as a table (overwrite if exists)
        df.to_sql(table_name, conn, if_exists='replace', index=False)

        print(f'Successfully stored {table_name} into {output_database}')

# Close the database connection
conn.close()