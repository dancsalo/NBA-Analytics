from events.formats import add_new_team_player
from events.helpers import set_in_dict, division, match_teams, match_players
from events.metrics import SHARED_METRICS, PLAYER_METRICS


def apply_edit_object(map_list, aggregate_stats, edit_object):
    """Recursively add metrics within nested dictionary to game_state nested_dictionary"""
    for key in edit_object:
        if isinstance(edit_object[key], dict):
            aggregate_stats = apply_edit_object(map_list + [key], aggregate_stats, edit_object[key])
        else:
            aggregate_stats = set_in_dict(map_list + [key], aggregate_stats, edit_object[key])
    return aggregate_stats


def update_aggregates(state):
    """Calculate percentages and totals"""
    state['fieldGoals']['percentage'] = division(state['fieldGoals']['made'], state['fieldGoals']['attempted'])
    state['freeThrows']['percentage'] = division(state['freeThrows']['made'], state['freeThrows']['attempted'])
    state['threePointFieldGoals']['percentage'] = division(state['threePointFieldGoals']['made'],
                                                           state['threePointFieldGoals']['attempted'])
    state['rebounds']['total'] = state['rebounds']['offensive'] + state['rebounds']['defensive']


def apply_metrics(event, order, state, metrics):
    for edit_object in filter(lambda d: d != {}, [metric(event, order) for metric in metrics.values()]):
        apply_edit_object([], state, edit_object)
        update_aggregates(state)


def process_scores(game_state, event):
    """Update box scores (i.e. player / team state) with an incoming event"""
    for order, player in enumerate(event['pbp']['players']):
        # Add new team / player
        add_new_team_player(game_state['boxscores'], event)

        # Team
        team_state = match_teams(game_state['boxscores'], player['teamId'])[0]
        apply_metrics(event, order, team_state['teamStats'], SHARED_METRICS)

        # Player
        player_state = match_players(game_state['boxscores'], player['teamId'], player['playerId'])[0]
        apply_metrics(event, order, player_state, SHARED_METRICS)
        apply_metrics(event, order, player_state, PLAYER_METRICS)

    return game_state
