from tiles import *
from player import *

from colours import *

from itertools import cycle
from collections import defaultdict

from numpy import random


class PlayerDebugDisplayer:
	def __init__(self, name):
		self.name = name

	def __call__(self, player):
		print(f"Tour de {self.name} qui a {colours.fg.yellow}{player.money}€{colours.reset}")
		for group in player.wallet:
			print(f"\t{group.__name__} : {", ".join(t.displayer.name for t in player.wallet[group])}")

	def lose(self, amount):
		print(f"\t{self.name} perd {colours.fg.yellow}{amount}€{colours.reset}")

	def win(self, amount):
		print(f"\t{self.name} reçoit {colours.fg.yellow}{amount}€{colours.reset}")

	def pay(self, other_displayer, amount):
		print(f"\t{self.name} −−{colours.fg.yellow}{amount}€{colours.reset}−−> {other_displayer.name}")

	def step(self):
		print(f"{self.name} avance d'une case")

	def too_many_doubles(self):
		print(f"\t{self.name} à fait 3 doubles de suite")

	def go_to_prison(self):
		print(f"{colours.bg.red}{colours.fg.black}{self.name} va en Prison !{colours.reset}")

	def leave_prison(self):
		print(f"{colours.bg.green}{colours.fg.black}{self.name} sort de Prison !{colours.reset}")

	def double_to_get_out_of_prison(self):
		print(f"{self.name} fait un double et sort")

	def pay_rent(self, owner_displayer, purchasable_displayer):
		print(f"{self.name} est sur {purchasable_displayer.name} qui appartient à {owner_displayer.name}")

	def buy(self, purchasable_displayer):
		print(f"{self.name} achète {purchasable_displayer.name}")


class TileDebugDisplayer:
	def __init__(self, name, colour):
		self.name = f"{colour}{name}{colours.reset}"


class ChanceDebugDisplayer:
	def __init__(self):
		self.name = f"{colours.bg.red}Chance{colours.reset}"

	def effect(self, description):
		print(f"\t{self.name} : {colours.bold}{description}{colours.reset}")


class CaisseDebugDisplayer:
	def __init__(self):
		self.name = f"{colours.bg.blue}Caisse{colours.reset}"

	def effect(self, description):
		print(f"\t{self.name} : {colours.bold}{description}{colours.reset}")


