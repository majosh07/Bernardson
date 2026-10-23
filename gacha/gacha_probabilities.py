import random

BASE = {'S': 0.02, 'A': 0.12, 'B': 0.35, 'C': 0.45}
S_HARD = 25
S_SOFT_START = 20
S_CAP = 0.2
A_HARD = 8
A_SOFT_START = 5
A_CAP = 0.25

# return a tuple
# 0: tier that was chosen
# 1: whether or not hard_pity was used for this decision
# 2: s_pity
# 3: a_pity
def roll_tier(s_pity, a_pity) -> tuple[str, bool, int, int]:
    if s_pity >= S_HARD:
        tier, hard = "S", True
    elif a_pity >= A_HARD:
        tier, hard = "A", True
    else:

        probs = get_probabilities(s_pity, a_pity)
        weights = list(probs.values())
        tier = random.choices(list(probs), weights=weights, k=1)[0]
        hard = False

    if tier == "S":
        s_pity, a_pity = 0, a_pity + 1
    elif tier == "A":
        s_pity, a_pity = s_pity + 1, 0
    else:
        s_pity, a_pity = s_pity + 1, a_pity + 1

    return tier, hard, s_pity, a_pity

def _soft_chance(base: float, cap: float, pity: int, start: int, hard: int) -> float:
    if pity < start:
        return base
    slope = (cap - base) / (hard - start)
    return min(cap, base + slope * (pity - start))

def get_probabilities(s_pity, a_pity):
    s = _soft_chance(BASE["S"], S_CAP, s_pity, S_SOFT_START, S_HARD)
    a = _soft_chance(BASE["A"], A_CAP, a_pity, A_SOFT_START, A_HARD)
    rest = 1 - a - s
    bc = BASE["B"] * BASE["C"]
    return {
        "S": s,
        "A": a,
        "B": rest * BASE["B"] / bc,
        "C": rest * BASE["C"] / bc,
    }

