from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import OutputType


print('***** SEASON advanced *****')
year = 2019
path = "seasonadvanced_"
# for year in range (2017,2019):
season_advanced = client.players_season_advanced(season_end_year=year,output_type =OutputType.CSV ,output_file_path=path+str(year)+".csv")
print("OK")