from database.database_players import SessionLocal, Players
from dotenv import load_dotenv
import os

def get_players_by_name(player_name):
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