import os, csv
from dotenv import load_dotenv

from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session


# Open .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
if os.path.exists(dotenv_path): 
    load_dotenv(dotenv_path)
    print(f"Environment variables loaded from {dotenv_path}")
else:
    print(f"Warning: .env file not found at {dotenv_path}. Environment variables may not be loaded.")

# Load environment variables
db_type = os.getenv("DB_TYPE")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
database = os.getenv("DB_NAME_PERGAME")               # Database name for per game stats
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASS")


# Contrsuct the database URL
def construct_db_url(db_type, db_host, db_port, database, db_user, db_password):
    if db_type == "mysql":
        return f"mysql://{db_user}:{db_password}@{db_host}:{db_port}/{database}"
    elif db_type == "mssql":
        return f"mssql+pyodbc://{db_user}:{db_password}@{db_host}:{db_port}/{database}"
    elif db_type == "pgsql":
        return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{database}"
    else:
        raise ValueError("Unsupported database type")
    

# Create engine
db_url = construct_db_url(db_type, db_host, db_port, database, db_user, db_password)
Base = declarative_base()
engine = create_engine(db_url, echo=True)

# Create session
SessionLocalPerGame = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocalPerGame()


"""
TABLE STRUCTURE FOR NBA STATS PER GAME
"""
class PerGame(Base):
    __tablename__ = "per_game_stats_24_25"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    rk = Column(Integer)
    player = Column(String)
    age = Column(Integer)
    team = Column(String)
    pos = Column(String)
    g = Column(Integer)
    gs = Column(Integer)
    mp = Column(Float)
    fg = Column(Float)
    fga = Column(Float)
    fg_pct = Column(Float)
    three_p = Column(Float)
    three_pa = Column(Float)
    three_p_pct = Column(Float)
    two_p = Column(Float)
    two_pa = Column(Float)
    two_p_pct = Column(Float)
    efg_pct = Column(Float)
    ft = Column(Float)
    fta = Column(Float)
    ft_pct = Column(Float)
    orb = Column(Float)
    drb = Column(Float)
    trb = Column(Float)
    ast = Column(Float)
    stl = Column(Float)
    blk = Column(Float)
    tov = Column(Float)
    pf = Column(Float)
    pts = Column(Float)
    awards = Column(String)
    player_additional = Column(String)
    efficiency = Column(Float)


'''
INSERTING DATA
'''

def insert_per_game_data(data_to_insert, batch_size=1000):
    # Insert data into the database in batches, batch size = 1000 if not specified
    try:
        if session is None:
            raise ValueError("Session is None. Cannot insert data.")
        
        # Split data into batches
        batches = [data_to_insert[i:i + batch_size] for i in range(0, len(data_to_insert), batch_size)]

        # Insert each batch
        for batch in batches:
            players = []
            for player in batch:
                player_data = PerGame(
                    rk=player["rk"],
                    player=player["player"],
                    age=player["age"],
                    team=player["team"],
                    pos=player["pos"],
                    g=player["g"],
                    gs=player["gs"],
                    mp=player["mp"],
                    fg=player["fg"],
                    fga=player["fga"],
                    fg_pct=player["fg_pct"],
                    three_p=player["three_p"],
                    three_pa=player["three_pa"],
                    three_p_pct=player["three_p_pct"],
                    two_p=player["two_p"],
                    two_pa=player["two_pa"],
                    two_p_pct=player["two_p_pct"],
                    efg_pct=player["efg_pct"],
                    ft=player["ft"],
                    fta=player["fta"],
                    ft_pct=player["ft_pct"],
                    orb=player["orb"],
                    drb=player["drb"],
                    trb=player["trb"],
                    ast=player["ast"],
                    stl=player["stl"],
                    blk=player["blk"],
                    tov=player["tov"],
                    pf=player["pf"],
                    pts=player["pts"],
                    awards=player["awards"],
                    player_additional=player["player_additional"],
                    efficiency=player["efficiency"]
                )
                players.append(player_data)

            # Bulk insert for efficiency
            session.bulk_save_objects(players)

            # Commit insertion, print a success message
            session.commit()
            print(f"Inserted {len(batch)} records into the database.")
    
    except Exception as e:
        session.rollback()
        print(f"Error inserting data: {e}")
    finally:
        # Close the session
        session.close()
        print("Session closed after data insertion.")


def get_players_data(filepath: str) -> list:
    """
    Reads the CSV file and returns a list of dictionaries containing player data.
    """
    players = []
    
    with open(filepath, 'r') as file:
        csv_file = csv.reader(file)
        
        for row in csv_file:
            # Skip the header row and bottom row
            if csv_file.line_num == 1:
                continue
            
            if row[1] == 'League Average':
                continue

            player_data = {
                "rk": int(row[0]),
                "player": row[1],
                "age": int(row[2]),
                "team": row[3],
                "pos": row[4],
                "g": int(row[5]),
                "gs": int(row[6]),
                "mp": float(row[7]) if row[7] != '' else 0.0,
                "fg": float(row[8]) if row[8] != '' else 0.0,
                "fga": float(row[9]) if row[9] != '' else 0.0,
                "fg_pct": float(row[10]) if row[10] != '' else 0.0,
                "three_p": float(row[11]) if row[11] != '' else 0.0,
                "three_pa": float(row[12]) if row[12] != '' else 0.0,
                "three_p_pct": float(row[13]) if row[13] != '' else 0.0,
                "two_p": float(row[14]) if row[14] != '' else 0.0,
                "two_pa": float(row[15]) if row[15] != '' else 0.0,
                "two_p_pct": float(row[16]) if row[16] != '' else 0.0,
                "efg_pct": float(row[17]) if row[17] != '' else 0.0,
                "ft": float(row[18]) if row[18] != '' else 0.0,
                "fta": float(row[19]) if row[19] != '' else 0.0,
                "ft_pct": float(row[20]) if row[20] != '' else 0.0,
                "orb": float(row[21]) if row[21] != '' else 0.0,
                "drb": float(row[22]) if row[22] != '' else 0.0,
                "trb": float(row[23]) if row[23] != '' else 0.0,
                "ast": float(row[24]) if row[24] != '' else 0.0,
                "stl": float(row[25]) if row[25] != '' else 0.0,
                "blk": float(row[26]) if row[26] != '' else 0.0,
                "tov": float(row[27]) if row[27] != '' else 0.0,
                "pf": float(row[28]) if row[28] != '' else 0.0,
                "pts": float(row[29]) if row[29] != '' else 0.0,
                "awards": row[30],
                "player_additional": row[31]
            }

            player_data["efficiency"] = (
                player_data["pts"] + player_data["trb"] + player_data["ast"] +
                player_data["stl"] - (player_data["fga"] - player_data["fg"]) - (player_data["fta"] - player_data["ft"]) + player_data["blk"] - player_data["tov"]
            ) / player_data["g"] if player_data["g"] > 0 else 0
            
            players.append(player_data)
    
    return players


# Main - create the database tables
def main():
    # Create the database tables
    try:
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully.")
        # Path to the CSV file
        filepath = "/Users/huylegia/Coding-Projects/Python/nba-project/server/raw-data/nba-stats-24-25.csv"
        
        # Get players data from CSV
        players_data = get_players_data(filepath)
        
        # Insert data into the database
        insert_per_game_data(players_data)
    except Exception as e:
        print(f"Error creating database tables: {e}")
    finally:
        session.close()
        print("Session closed.")


if __name__ == "__main__":
    main()
    # Close the session