class Board:
	def __init__(self, players):
		self.players = cycle(players)
		self.chance_deck = Chance.make_deck()
		self.caisse_deck = Caisse.make_deck()
		self.tiles = [
			# fmt: on
			Tile(TileDebugDisplayer("Départ", colours.italic)),
			Brown(60, 50, (2, 10, 30, 90, 160, 250), TileDebugDisplayer("Boulevard de Belleville", colours.fg.brown)),
			Caisse(self.caisse_deck, CaisseDebugDisplayer()),
			Brown(60, 50, (4, 20, 60, 180, 320, 450), TileDebugDisplayer("Rue Lecourbe", colours.fg.brown)),
			Tax(200, TileDebugDisplayer("Impôt sur le revenu", colours.italic)),
			Station(TileDebugDisplayer("Gare Montparnasse", colours.fg.darkgrey)),
			Grey(100, 50, (6, 30, 90, 270, 400, 550), TileDebugDisplayer("Rue Vaugirard", colours.fg.lightgrey)),
			Chance(self.chance_deck, ChanceDebugDisplayer()),
			Grey(100, 50, (6, 30, 90, 270, 400, 550), TileDebugDisplayer("Rue de Courcelles", colours.fg.lightgrey)),
			Grey(120, 50, (8, 40, 100, 300, 450, 600), TileDebugDisplayer("Avenue de la République", colours.fg.lightgrey)),
			Tile(TileDebugDisplayer("Simple Visite", colours.italic)),
			Pink(140, 100, (10, 50, 150, 450, 625, 750), TileDebugDisplayer("Boulevard de la Villette", colours.fg.pink)),
			Company(TileDebugDisplayer("Service de distribution d'éléctricité", colours.italic)),
			Pink(140, 100, (10, 50, 150, 450, 625, 750), TileDebugDisplayer("Avenue de Neuilly", colours.fg.pink)),
			Pink(160, 100, (12, 60, 180, 500, 700, 900), TileDebugDisplayer("Rue de Paradis", colours.fg.pink)),
			Station(TileDebugDisplayer("Gare de Lyon", colours.fg.darkgrey)),
			Orange(180, 100, (14, 70, 200, 550, 750, 950), TileDebugDisplayer("Avenue Mozart", colours.fg.brown)),
			Caisse(self.caisse_deck, CaisseDebugDisplayer()),
			Orange(180, 100, (14, 70, 200, 550, 750, 950), TileDebugDisplayer("Boulevard Saint-Michel", colours.fg.brown)),
			Orange(200, 100, (16, 80, 220, 600, 800, 1000), TileDebugDisplayer("Place Pigalle", colours.fg.brown)),
			Tile(TileDebugDisplayer("Parc gratuit", colours.italic)),
			Red(220, 150, (18, 90, 250, 700, 875, 1050), TileDebugDisplayer("Avenue Matignon", colours.fg.red)),
			Chance(self.chance_deck, ChanceDebugDisplayer()),
			Red(220, 150, (18, 90, 250, 700, 875, 1050), TileDebugDisplayer("Boulevard Malesherbes", colours.fg.red)),
			Red(240, 150, (20, 100, 300, 750, 925, 1100), TileDebugDisplayer("Avenue Henri-Martin", colours.fg.red)),
			Station(TileDebugDisplayer("Gare du Nord", colours.fg.darkgrey)),
			Yellow(260, 150, (22, 110, 330, 800, 975, 1150), TileDebugDisplayer("Faubourg Saint-Honoré", colours.fg.yellow)),
			Yellow(260, 150, (22, 110, 330, 800, 975, 1150), TileDebugDisplayer("Place de la bourse", colours.fg.yellow)),
			Company(TileDebugDisplayer("Service de distribution des eaux", colours.italic)),
			Yellow(280, 150, (24, 120, 360, 850, 1025, 1200), TileDebugDisplayer("Rue la Fayette", colours.fg.yellow)),
			Prison(TileDebugDisplayer("Prison", colours.italic)),
			Green(300, 200, (26, 130, 390, 900, 1100, 1275), TileDebugDisplayer("Avenue de Breteuil", colours.fg.green)),
			Green(300, 200, (26, 130, 390, 900, 1100, 1275), TileDebugDisplayer("Avenue Foch", colours.fg.green)),
			Caisse(self.caisse_deck, CaisseDebugDisplayer()),
			Green(320, 200, (28, 150, 450, 1000, 1200, 1400), TileDebugDisplayer("Boulevard des Capucines", colours.fg.green)),
			Station(TileDebugDisplayer("Gare Saint-Lazare", colours.fg.darkgrey)),
			Chance(self.chance_deck, ChanceDebugDisplayer()),
			Blue(350, 200, (35, 175, 500, 1100, 1300, 1500), TileDebugDisplayer("Avenue des Champs-Élysées", colours.fg.blue)),
			Tax(100, TileDebugDisplayer("Taxe de Luxe", colours.italic)),
			Blue(400, 200, (50, 200, 600, 1400, 1700, 2000), TileDebugDisplayer("Rue de la paix", colours.fg.blue)),
			# fmt: on
		]

		# TODO : Dirty monkey patching
		groups = defaultdict(set)
		for t in self.tiles:
			groups[type(t)].add(t)

		for t in self.tiles:
			t.group = groups[type(t)]

	def turn_of(self, player):
		dice1, dice2 = random.randint(1, 7, 2)

		if player.position == Tile.PRISON:
			stay = player.in_prison_and_stay(dice1, dice2, board)
			if stay:
				return
		elif player.too_many_doubles(dice1, dice2):
			player.go_to_prison()
			return

		player.displayer(player)
		player.move_from_dice(dice1, dice2)

		while True:  # Loop until player settles down on a tile
			tile = board.tiles[player.position]
			double = False

			if isinstance(tile, Prison):
				player.go_to_prison()
				return

			elif isinstance(tile, Tax):
				tile.tax_from(player)

			elif isinstance(tile, Chance) or isinstance(tile, Caisse):
				prison, moved, double = tile.action(player, players)
				if prison:
					return  # already sent to prison
				if moved:
					continue
			break

		if isinstance(tile, Purchasable):
			player.pay_rent_or_try_to_buy(tile, double, dice1, dice2)

		# print("Add constructions")


players = [Player(PlayerDebugDisplayer("Toto")), Player(PlayerDebugDisplayer("Tata"))]
board = Board(players)

for _ in range(100):
	player = next(board.players)
	board.turn_of(player)
