import re
import string
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


VIOLENT_KEYWORDS = [
    "kill", "murder", "massacre", "slaughter", "execute", "decapitate",
    "stab", "shoot", "gun down", "bomb", "explode", "detonate", "firebomb",
    "hang", "lynch", "burn alive", "assassinate", "behead", "ambush",
    "torture", "rape", "poison", "strangle", "shoot up", "wipe out",
    "take out", "obliterate", "destroy them", "eradicate", "exterminate"
]

EXTREME_KEYWORDS = [
    "race war", "holy war", "jihad", "crusade", "purge", "ethnic cleansing",
    "genocide", "final solution", "death to", "wipe them out",
    "bloodbath", "uprising", "revolution by force", "armed resistance",
    "martyrdom", "terror attack", "suicide bombing", "bring down",
    "overthrow by force", "civil war", "death squad"
]

HATE_KEYWORDS = [
    "white power", "heil hitler", "14 words", "1488", "blood and soil",
    "kkk", "klan", "neo-nazi", "nazi scum", "skinhead", "ss soldier",
    "great replacement", "zionist conspiracy", "globalist pigs",
    "race traitor", "mud people", "invaders", "degenerates",
    "inferior race", "ape-like", "subhuman", "pure blood",
    "white genocide", "ethno-state"
]

THREAT_PHRASES = [
    "i’ll kill you", "you should die", "hope you die",
    "you deserve to die", "i will hunt you down", "i’ll find you",
    "you’re dead", "shoot you in the head", "blow you up",
    "i swear i’ll kill", "i’ll make you pay", "i’ll destroy you",
    "bring my gun", "school shooting", "shoot up the place",
    "blood will be spilled", "time to die"
]


analyzer = SentimentIntensityAnalyzer()

def calculate_risk_score(post, user_history=None):
    text = post.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))

    risk_score = 0
    matches = []

    def scan_and_score(keywords, weight):
        nonlocal risk_score
        for kw in keywords:
            if re.search(rf"\b{re.escape(kw)}\b", text):
                risk_score += weight
                matches.append(kw)

    scan_and_score(VIOLENT_KEYWORDS, 5)
    scan_and_score(EXTREME_KEYWORDS, 7)
    scan_and_score(HATE_KEYWORDS, 6)
    scan_and_score(THREAT_PHRASES, 10)

    sentiment = analyzer.polarity_scores(text)
    if sentiment["compound"] < -0.5:
        risk_score += 3
        matches.append("negative_sentiment")

    violent_hits = sum(kw in text for kw in VIOLENT_KEYWORDS)
    if violent_hits >= 3:
        risk_score += 5
        matches.append("multiple_violent_terms")

    urgency_triggers = ["today", "right now", "soon", "time to act"]
    if any(ut in text for ut in urgency_triggers):
        risk_score += 4
        matches.append("urgency")

    if user_history and user_history.get("flagged_rate", 0) > 0.2:
        risk_score += 5
        matches.append("repeat_offender")

    # return {
    #     "risk_score": risk_score,
    #     "matches": matches,
    #     "sentiment": sentiment
    # }
    return risk_score