def get_timestamp(play_by_play):
    return {
        'minutes': int(play_by_play['time']['minutes']),
        'seconds': float(play_by_play['time']['seconds']),
        'period': int(play_by_play['period'])
    }


def convert_to_seconds(timestamp):
    return (timestamp['period'] - 1) * 1200 + (1200 - (timestamp['minutes'] * 60 + timestamp['seconds']))


def time_difference(current, last):
    return convert_to_seconds(current) - convert_to_seconds(last)


def update_player_seconds(player_states, seconds_difference):
    for player in player_states:
        if player['isIn']:
            player['secondsPlayed'] += seconds_difference


def update_player_minutes(player_states):
    for player in player_states:
        player['minutesPlayed'] = int(round(player['secondsPlayed'] / 60))


def loop_over_players(game_state):
    for team in game_state['boxscores']:
        for player in team['playerStats']:
            yield player


def process_time_step(game_state, event):
    current_timestamp = get_timestamp(event['pbp'])

    seconds_difference = time_difference(current_timestamp, game_state['timestamp'])
    update_player_seconds(loop_over_players(game_state), seconds_difference)
    update_player_minutes(loop_over_players(game_state))

    game_state['timestamp'] = current_timestamp

    return game_state
