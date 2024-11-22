import random
import time
import os
from gif_and_inventory import Inventory, GIF, urls
import numpy

import jsonpickle
TIME_DIFFERENCE_TO_EST_SECONDS = 18000

def get_random_askb():
  return random.choice(urls)


if os.path.getsize('gif_of_day.json') != 0:
  with open("gif_of_day.json") as output_file:
    text = output_file.read()
    gif_dict = jsonpickle.decode(text)
    today_askb = list(gif_dict.values())[-1]
else:
  today_askb = get_random_askb()
  current_time = time.gmtime(time.time() - TIME_DIFFERENCE_TO_EST_SECONDS)
  gif_dict = {(current_time.tm_mon, current_time.tm_mday, current_time.tm_year): today_askb}
  with open("gif_of_day.json", 'w') as output_file:
    output_file.write(jsonpickle.encode(gif_dict, indent=1))


if os.path.getsize('members.json') != 0:
  with open("members.json") as output_file:
    text = output_file.read()
    members = jsonpickle.decode(text)  
else:
  members = {}


def find_json_time():
  if os.path.getsize('time_of_day.json') != 0:
    with open('time_of_day.json') as output_file:
      text = output_file.read()
      json_time = jsonpickle.decode(text)
  else:
    json_time = time.gmtime(time.time() - TIME_DIFFERENCE_TO_EST_SECONDS)
    with open('time_of_day.json', 'w') as output_file:
      output_file.write(jsonpickle.encode(json_time, indent=1))
  return json_time


def askb_of_the_day(author):
  global today_askb
  current_time = time.gmtime(time.time() - TIME_DIFFERENCE_TO_EST_SECONDS)
  print(current_time)
  json_time = find_json_time()
  if current_time.tm_mday != json_time.tm_mday:
    asked = False
  else:
    asked = True

  if not asked:
    today_askb = get_random_askb()
    with open('time_of_day.json', 'w') as output_file:
      output_file.write(jsonpickle.encode(current_time, indent=1))
    with open("gif_of_day.json") as output_file:
      text = output_file.read()
      gif_dict = jsonpickle.decode(text)
    with open("gif_of_day.json", "w") as output_file:
      gif_dict[(current_time.tm_mon, current_time.tm_mday, current_time.tm_year)] = today_askb
      output_file.write(jsonpickle.encode(gif_dict, indent=1))
    check_and_add(author)
    return today_askb
  else:
    check_and_add(author)
    return today_askb






def check_and_add(author):
  author_id = str(author.id)
  if author_id in members:
    members[author_id].add_rolls()
    if author.name != members[author_id].name:
      members[author_id].name = author.name
  else:
    members[author_id] = Inventory(author)
  with open("members.json", 'w') as output_file:
    output_file.write(jsonpickle.encode(members, indent=1))


def num_rolls(author):
  return members[str(author.id)].rolls


def roll(author):
  # This will hold:
  # the gif, if hit s pity, if hit a pity
  roll_list = [False, False, False]
  id_key = str(author.id)
  tiers = ['S', 'A', 'B', 'C']
  if members[id_key].S_pity >= 29:
    rand_tier_value = "S"
    plus_pity(id_key, rand_tier_value)
    roll_list[1] = True
  elif members[id_key].A_pity >= 9:
    rand_tier_value = "A"
    plus_pity(id_key, rand_tier_value)
    roll_list[2] = True
  else:
    rand_tier_value = find_roll(tiers, members[id_key].A_pity, members[id_key].S_pity)
    plus_pity(id_key, rand_tier_value)

  roll_list[0] = GIF(tier_value = rand_tier_value)
  members[id_key].add_gif(roll_list[0])
  members[id_key].subtract_rolls()
  with open("members.json", 'w') as output_file:
    output_file.write(jsonpickle.encode(members, indent=0))
  return roll_list

def plus_pity(id_key, rand_tier_value):
  if rand_tier_value == 'S':
    members[id_key].S_pity = 0
    members[id_key].A_pity += 1
  elif rand_tier_value == 'A':
    members[id_key].S_pity += 1
    members[id_key].A_pity = 0
  else:
    members[id_key].S_pity += 1
    members[id_key].A_pity += 1

def find_roll(tiers, A_pity, S_pity):
  S_SOFT_PITY = 25
  A_SOFT_PITY = 8
  # Just tested weights to get these numbers, tried to aim for
  # 10% for S when you were at max
  # 20% for A when you were at max

  return linear_percentage_rolls(tiers, A_pity, S_pity)



# Linear equations end right before guaranteed
# So S_pity end is 29 and A_pity end 9
# Having start be at 2% and end at 10% for S
# Having start be at 10% and end at 20% for A
def linear_percentage_rolls(tiers, A_pity, S_pity, S_SOFT_PITY = 25, A_SOFT_PITY = 8, S_start = .02, S_end = .1,
                            A_start = .1, A_end = .2):
  S_slope = (S_end * 100 - S_start * 100) / (29 - S_SOFT_PITY)
  S_intercept = S_start * 100 - (S_slope * S_SOFT_PITY)
  A_slope = (A_end * 100 - A_start * 100) / (9 - A_SOFT_PITY)
  A_intercept = A_start * 100 - (A_slope * A_SOFT_PITY)


  S_chance = .01
  A_chance = .09
  if S_pity >= S_SOFT_PITY and A_pity >= A_SOFT_PITY:
    S_chance = (S_slope * S_pity + S_intercept) / 100
    A_chance = (A_slope * A_pity + A_intercept) / 100
  elif S_pity >= S_SOFT_PITY:
    S_chance = (S_slope * S_pity + S_intercept) / 100
  elif A_pity >= A_SOFT_PITY:
    A_chance = (A_slope * A_pity + A_intercept) / 100
  B_and_C_chance = (1 - (S_chance + A_chance)) / 2

  return numpy.random.choice(tiers, p=[S_chance, A_chance, B_and_C_chance, B_and_C_chance])

def append_favorite(author, id_num):
  members[str(author.id)].favorites.append(GIF("C", id_num))
  with open("members.json", 'w') as output_file:
    output_file.write(jsonpickle.encode(members, indent=2))