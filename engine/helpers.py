import pygame
import enum
import time

class Events(enum.Enum):
    CHANGE_ACTIVITY = 0
    ADD_SESSION_DATA = 1

def change_activity(activity_name):
    event = pygame.event.Event(pygame.USEREVENT, val=Events.CHANGE_ACTIVITY, name=activity_name)
    pygame.event.post(event)

def add_session_data(key, val):
    event = pygame.event.Event(pygame.USEREVENT, val=Events.ADD_SESSION_DATA, key=key, vl=val)
    pygame.event.post(event)

def smooth_code(func, after = None, duration=1, interval=0.05):
    """
    thread blockin with sleep calls

    :param func: function (i) where i is current loop no
    :param after: function to call after execution
    :param duration: duration of smooth (in seconds)
    :param interval: interval between func calls (in seconds)
    :return:
    """
    times =  duration // interval
    for i in range(int(times)):
        func(i)
        time.sleep(interval)
    if after is not None:
        after()