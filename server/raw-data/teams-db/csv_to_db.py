import os
import pandas as pd
import sqlite3
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Directory for CSV files
csv_directory = os.getenv("CSV_DIR")
output_directory = os.getenv("OUTPUT_DIR")

for filename in os.listdir(csv_directory):
    # print(filename)
    if filename.endswith('.csv'):
        # print()
        team_name = os.path.splitext(filename)[0]  # e.g., "lakers"
        csv_path = os.path.join(csv_directory, filename)
        # print(csv_path)

        # Read CSV into DataFrame
        df = pd.read_csv(csv_path)

        # Create a SQLite DB for the team
        db_path = os.path.join(output_directory, f'{team_name}.db')
        # print(db_path)

        conn = sqlite3.connect(db_path)

        # Save the DataFrame into the DB (overwrite if exists)
        df.to_sql('players', conn, if_exists='replace', index=False)
        conn.close()

        print(f'Successfully stored {team_name} into {db_path}\n')
        # print()