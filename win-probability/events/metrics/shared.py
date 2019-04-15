from events.helpers import nested_defaultdict


def free_throws(event, order):
    d = nested_defaultdict()
    if event['pbp'].get('shotAttemptPoints', -1) == 1 and order == 0:
        d['freeThrows']['attempted'] = 1
        if event['pbp']['playEvent'].get('name', '') == 'Free Throw Made':
            d['freeThrows']['made'] = 1
            d['points'] = 1
    return d


def field_goals(event, order):
    d = nested_defaultdict()
    if event['pbp'].get('shotAttemptPoints', -1) == 2 and order == 0:
        d['fieldGoals']['attempted'] = 1
        if event['pbp']['playEvent'].get('name', '') == 'Field Goal Made':
            d['fieldGoals']['made'] = 1
            d['points'] = 2
    return d


def three_point_field_goals(event, order):
    d = nested_defaultdict()
    if event['pbp'].get('shotAttemptPoints', -1) == 3 and order == 0:
        d['threePointFieldGoals']['attempted'] = 1
        d['fieldGoals']['attempted'] = 1
        if event['pbp']['playEvent'].get('name', '') == 'Field Goal Made':
            d['fieldGoals']['made'] = 1
            d['threePointFieldGoals']['made'] = 1
            d['points'] = 3
    return d


def rebounds(event, order):
    d = nested_defaultdict()
    if event['pbp']['playEvent'].get('name', '') == 'Offensive Rebound' and order == 0:
        d['rebounds']['offensive'] = 1
    if event['pbp']['playEvent'].get('name', '') == 'Defensive Rebound' and order == 0:
        d['rebounds']['defensive'] = 1
    return d


def assists(event, order):
    d = dict()
    if event['pbp'].get('pointsScored', -1) > 0 and order == 1:
        d['assists'] = 1
    return d


def personal_fouls(event, order):
    d = dict()
    if event['pbp']['playEvent'].get('name', '') == 'Foul' and \
            event['pbp']['playEvent']['playDetail'].get('name', '') == 'Personal' and order == 0:
        d['personalFouls'] = 1
    return d


def turnovers(event, order):
    d = dict()
    if event['pbp']['playEvent'].get('name', '') == 'Turnover' and order == 0:
        d['turnovers'] = 1
    return d


def steals(event, order):
    d = dict()
    if event['pbp']['playEvent'].get('name', '') == 'Turnover' and order == 1:
        d['steals'] = 1
    return d


def blocks(event, order):
    d = dict()
    if event['pbp']['playEvent'].get('name', '') == 'Field Goal Missed' and order == 1:
        d['blockedShots'] = 1
    return d


SHARED_METRICS = {
    'free_throws': free_throws,
    'field_goals': field_goals,
    'three_point_field_goals': three_point_field_goals,
    'steals': steals,
    'rebounds': rebounds,
    'assists': assists,
    'personal_fouls': personal_fouls,
    'turnovers': turnovers,
    'blocks': blocks
}
