from flask import Flask
from flask_cors import CORS
#from test_query_sqlite3 import get_player_list
from database.queries_players import get_players_by_name

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the NBA Player Data API!"

@app.route('/players/<player_name>', methods=["GET"])
def get_player_list(player_name):
    return get_players_by_name(player_name)


if __name__ == '__main__':
    # Enable CORS for all routes
    CORS(app, origins=["http://localhost:5173"])
    
    # Run the Flask app
    app.run(debug=True)