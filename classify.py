import random


def inrush_classifier(signals):
    """
    Classify whether inrush is present in `signals`
    """

    result = random.choice(["Inrush", "No inrush"])

    return result
