from .database_players import SessionLocal, Players
from .database_pergame import SessionLocalPerGame, PerGame
from dotenv import load_dotenv
import os, sqlite3

def get_top_10(date: str) -> list[dict]:
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

def get_players_by_name(player_name: str):
    """
    Fetch player data from the database based on the player's name.
    
    :param player_name: The name of the player to search for.
    :return: A list of players matching the name.
    """
    session = SessionLocal()
    try:
        # Use SQLAlchemy to query the database
        players = session.query(Players).filter(Players.Player.ilike(f"%{player_name}%")).all()
        
        # Convert the result to a list of dictionaries
        player_list = [{"id": player.id, "additionals": player.player_additional, "name": player.Player} for player in players]
        
        return player_list
    except Exception as e:
        session.rollback()
        print(f"Error fetching: {e}")
        return []
    finally:
        session.close()

#print(get_players_by_name("mAn"))