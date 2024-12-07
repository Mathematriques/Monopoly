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
			print(f"\t{group.__name__} : {", ".join(str(t) for t in player.wallet[group])}")

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

	def pay_rent(self, owner_displayer, purchasable):
		print(f"{self.name} est sur {str(purchasable)} qui appartient à {owner_displayer.name}")

	def buy(self, purchasable):
		print(f"{self.name} achète {str(purchasable)}")


class Board:
	def __init__(self, players):
		self.players = cycle(players)
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
board.set_tiles(
	[
		TileDebug(),  # f"{colours.italic}Départ{colours.reset}"),
		BrownDebug(f"{colours.fg.brown}Boulevard de Belleville{colours.reset}", 60, 50, (2, 10, 30, 90, 160, 250)),
		CaisseDebug(board.caisse_deck),
		BrownDebug(f"{colours.fg.brown}Rue Lecourbe{colours.reset}", 60, 50, (4, 20, 60, 180, 320, 450)),
		TaxDebug(f"{colours.italic}Impôt sur le revenu{colours.reset}", 200),
		StationDebug(f"{colours.fg.darkgrey}Gare Montparnasse{colours.reset}"),
		GreyDebug(f"{colours.fg.lightgrey}Rue Vaugirard{colours.reset}", 100, 50, (6, 30, 90, 270, 400, 550)),
		ChanceDebug(board.chance_deck),
		GreyDebug(f"{colours.fg.lightgrey}Rue de Courcelles{colours.reset}", 100, 50, (6, 30, 90, 270, 400, 550)),
		GreyDebug(f"{colours.fg.lightgrey}Avenue de la République{colours.reset}", 120, 50, (8, 40, 100, 300, 450, 600)),
		TileDebug(),  # f"{colours.italic}Simple Visite{colours.reset}"),
		PinkDebug(f"{colours.fg.pink}Boulevard de la Villette{colours.reset}", 140, 100, (10, 50, 150, 450, 625, 750)),
		CompanyDebug(f"{colours.italic}Service de distribution d'éléctricité{colours.reset}"),
		PinkDebug(f"{colours.fg.pink}Avenue de Neuilly{colours.reset}", 140, 100, (10, 50, 150, 450, 625, 750)),
		PinkDebug(f"{colours.fg.pink}Rue de Paradis{colours.reset}", 160, 100, (12, 60, 180, 500, 700, 900)),
		StationDebug(f"{colours.fg.darkgrey}Gare de Lyon{colours.reset}"),
		OrangeDebug(f"{colours.fg.brown}Avenue Mozart{colours.reset}", 180, 100, (14, 70, 200, 550, 750, 950)),
		CaisseDebug(board.caisse_deck),
		OrangeDebug(f"{colours.fg.brown}Boulevard Saint-Michel{colours.reset}", 180, 100, (14, 70, 200, 550, 750, 950)),
		OrangeDebug(f"{colours.fg.brown}Place Pigalle{colours.reset}", 200, 100, (16, 80, 220, 600, 800, 1000)),
		TileDebug(),  # f"{colours.italic}Parc gratuit{colours.reset}"),
		RedDebug(f"{colours.fg.red}Avenue Matignon{colours.reset}", 220, 150, (18, 90, 250, 700, 875, 1050)),
		ChanceDebug(board.chance_deck),
		RedDebug(f"{colours.fg.red}Boulevard Malesherbes{colours.reset}", 220, 150, (18, 90, 250, 700, 875, 1050)),
		RedDebug(f"{colours.fg.red}Avenue Henri-Martin{colours.reset}", 240, 150, (20, 100, 300, 750, 925, 1100)),
		StationDebug(f"{colours.fg.darkgrey}Gare du Nord{colours.reset}"),
		YellowDebug(f"{colours.fg.yellow}Faubourg Saint-Honoré{colours.reset}", 260, 150, (22, 110, 330, 800, 975, 1150)),
		YellowDebug(f"{colours.fg.yellow}Place de la bourse{colours.reset}", 260, 150, (22, 110, 330, 800, 975, 1150)),
		CompanyDebug(f"{colours.italic}Service de distribution des eaux{colours.reset}"),
		YellowDebug(f"{colours.fg.yellow}Rue la Fayette{colours.reset}", 280, 150, (24, 120, 360, 850, 1025, 1200)),
		PrisonDebug(f"{colours.italic}Prison{colours.reset}"),
		GreenDebug(f"{colours.fg.green}Avenue de Breteuil{colours.reset}", 300, 200, (26, 130, 390, 900, 1100, 1275)),
		GreenDebug(f"{colours.fg.green}Avenue Foch{colours.reset}", 300, 200, (26, 130, 390, 900, 1100, 1275)),
		CaisseDebug(board.caisse_deck),
		GreenDebug(f"{colours.fg.green}Boulevard des Capucines{colours.reset}", 320, 200, (28, 150, 450, 1000, 1200, 1400)),
		StationDebug(f"{colours.fg.darkgrey}Gare Saint-Lazare{colours.reset}"),
		ChanceDebug(board.chance_deck),
		BlueDebug(f"{colours.fg.blue}Avenue des Champs-Élysées{colours.reset}", 350, 200, (35, 175, 500, 1100, 1300, 1500)),
		TaxDebug(f"{colours.italic}Taxe de Luxe{colours.reset}", 100),
		BlueDebug(f"{colours.fg.blue}Rue de la paix{colours.reset}", 400, 200, (50, 200, 600, 1400, 1700, 2000)),
	]
)

for _ in range(100):
	player = next(board.players)
	board.turn_of(player)
