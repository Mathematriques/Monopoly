from tiles import *
from collections import defaultdict


class Player:
	def __init__(self):
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
		print("\tAdd player end + real amount payed")
		return amount

	def win(self, amount):
		self.money += amount

	def step(self, step):
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
			return True
		return False

	def go_to_prison(self):
		self.position = Tile.PRISON
		self.turns_in_prison = 0

	def use_chance_to_get_out_of_prison(self, chance_deck):
		self.chance_out = False
		board.chance_deck.append(Chance.SORTIE_DE_PRISON)

	def use_caisse_to_get_out_of_prison(self, caisse_deck):
		self.caisse_out = False
		board.caisse_deck.append(Caisse.SORTIE_DE_PRISON)

	def pay_tax_to_get_out_of_prison(self):
		self.lose(50)

	def double_to_get_out_of_prison(self):
		pass  # Leaving the prison is handeled in in_prison_and_stay

	def leave_prison(self):
		self.position = Tile.PRISON
		self.turns_in_prison = 0

	def pay_rent(self, purchasable, double, dice1, dice2):
		rent = purchasable.compute_rent(double, dice1, dice2)
		payed = self.lose(rent)
		purchasable.owner.win(payed)

	def buy(self, purchasable):
		self.lose(purchasable.price)
		group = type(purchasable)
		self.wallet[group].add(purchasable)
		purchasable.owner = self
		purchasable.buy_update_rent(self.wallet[group])

	#############################################################

	def pay(self, other, amount):
		other.win(self.lose(amount))

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


class PlayerDebug(Player):
	def __init__(self, name):
		super().__init__()
		self.name = name

	def __str__(self):
		return self.name

	def sumup(self):
		print(f"Tour de {self.name} qui a {colours.fg.yellow}{self.money}€{colours.reset}")
		for group in self.wallet:
			print(f"\t{group.__name__} : {", ".join(str(t) for t in self.wallet[group])}")

	def lose(self, amount):
		print(f"\t{self.name} perd {colours.fg.yellow}{amount}€{colours.reset}")
		return super().lose(amount)

	def win(self, amount):
		print(f"\t{self.name} reçoit {colours.fg.yellow}{amount}€{colours.reset}")
		super().win(amount)

	def step(self, step):
		print(f"{self.name} avance d'une case")
		super().step(step)

	def too_many_doubles(self, dice1, dice2):
		prison = super().too_many_doubles(dice1, dice2)
		if prison:
			print(f"\t{self.name} à fait 3 doubles de suite")
		return prison

	def go_to_prison(self):
		print(f"{colours.bg.red}{colours.fg.black}{self.name} va en Prison !{colours.reset}")
		super().go_to_prison()

	def use_chance_to_get_out_of_prison(self, chance_deck):
		self.chance_out = False
		board.chance_deck.append(Chance.SORTIE_DE_PRISON)

	def use_caisse_to_get_out_of_prison(self, caisse_deck):
		self.caisse_out = False
		board.caisse_deck.append(Caisse.SORTIE_DE_PRISON)

	def pay_tax_to_get_out_of_prison(self):
		self.lose(50)

	def double_to_get_out_of_prison(self):
		print(f"{self.name} fait un double et sort")

	def leave_prison(self):
		print(f"{colours.bg.green}{colours.fg.black}{self.name} sort de Prison !{colours.reset}")
		super().leave_prison()

	def pay_rent(self, purchasable, double, dice1, dice2):
		print(f"{self.name} est sur {str(purchasable.name)} qui appartient à {str(purchasable.owner)}")
		super().pay_rent(purchasable, double, dice1, dice2)

	def buy(self, purchasable):
		print(f"{self.name} achète {str(purchasable.name)}")
		super().buy(purchasable)
