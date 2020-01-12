from basketball_reference_web_scraper import client
from datetime import datetime
import functools
import sys


def get_team_score(team, num_games, sched, last_index, box_score_dict):
    num_games = int(num_games)
    recent_games = []
    recent_opp_games = []

    while len(recent_games) < num_games:
        game = sched[last_index]
        opponent = None
        if game['home_team'] == team:
            opponent = game['away_team']
        elif game['away_team'] == team:
            opponent = game['home_team']

        if opponent is not None:
            day = game['start_time'].day
            month = game['start_time'].month
            year = game['start_time'].year
            key = game['start_time'].date()

            if key in box_score_dict:
                box_scores = box_score_dict[key]
            else:
                box_scores = client.team_box_scores(day=day, month=month, year=year)
                box_score_dict[key] = box_scores

            for i in range(0, len(box_scores)):
                if box_scores[i]['team'] == team:
                    recent_games.append(box_scores[i])
                elif box_scores[i]['team'] == opponent:
                    recent_opp_games.append(box_scores[i])

        last_index -= 1
        if last_index < 0:
            break

    ft_att = 0
    ft_made = 0
    fg_att = 0
    fg_made = 0
    off_reb = 0
    def_reb = 0
    to = 0
    num_poss = 0

    opp_ft_att = 0
    opp_ft_made = 0
    opp_fg_att = 0
    opp_fg_made = 0
    opp_def_reb = 0
    opp_off_reb = 0
    opp_to = 0
    opp_num_poss = 0

    for i in recent_games:
        ft_att += i['attempted_free_throws']
        ft_made += i['made_free_throws']
        fg_att += i['attempted_field_goals']
        fg_made += i['made_field_goals'] + .5 * i['made_three_point_field_goals']
        off_reb += i['offensive_rebounds']
        def_reb += i['defensive_rebounds']
        to += i['turnovers']
        num_poss += i['attempted_field_goals'] + i['turnovers'] + i['attempted_free_throws'] / 1.8

    for i in recent_opp_games:
        opp_ft_att += i['attempted_free_throws']
        opp_ft_made += i['made_free_throws']
        opp_fg_att += i['attempted_field_goals']
        opp_fg_made += i['made_field_goals'] + .5 * i['made_three_point_field_goals']
        opp_off_reb += i['offensive_rebounds']
        opp_def_reb += i['defensive_rebounds']
        opp_to += i['turnovers']
        opp_num_poss += i['attempted_field_goals'] + i['turnovers'] + i['attempted_free_throws'] / 1.8

    efg = fg_made / fg_att
    ft = ft_made / fg_att
    orp = off_reb / (off_reb + opp_def_reb)
    drp = def_reb / (opp_off_reb + def_reb)
    turnover = to / num_poss

    if opp_fg_att != 0:
        opp_efg = opp_fg_made / opp_fg_att
        opp_ft = opp_ft_made / opp_fg_att
    else:
        opp_efg = 0
        opp_ft = 0

    # opp_orp = opp_off_reb / (opp_off_reb + def_reb)
    # opp_drp = opp_def_reb / (off_reb + opp_def_reb)
    if opp_num_poss != 0:
        opp_turnover = opp_to / opp_num_poss
    else:
        opp_turnover = 0

    off_score = .43 * efg - .39 * turnover + .1 * orp + .08 * ft
    def_score = -.43 * opp_efg + .39 * opp_turnover + .1 * drp - .08 * opp_ft

    return off_score + def_score


def compare(a, b):
    if a[1] > b[1]:
        return -1
    else:
        return 1


def run_four_factors(num_games):
    today = datetime.today()
    sched = client.season_schedule(season_end_year=2020)
    box_score_dict = {}
    final_scores = []

    for i in range(len(sched) - 1, 0, -1):
        game = sched[i]
        if today.date() == game['start_time'].date():
            home_score = get_team_score(game['home_team'], num_games, sched, i, box_score_dict)
            final_scores.append((game['home_team'], home_score))
            # print(game['home_team'], home_score, '\n')

            away_score = get_team_score(game['away_team'], num_games, sched, i, box_score_dict)
            final_scores.append((game['away_team'], away_score))

    sorted_scores = sorted(final_scores, key=functools.cmp_to_key(compare))
    return sorted_scores


def test_player_season_totals(player_name, season_end_year):
    return client.single_player_season_totals(player_name=player_name, season_end_year=season_end_year)


def test_player_box_scores_jersey(player_name, day, month, year):
    return client.single_player_box_scores(player_name=player_name, day=day, month=month, year=year)


def test_player_jersey_number(player_name):
    return client.get_jersey_number(player_name)


def main():
    run_four_factors()

    # print(test_did_player_start(player_name='Zach LaVine', day=29, month=11, year=2019))

    # print(test_player_box_scores_jersey(day=29, month=11, year=2019, player_name='Zach LaVine'))

    # print(test_player_season_totals('Zach LaVine', 2020)['jersey_number'])

    # print(test_player_jersey_number('Dario Šarić'))


def test_did_player_start(player_name, day, month, year):
    box_scores = client.player_box_scores(day, month, year)

    for player in box_scores:
        print(player['name'])#, player['did_start'])


if __name__ == '__main__':
    main()
