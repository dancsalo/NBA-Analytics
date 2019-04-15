from events.helpers import match_teams, match_players


def new_game():
    return {
        'boxscores': [],
        'timestamp': {'minutes': 20, 'seconds': 0, 'period': 1}
    }


def new_team(team_id):
    return {
        'teamId': team_id,
        'playerStats': [],
        'teamStats': {
            'timeoutsRemaining': {},
            'fieldGoals': {
                'made': 0,
                'attempted': 0,
                'percentage': 0.0
            },
            'freeThrows': {
                'made': 0,
                'attempted': 0,
                'percentage': 0.0
            },
            'ejections': {
                'player': 0,
                'coach': 0
            },
            'threePointFieldGoals': {
                'made': 0,
                'attempted': 0,
                'percentage': 0.0
            },
            'points': 0,
            'rebounds': {
                'offensive': 0,
                'defensive': 0,
                'total': 0,
            },
            'assists': 0,
            'steals': 0,
            'blockedShots': 0,
            'turnovers': 0,
            'personalFouls': 0,
            'disqualifications': 0,
            'technicalFouls': {
                'player': 0,
                'coach': 0,
                'bench': 0
            }
        }
    }


def new_subplayer(player_id, first_name, last_name, uniform):
    return {
        'playerId': player_id,
        'firstName': first_name,
        'lastName': last_name,
        'uniform': uniform
    }


def new_player(subplayer):
    return {
        'startingPosition': {},
        'minutesPlayed': 0,
        'player': subplayer,
        'isGamePlayed': True,
        'isGameStarted': False,
        'fieldGoals': {
            'percentage': 0.0,
            'made': 0,
            'attempted': 0
        },
        'freeThrows': {
            'percentage': 0.0,
            'made': 0,
            'attempted': 0
        },
        'threePointFieldGoals': {
            'made': 0,
            'attempted': 0,
            'percentage': 0.0
        },
        'points': 0,
        'rebounds': {
            'offensive': 0,
            'defensive': 0,
            'total': 0
        },
        'assists': 0,
        'steals': 0,
        'blockedShots': 0,
        'turnovers': 0,
        'personalFouls': 0,
        'isDisqualification': False,
        'technicalFouls': 0,
        'isEjected': False,
        'isIn': True,  # not part of official box score
        'secondsPlayed': 0  # not part of official box score
    }


def add_team(boxscores, player):
    if not match_teams(boxscores, player['teamId']):
        boxscores.append(new_team(player['teamId']))


def add_player(boxscores, player):
    players = match_players(boxscores, player['teamId'], player['playerId'])
    if not players:
        subplayer = new_subplayer(player['playerId'],
                                  player.get('firstName', ''),
                                  player.get('lastName', ''),
                                  player.get('uniform', ''))
        team = match_teams(boxscores, player['teamId'])[0]
        team['playerStats'].append(new_player(subplayer))


def add_new_team_player(boxscores, event):
    """ Only if player / team has not been mentioned before """
    for player in event['pbp']['players']:
        add_team(boxscores, player)
        add_player(boxscores, player)
