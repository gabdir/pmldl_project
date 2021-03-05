from enum import IntEnum
import numpy as np
from tinder.decision_making.model import get_model, process_external_image


class Decision(IntEnum):
    """
    There are three possible decisions by our bot, include the one, that closes all popups
    """

    LIKE = 1
    DISLIKE = 2
    CLOSE_POPUP = 3


def make_decision(picture_url):
    """
    Makes decision on like or dislike for given picture
    """
    image = process_external_image(picture_url)
    model = get_model()
    prediction = model.predict(image)
    if prediction[0][1] > 0.4:
        return Decision.LIKE
    else:
        return Decision.DISLIKE
