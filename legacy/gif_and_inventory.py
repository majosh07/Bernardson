import time
import random
from askb_data import askb_list, tier_values, khaled_gifs, khaled_tiers

testing = False

if testing:
  print("\n\n\nYou are in Testing Mode :D\n\n\n\n\n\n\n\n")

urls = askb_list + khaled_gifs
tiers = tier_values + khaled_tiers
zipped_list = zip(urls, tiers)
zipped_list = [(x, y) for x, y in zipped_list]
final_list = [(id + 1001, gif) for id, gif in enumerate(zipped_list)]
TIME_DIFFERENCE_TO_EST_SECONDS = 14400

def tier_random_choice(tier_value):
  tiered_list = [(id, gif) for id, gif in final_list if gif[1] == tier_value]
  choice = random.choice(tiered_list)
  print(choice)
  return choice




class Inventory:
  def __init__(self, author):
    self.name = author.name
    self.rolls = 1
    self.gifs = []
    self.favorites = []
    self.previous_day = time.gmtime(time.time() - TIME_DIFFERENCE_TO_EST_SECONDS).tm_mday
    self.A_pity = 0
    self.S_pity = 0

  def add_rolls(self):
    current_time = time.gmtime(time.time() - TIME_DIFFERENCE_TO_EST_SECONDS)
    if not testing:
      if current_time.tm_mday != self.previous_day:
        self.rolls += 1
        # Gives players an incentive to wait to roll
        # You get an extra roll every 7 days you daily
        if current_time.tm_wday == 6:
          self.rolls += 1
        self.previous_day = time.gmtime(time.time() - 14400).tm_mday
    else:
      self.rolls += 1
      # Gives players an incentive to wait to roll
      # You get an extra roll every 7 days you daily
      if current_time.tm_wday == 6:
        self.rolls += 1
      self.previous_day = time.gmtime(time.time() - 14400).tm_mday

  # Adds the gif to the gif list in Inventory
  # Want to make sure there are no duplicates but there are copies
  def add_gif(self, gif):
    begin = 0
    end = len(self.gifs)
    while begin < end:
      midpoint = (begin + end) // 2
      if gif.id > self.gifs[midpoint].id:
          begin = midpoint + 1
      else:
          end = midpoint
    if begin == len(self.gifs):
      self.gifs.insert(begin, gif)
      return

    if self.gifs[begin].id == gif.id:
      self.gifs[begin].number += 1
    else:
      self.gifs.insert(begin, gif)

  def subtract_rolls(self):
    self.rolls -= 1





class GIF:
  def __init__(self, tier_value = "C", id = 0):
    if id == 0:
      tuple_gif = tier_random_choice(tier_value)
    else:
      for pair in final_list:
        if pair[0] == id:
          tuple_gif = pair
    self.id = tuple_gif[0]
    self.gif = tuple_gif[1][0]
    self.tier = tuple_gif[1][1]
    self.number = 1
    self.obtain_date = time.gmtime(time.time() - TIME_DIFFERENCE_TO_EST_SECONDS)

  def __repr__(self):
    return f"ID: {self.id}\n\turl: {self.gif}\n\ttier: {self.tier}\n\tnumber: {self.number}\n\tDate: {self.obtain_date}"






