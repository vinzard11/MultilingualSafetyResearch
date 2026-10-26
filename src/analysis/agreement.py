"""Analysis 4: judge reliability.

Cohen's kappa between each judge and the human checks per language, and
between the two human checkers on the overlap samples.
"""

from collections import Counter


def cohen_kappa(a: list[str], b: list[str]) -> float:
    """Cohen's kappa for two raters labelling the same items."""
    if len(a) != len(b) or not a:
        raise ValueError("need two equal-length, non-empty label lists")
    n = len(a)
    observed = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    expected = sum(ca[k] * cb[k] for k in ca) / n**2
    if expected == 1:
        return 1.0
    return (observed - expected) / (1 - expected)


def judge_human_agreement(judge_labels, human_labels):
    # TODO: kappa per judge x language.
    raise NotImplementedError


def human_overlap_agreement(human_labels):
    # TODO: kappa between main and overlap checkers per language.
    raise NotImplementedError
