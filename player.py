from tiles import *

from collections import defaultdict


class Player:
	def __init__(self, displayer):
		self.displayer = displayer
		self.money = 1500
		self.position = Tile.DEPART
		self.doubles_in_a_row = 0
		self.turns_in_prison = 0
		self.chance_out = False
		self.caisse_out = False
		self.wallet = defaultdict(set)

	# Subclassing
	def prison_will(self):
		return False, False, False

	# Subclassing
	def veut_acheter(self, purchasable):
		return True

	# Subclassing
	def vent_construire(self, groups):
		for _ in range(5):
			pass

	def lose(self, amount):
		self.money -= amount
		self.displayer.lose(amount)
		print("\tAdd player end + real amount payed")
		return amount

	def win(self, amount):
		self.money += amount
		self.displayer.win(amount)

	def pay(self, other, amount):
		other.money += amount
		self.money -= amount
		self.displayer.pay(other, amount)
		print("\tAdd player end + real amount payed")

	def too_many_doubles(self, dice1, dice2):
		double = dice1 == dice2
		self.doubles_in_a_row = self.doubles_in_a_row + 1 if double else 0
		if self.doubles_in_a_row == 3:
			self.doubles_in_a_row = 0
			return True
		return False

	def move_to(self, position, step=1):
		assert abs(step) == 1
		while self.position != position:
			self.displayer.step()
			self.position += step
			# Technically DÉPART can be elsewhere than zero
			if self.position in (-1, Tile.TOTAL):
				self.position = 0
			if self.position == Tile.DEPART:
				self.win(200)

	def move_from_dice(self, dice1, dice2):
		self.move_to((self.position + dice1 + dice2) % Tile.TOTAL)

	def go_to_prison(self):
		self.displayer.go_to_prison()
		self.position = Tile.PRISON
		self.turns_in_prison = 0

	def leave_prison(self):
		self.displayer.leave_prison()
		self.position = Tile.PRISON
		self.turns_in_prison = 0

	def tax_construction(self, house, hotel):
		print("\tAdd tax_construction later")

	def in_prison_and_stay(self, dice1, dice2, board):
		if self.turns_in_prison == 1:
			chance, caisse, taxe = self.prison_will()
			if chance and self.chance_out:
				board.chance_deck.append(Chance.SORTIE_DE_PRISON)
			elif caisse and self.caisse_out:
				board.caisse_deck.append(Caisse.SORTIE_DE_PRISON)
			elif taxe and (self.money >= 50):
				self.lose(50)
			elif dice1 != dice2:
				# Look at dices output only if no othe method is wanted
				return True  # stay in prison

		elif self.turns_in_prison < 3:
			if dice1 != dice2:
				return True  # stay in prison

		self.leave_prison()
		return False

	def buy(self, tile):
		self.lose(tile.price)
		group = type(tile)
		self.wallet[group].add(tile)
		tile.owner = self
		tile.buy_update_rent(self.wallet[group])
