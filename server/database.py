import os
from dotenv import load_dotenv


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
database = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASS")
db_schema =  os.getenv("DB_SCHEMA")


def construct_db_url(db_type, db_host, db_port, database, db_user, db_password):
    if db_type == "mysql":
        return f"mysql://{db_user}:{db_password}@{db_host}:{db_port}/{database}"
    elif db_type == "mssql":
        return f"mssql+pyodbc://{db_user}:{db_password}@{db_host}:{db_port}/{database}"
    elif db_type == "pgsql":
        return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{database}"
    else:
        raise ValueError("Unsupported database type")
    

