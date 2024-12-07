from tiles import *

from itertools import cycle
from collections import defaultdict
from numpy import random


class Board:
	def __init__(self, players):
		self.players = players
		self.players_cycle = cycle(players)
		self.chance_deck = Chance.make_deck()
		self.caisse_deck = Caisse.make_deck()

	def set_tiles(self, tiles):
		self.tiles = tiles

		groups = defaultdict(set)
		for t in self.tiles:
			groups[type(t)].add(t)

		for t in self.tiles:
			t.group = groups[type(t)]

	def turn_of(self, player):
		dice1, dice2 = random.randint(1, 7, 2)

		if player.position == Tile.PRISON:
			stay = player.in_prison_and_stay(dice1, dice2, self)
			if stay:
				return
		elif player.too_many_doubles(dice1, dice2):
			player.go_to_prison()
			return

		player.move_from_dice(dice1, dice2)

		while True:  # Loop until player settles down on a tile
			tile = self.tiles[player.position]
			double = False

			if isinstance(tile, Prison):
				player.go_to_prison()
				return

			elif isinstance(tile, Tax):
				tile.tax_from(player)

			elif isinstance(tile, Chance) or isinstance(tile, Caisse):
				prison, moved, double = tile.action(player, self.players)
				if prison:
					return  # already sent to prison
				if moved:
					continue
			break

		if isinstance(tile, Purchasable):
			player.pay_rent_or_try_to_buy(tile, double, dice1, dice2)

		# print("Add constructions")
