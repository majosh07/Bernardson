from gacha_probabilities import roll_tier
from collections import Counter
a = s = 0
counts, longest_s = Counter(), 0
s_pities = []
a_pities = []
for _ in range(200_000):
    tier, _, s, a = roll_tier(s, a)
    s_pities.append(s)
    a_pities.append(a)
    counts[tier] += 1
print(f"This is s_pities:\n{s_pities}")
# print(f"This is a_pities:\n{a_pities}")
