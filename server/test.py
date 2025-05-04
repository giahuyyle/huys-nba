import csv, string
from database_pergame import insert_per_game_data, PerGame
from database_players import process_players_data, insert_players_data, Players, session, insert_players_by_file


'''
"""
GET PLAYERS DATA
"""
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


def main():
    # Path to the CSV file
    filepath = "/Users/huylegia/Coding-Projects/Python/nba-project/server/raw-data/nba-stats-24-25.csv"
    
    # Get players data from CSV
    players_data = get_players_data(filepath)
    
    # Insert data into the database
    insert_per_game_data(players_data)

if __name__ == "__main__":
    main()
'''


def main():
    insert_players_by_file()

if __name__ == "__main__":
    main()