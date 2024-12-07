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

	def prison_will(self):
		return False, False, False

	def buy_will(self, purchasable):
		return True

	def construction_will(self, groups):
		pass

	#############################################################

	def lose(self, amount):
		self.money -= amount
		self.displayer.lose(amount)
		print("\tAdd player end + real amount payed")
		return amount

	def win(self, amount):
		self.money += amount
		self.displayer.win(amount)

	def pay(self, other, amount):
		other.win(self.lose(amount))

	def step(self, step):
		self.displayer.step()
		self.position += step
		# Technically DÉPART can be elsewhere than zero
		if self.position in (-1, Tile.TOTAL):
			self.position = 0
		if self.position == Tile.DEPART:
			self.win(200)

	def too_many_doubles(self, dice1, dice2):
		double = dice1 == dice2
		self.doubles_in_a_row = self.doubles_in_a_row + 1 if double else 0
		if self.doubles_in_a_row == 3:
			self.doubles_in_a_row = 0
			self.displayer.too_many_doubles()
			return True
		return False

	def go_to_prison(self):
		self.displayer.go_to_prison()
		self.position = Tile.PRISON
		self.turns_in_prison = 0

	def use_chance_to_get_out_of_prison(self, chance_deck):
		self.displayer.use_chance_to_get_out_of_prison()
		self.chance_out = False
		board.chance_deck.append(Chance.SORTIE_DE_PRISON)

	def use_caisse_to_get_out_of_prison(self, caisse_deck):
		self.displayer.use_caisse_to_get_out_of_prison()
		self.caisse_out = False
		board.caisse_deck.append(Caisse.SORTIE_DE_PRISON)

	def pay_tax_to_get_out_of_prison(self):
		self.displayer.pay_tax_to_get_out_of_prison()
		self.lose(50)

	def double_to_get_out_of_prison(self):
		self.displayer.double_to_get_out_of_prison()

	def leave_prison(self):
		self.displayer.leave_prison()
		self.position = Tile.PRISON
		self.turns_in_prison = 0

	def pay_rent(self, purchasable, double, dice1, dice2):
		self.displayer.pay_rent(purchasable.owner.displayer, purchasable)
		rent = purchasable.compute_rent(double, dice1, dice2)
		payed = self.lose(rent)
		purchasable.owner.win(payed)

	def buy(self, purchasable):
		self.displayer.buy(purchasable)
		self.lose(purchasable.price)
		group = type(purchasable)
		self.wallet[group].add(purchasable)
		purchasable.owner = self
		purchasable.buy_update_rent(self.wallet[group])

	#############################################################

	def move_to(self, position, step=1):
		assert abs(step) == 1
		while self.position != position:
			self.step(step)

	def move_from_dice(self, dice1, dice2):
		self.move_to((self.position + dice1 + dice2) % Tile.TOTAL)

	def tax_construction(self, house, hotel):
		print("\tAdd tax_construction later")

	def in_prison_and_stay(self, dice1, dice2, board):
		if self.turns_in_prison == 1:
			chance, caisse, taxe = self.prison_will()
			if chance and self.chance_out:
				self.use_chance_to_get_out_of_prison(board.chance_deck)
			elif caisse and self.caisse_out:
				self.use_caisse_to_get_out_of_prison(board.caisse_deck)
			elif taxe and (self.money >= 50):
				self.pay_tax_to_get_out_of_prison()
			# Look at dices output only if no othe method is wanted
			elif dice1 == dice2:
				self.double_to_get_out_of_prison()
			else:
				self.turns_in_prison += 1
				return True  # stay in prison

		elif self.turns_in_prison < 3:
			if dice1 == dice2:
				self.double_to_get_out_of_prison()
			else:
				self.turns_in_prison += 1
				return True  # stay in prison

		self.leave_prison()
		return False

	def pay_rent_or_try_to_buy(self, purchasable, double, dice1, dice2):
		if purchasable.owner:
			self.pay_rent(purchasable, double, dice1, dice2)
		elif self.buy_will(purchasable) and self.money >= purchasable.price:
			self.buy(purchasable)
