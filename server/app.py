from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the NBA Player Data API!"

if __name__ == '__main__':
    # Enable CORS for all routes
    # CORS(app)
    
    # Run the Flask app
    app.run(debug=True)