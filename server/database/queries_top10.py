import firebase_admin, os
from firebase_admin import credentials, db
from dotenv import load_dotenv
from .database_pergame import SessionLocalPerGame, PerGame

load_dotenv()

cred = credentials.Certificate("/Users/huylegia/Coding-Projects/Python/nba-project/server/database/serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": os.getenv("REALTIME_FIREBASE_URL")
})

# mock save data
# ref = db.reference("29may2025/")
# title_ref = ref.child("title")
# players_ref = ref.child("players")

def get_top_10_rebs(date: str) -> list[dict]:
    """
    Fetch the designated top 10 of a specific date

    :param: date - The date to fetch the top 10 topic for
    :return: A list of dictionaries containing the 10 players of the list
    """
    # trial: data from the 24-25 database, top 10 ppg
    try:
        session = SessionLocalPerGame()
        top10_players = (
            session.query(PerGame).filter(
                (PerGame.team == '2TM') | 
                (~PerGame.player.in_(session.query(PerGame.player).filter(PerGame.team == '2TM'))
            ))
            .order_by(PerGame.trb.desc())
            .limit(10)
            .all()
        )

        top10_players = [
            {
                "id": player.id, 
                "name": player.player,
                "team": player.team,
                "additionals": player.player_additional,
            }
            for player in top10_players
        ]

        return top10_players
    
    except Exception as e:
        session.rollback()
        print(f"Error fetching: {e}")
        return []

    finally:
        session.close()

def insert_top_10(date: str) -> bool:
    ref = db.reference(f"{date}/")
    players_ref = ref.child("players")
    top10_rebs = get_top_10_rebs("1")
    players_ref.set(top10_rebs)

    if (not top10_rebs):
        return False
    return True

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

def get_top_10_title(date: str) -> str:
    """
    Fetch the title of the top 10 topic for a specific date
    :param date: The date to fetch the top 10 topic for
    :return: The title of the top 10 topic
    """
    ref = db.reference(f"{date}/")
    title_ref = ref.child("title")
    title = title_ref.get()
    return title if title else "Top 10 Players"  # Default title if not found

if __name__ == "__main__":
    insert_top_10("30may2025")