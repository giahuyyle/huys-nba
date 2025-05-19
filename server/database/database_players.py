import os, csv, string
from dotenv import load_dotenv

from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session


# Open .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
if os.path.exists(dotenv_path): 
    load_dotenv(dotenv_path)
    print(f"Environment variables loaded from {dotenv_path}")
else:
    print(f"Warning: .env file not found at {dotenv_path}. Environment variables may not be loaded.")

# Load environment variables
db_type = os.getenv("DB_TYPE")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
database = os.getenv("DB_NAME_PLAYERS")               # Database name for players
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
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
session = SessionLocal()


'''
TABLE STRUCTURE FOR NBA PLAYERS
'''
class Players(Base):
    __tablename__ = "players"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    Player = Column(String)
    From = Column(Integer)
    To = Column(Integer)
    Pos = Column(String)
    Height = Column(String)
    Weight = Column(String)
    Birthdate = Column(String)
    College = Column(String)
    player_additional = Column(String)


'''
PROCESSING DATA FUNCTION
'''
def process_players_data(csv_filepath):
    """
    Reads the CSV file and returns a list of dictionaries containing player data.
    """
    data = []
    
    with open(csv_filepath, 'r') as file:
        csv_file = csv.reader(file)
        
        for row in csv_file:
            # Skip the header row
            if csv_file.line_num == 1:
                continue
            
            player_data = Players(
                Player=row[0],
                From=int(row[1]),
                To=int(row[2]),
                Pos=row[3],
                Height=row[4],
                Weight=row[5],
                Birthdate=row[6],
                College=row[7],
                player_additional=row[8]
            )

            data.append(player_data)

    return data


'''
INSERTING DATA FUNCTION
'''
def insert_players_data(data_to_insert):
    try:
        if session is None:
            raise ValueError("Session is not initialized.")
        
        session.bulk_save_objects(data_to_insert)
        session.commit()
        print(f"Inserted {len(data_to_insert)} records into the database.")

    except ValueError as ve:
        print(f"ValueError: {ve}")
        
    except Exception as e:
        print(f"Error inserting data: {e}")

    finally:
        # Close the session
        session.close()
        print("Session closed after data insertion.")


def insert_players_by_file():
    lowercase_letters = list(string.ascii_lowercase)

    for letter in lowercase_letters:
        # Path to the CSV file
        filepath = f"/Users/huylegia/Coding-Projects/Python/nba-project/server/raw-data/all-time-players-data/{letter}_lastname.csv"
        data_to_insert = process_players_data(filepath)
        insert_players_data(data_to_insert)
        print(f"Inserted data for players with last name starting with '{letter}'")


# Main - create the database tables
def main():
    # Create the database tables
    try:
        # Base.metadata.create_all(bind=engine)
        print("Database tables created successfully.")
    except Exception as e:
        print(f"Error creating database tables: {e}")
    finally:
        session.close()
        print("Session closed.")


if __name__ == "__main__":
    main()
    # Close the session