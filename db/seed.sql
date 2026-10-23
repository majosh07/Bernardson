-- seed.sql
INSERT INTO users (user_id) VALUES (594617002736222219);
-- the trigger creates user_gacha rows with 10 rolls; adjust them here
UPDATE user_gacha SET roll_count = 50, a_pity = 7, s_pity = 24 WHERE user_id = 594617002736222219;
INSERT INTO user_gifs (user_id, gif_id) VALUES (594617002736222219, 1), (594617002736222219, 2), (594617002736222219, 3);
