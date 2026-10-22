import random

BASE_PROBABILITIES = {'S': 0.02, 'A': 0.12, 'B': 0.35, 'C': 0.45}
S_HARD_PITY = 25
S_SOFT_PITY_START = 20
S_SOFT_PITY_CAP = 0.15
S_SLOPE = (S_SOFT_PITY_CAP - BASE_PROBABILITIES['S']) / (S_HARD_PITY - 1 - S_SOFT_PITY_START - 1)
S_INTERCEPT = S_SOFT_PITY_CAP - (S_SLOPE * S_HARD_PITY - 1)
A_HARD_PITY = 8
A_SOFT_PITY_START = 5
A_SOFT_PITY_CAP = 0.30
A_SLOPE = (A_SOFT_PITY_CAP - BASE_PROBABILITIES['A']) / (A_HARD_PITY - 1 - A_SOFT_PITY_START - 1)
A_INTERCEPT = A_SOFT_PITY_CAP - (A_SLOPE * A_HARD_PITY - 1)



# return a tuple
# 0: tier that was chosen
# 1: whether or not hard_pity was used for this decision
def choose_tier(a_pity, s_pity):
    if s_pity >= S_HARD_PITY:
        return 'S', True
    if a_pity >= A_HARD_PITY:
        return 'A', True

    probabilities = get_probabilities(BASE_PROBABILITIES, s_pity, a_pity)
    tiers = list(probabilities.keys())
    weights = list(probabilities.values())

    return random.choices(tiers, weights=weights, k=1)[0], False

def get_probabilities(probabilities, s_pity, a_pity):
    probs = probabilities
    s_chance = probs['S']
    a_chance = probs['A']
    if s_pity >= S_SOFT_PITY_START:
        s_chance = S_SLOPE * s_chance + S_INTERCEPT
    if a_pity >= A_SOFT_PITY_START:
        a_chance = A_SLOPE * a_chance + S_INTERCEPT
    rest_of_chance = 1 - (s_chance + a_chance)

    probs['S'] = s_chance
    probs['A'] = a_chance
    total_base = probs['B'] + probs['C']
    probs['B'] = rest_of_chance * (probs['B'] / total_base)
    probs['C'] = rest_of_chance * (probs['C'] / total_base)

    return probs
