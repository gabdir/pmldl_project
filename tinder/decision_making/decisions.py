from enum import IntEnum


class Decision(IntEnum):
    """
    There are three possible decisions by our bot, include the one, that closes all popups
    """

    LIKE = 1
    DISLIKE = 2
    CLOSE_POPUP = 3


def make_decision(picture_url, model):
    """
    Makes decision on like or dislike for given picture
    """
    prediction = model.predict(picture_url)
    if prediction == 1:
        return Decision.LIKE
    else:
        return Decision.DISLIKE
