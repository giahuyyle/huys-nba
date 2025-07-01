from flask import Flask, request, jsonify
from flask_cors import CORS
from .database.queries_players import get_players_by_name
from .database.queries_top10 import get_top_10, get_top_10_title
import os, sqlite3

app = Flask(__name__)

CORS(
    app, 
    resources={
        r"/*": {
            "origins": ["http://localhost:5173", "http://127.0.0.1:5173"],
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "expose_headers": ["Content-Range", "X-Content-Range"]
        }
     },
    supports_credentials=True
)

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

@app.route("/top10", methods=["GET"])
def get_top_10_today():
    """
    Fetch the top 10 players for today
    """
    date = request.args.get('date', '')
    top_10 = get_top_10(date)
    print(top_10)
    return jsonify(top_10)

@app.route("/top10/title", methods=["GET"])
def get_top_10_today_title():
    """
    Fetch the top 10 players for today
    """
    date = request.args.get('date', '')
    top_10 = get_top_10_title(date)
    return jsonify(top_10)

if __name__ == '__main__':
    # Enable CORS for all routes
    # Run the Flask app
    app.run(debug=True)