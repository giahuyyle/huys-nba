from flask import Flask, request, jsonify
from flask_cors import CORS
from database.queries_players import get_players_by_name
import os, sqlite3

app = Flask(__name__)

db_path = os.getenv("OUTPUT_DB")

def test_query(columns: list[str], rows: list[str]) -> dict:
    """
    takes two lists of teams, and return a dictionary of players for each column, row
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
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
                new_key = str((row, col))
                players[new_key] = result
            except sqlite3.Error as e:
                print(f"An error occurred: {e}")
                continue
    for key, val in players.items():
        players[key] = [item[0] for item in val]

    conn.close()
    return jsonify(players)

@app.route('/')
def home():
    return "Welcome to the NBA Player Data API!"

@app.route('/players/<player_name>', methods=["GET"])
def get_player_list(player_name):
    return get_players_by_name(player_name)

@app.route('/common_players', methods=["GET"])
def get_common_players():
    rows = request.args.get('rows', '')
    cols = request.args.get('cols', '')
    # split the comma separated values
    rows = rows.split(",")
    cols = cols.split(",")
    return test_query(cols, rows)


if __name__ == '__main__':
    # Enable CORS for all routes
    CORS(app, origins=["http://localhost:5173"])
    
    # Run the Flask app
    app.run(debug=True)