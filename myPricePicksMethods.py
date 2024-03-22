import pandas as pd
import numpy as np
from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import Location 
from basketball_reference_web_scraper.data import Team
from basketball_reference_web_scraper.data import Outcome 
from basketball_reference_web_scraper.data import OutputType 
from basketball_reference_web_scraper.data import OutputWriteOption 
from basketball_reference_web_scraper.data import Position

#allows me to look up the players slug with his name
def find_slug_by_name(name_dict,player_name):
    for slug, name in name_dict.items():
        if name == player_name:
            return slug
    return None

#allows me to gather players info
def get_players_info(player_name,year):
    return pd.DataFrame(client.regular_season_player_box_scores(
        player_identifier=player_name, 
        season_end_year=year
    ))

#used the get the average of a player for a certain category
def get_players_average_stat(all_data, player_name, stat):
    if stat not in all_data.columns:
        print(f"Stat '{stat}' not found in the data.")
        return None
    
    player_data = all_data[all_data['name'] == player_name]

    if player_data.empty:
        print(f"No data found for player: {player_name}")
        return None
    
    return player_data[stat].mean()

#used to calculate the amount of times the player has hit the under on the projected value
def count_projected(player_name, year, stat, projected_value,bet='over'):
    player_data = get_players_info(player_name,year)

    proj_value = np.ceil(projected_value) if bet == 'over' else np.floor(projected_value)
    
    if stat not in player_data.columns:
        print(f"Stat '{stat}' not found in the data. ")
        return None

    if player_data.empty:
        print(f"No data found for player: {player_name}")
        return None
    if bet == 'over':    
        count = (player_data[stat] <= proj_value).sum()
    else:
        count = (player_data[stat] >= proj_value).sum()

    games_played = player_data.shape[0]
    percentage = (count/games_played).round(2)

    print(f"{name_dict[player_name]} has gone {bet} on {projected_value} in {columns_rename[stat]} a total of {count} times in {games_played} games played which is {percentage}%.")
    return count

#used to calculate the amount of times they've hit the under in most recent games
def count_projected_within_x_games(player_name, year, stat, projected_value, num_games=None,bet='over'):
    player_data = get_players_info(player_name,year)

    if num_games is not None and num_games < len(player_data):
        player_data = player_data.tail(num_games)

    proj_value = np.ceil(projected_value) if bet =='over' else np.floor(projected_value)
    
    if stat not in player_data.columns:
        print(f"Stat '{stat}' not found in the data. ")
        return None

    if player_data.empty:
        print(f"No data found for player: {player_name}")
        return None
    
    if bet == 'under':
        count = (player_data[stat] >= proj_value).sum() 
    elif bet == 'over':
        count = (player_data[stat] >= proj_value).sum()

    games_played = player_data.shape[0]
    percentage = (count/num_games).round(2)

    print(f"{name_dict[player_name]} has gone {bet} on {projected_value} in {columns_rename[stat]} a total of {count} times in his last {num_games} games played which his {percentage}%.")
    return count


