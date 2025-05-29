import firebase_admin, os
from firebase_admin import credentials, db
from dotenv import load_dotenv

load_dotenv()
print(os.getenv("REALTIME_FIREBASE_URL"))

cred = credentials.Certificate("/Users/huylegia/Coding-Projects/Python/nba-project/server/database/serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": os.getenv("REALTIME_FIREBASE_URL")
})

# mock save data
# ref = db.reference("29may2025/")
# title_ref = ref.child("title")
# players_ref = ref.child("players")

def get_top_10(date: str) -> list:
    """
    Fetch the designated top 10 of a specific date
    :param date: The date to fetch the top 10 topic for
    :return: A list of dictionaries containing the 10 players of the list
    """
    ref = db.reference(f"{date}/")
    players_ref = ref.child("players")
    players = players_ref.get()
    return players