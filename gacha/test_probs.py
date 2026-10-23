from gacha_probabilities import roll_tier
from collections import Counter
a = s = 0
counts, longest_s = Counter(), 0
for _ in range(200_000):
    tier, _, s, a = roll_tier(a, s)
    longest_s = max(s, longest_s)
    counts[tier] += 1
print({t: round(n / 200_000, 4) for t, n in sorted(counts.items())})
print(f"Longest s: {longest_s}")
