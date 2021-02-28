from enum import IntEnum


class Decision(IntEnum):
    """
    There are three possible decisions by our bot, include the one, that closes all popups
    """

    LIKE = 1
    DISLIKE = 2
    CLOSE_POPUP = 3


def make_decision(picture):
    """
    Makes decision on like or dislike for given picture
    """
    pass
