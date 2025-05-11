import sqlite3, os

columns = [
    "lakers",
    "clippers",
    "warriors"
]

rows = [
    "celtics",
    "nets",
    "cavaliers",
]

db_path = os.getenv("OUTPUT_DB")
conn = sqlite3.connect("/Users/huylegia/Coding-Projects/Python/nba-project/server/raw-data/players.db")
cursor = conn.cursor()

def test_query(columns: list[str], rows: list[str]) -> dict:
    """
    takes two lists of teams, and return a dictionary of players for each column, row
    """
    players = {}
    for row in rows:
        for col in columns:
            try:
                query = f"""SELECT {row}.additionals
                FROM {row}, {col}
                WHERE {row}.additionals = {col}.additionals;
                """
                cursor.execute(query)
                result = cursor.fetchall()
                players[(row, col)] = result
            except sqlite3.Error as e:
                print(f"An error occurred: {e}")
                continue
    return players

players = test_query(columns, rows)

for key, val in players.items():
    print(f"{key}: {val}\n")

conn.close()