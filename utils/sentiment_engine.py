import pandas as pd
import re
from utils.keyword_lists import positive_keywords, negative_keywords

positive_pattern = r"\b(" + "|".join(positive_keywords) + r")\b"
negative_pattern = r"\b(" + "|".join(negative_keywords) + r")\b"

NEGATION_WORDS = {"not", "no", "never", "neither", "nor", "barely", "hardly", "scarcely"}


def _has_negation_before(text, match_start, window=3):
    """Check if a negation word appears within `window` words before the match."""
    words_before = text[:match_start].split()[-window:]
    return bool(NEGATION_WORDS & set(words_before))


def _score_review(text: str) -> tuple[int, int]:
    """Return (pos_count, neg_count) with basic negation awareness."""
    lowered = text.lower()
    pos = 0
    neg = 0

    for m in re.finditer(positive_pattern, lowered):
        if _has_negation_before(lowered, m.start()):
            neg += 1          # "not good" → counts as negative signal
        else:
            pos += 1

    for m in re.finditer(negative_pattern, lowered):
        if _has_negation_before(lowered, m.start()):
            pos += 1          # "not bad" → slight positive signal
        else:
            neg += 1

    return pos, neg


def analyze_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    # Work on a copy so the original Review text is preserved
    result = df.copy()
    result["Review"] = result["Review"].astype(str)

    lowered = result["Review"].str.lower()

    counts = lowered.apply(lambda t: pd.Series(_score_review(t), index=["pos_count", "neg_count"]))
    result["pos_count"] = counts["pos_count"]
    result["neg_count"] = counts["neg_count"]

    result["Score"] = (result["pos_count"] * 2) - (result["neg_count"] * 2)

    # Lowered threshold: ±2 so single-keyword reviews are classified
    result["Sentiment"] = "Neutral"
    result.loc[result["Score"] >= 2, "Sentiment"] = "Positive"
    result.loc[result["Score"] <= -2, "Sentiment"] = "Negative"

    result["Status"] = "Neutral"
    result.loc[result["Sentiment"] == "Positive", "Status"] = "Good"
    result.loc[result["Sentiment"] == "Negative", "Status"] = "Bad"

    return result[["Review", "Score", "Status", "Sentiment"]]
