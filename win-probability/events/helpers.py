from collections import defaultdict
from functools import reduce
import operator


def convert_to_seconds_elapsed(event):
    minutes = int(event.get('pbptimeminutes'))
    seconds = int(event.get('pbptimeseconds').replace('.', ''))
    period = int(event.get('pbpperiod'))
    return ((period - 1) * 1200) + ((20 - minutes) * 20) + (60 - seconds)


def get_from_dict(map_list, data_dict):
    return reduce(operator.getitem, map_list, data_dict)


def set_in_dict(map_list, data_dict, value):
    original_value = get_from_dict(map_list[:-1], data_dict)[map_list[-1]]
    if isinstance(original_value, bool):
        get_from_dict(map_list[:-1], data_dict)[map_list[-1]] = value
    else:
        get_from_dict(map_list[:-1], data_dict)[map_list[-1]] = value + original_value
    return data_dict


def nested_defaultdict():
    return defaultdict(nested_defaultdict)


def division(numerator, denominator):
    if denominator > 0:
        return round(numerator / denominator, 3)
    else:
        return 0.0


def match_teams(boxscores, team_id):
    return [team for team in boxscores if team['teamId'] == team_id]


def match_players(boxscores, team_id, player_id):
    teams = match_teams(boxscores, team_id)
    if len(teams) > 0:
        return [player for player in teams[0]['playerStats'] if player['player']['playerId'] == player_id]
    return []
