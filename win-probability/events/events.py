from events.scores import process_scores
from events.time import process_time_step


def process_events(game_state, events):
    """Process box score updates and seconds / minutes played updates"""
    for event in events:
        game_state = process_time_step(game_state, event)
        game_state = process_scores(game_state, event)
    return game_state
