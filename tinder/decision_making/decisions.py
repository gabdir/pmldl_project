from enum import IntEnum


class Decision(IntEnum):
    """
    There are possible two decisions by our bot
    """

    LIKE = 1
    DISLIKE = 2
    CLOSE_POPUP = 3
    CLOSE_MATCH = 4


def make_decision(picture):
    """
    Makes decision on like or dislike for given picture
    """
    pass
