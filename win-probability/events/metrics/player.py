def starting(event, order):
    d = dict()
    if event['pbp'].get('playText', '') == 'Starting Lineup' and order == 0:
        d['isGameStarted'] = True
    return d


def substitution(event, order):
    d = dict()
    if event['pbp']['playEvent'].get('name', '') == 'Substitution' and order == 0:
        d['isIn'] = True
    if event['pbp']['playEvent'].get('name', '') == 'Substitution' and order == 1:
        d['isIn'] = False
    return d


PLAYER_METRICS = {
    'starting': starting,
    'substitution': substitution
}
