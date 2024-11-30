from tiles import *
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
        print(f"\t\t{self.name} donne {colours.fg.yellow}{amount}€{colours.reset}")

    def win(self, amount):
        print(f"\t\t{self.name} reçoit {colours.fg.yellow}{amount}€{colours.reset}")

    def pay(self, other, amount):
        print(f"\t\t{self.name} −−{colours.fg.yellow}{amount}€{colours.reset}−−> {other.displayer.name}")

    def step(self):
        return
        print(f"{self.name} avance d'une case")

    def go_to_prison(self):
        print(f"{colours.bg.red}{colours.fg.black}{self.name} va en Prison !{colours.reset}")

    def leave_prison(self):
        print(f"{colours.bg.green}{colours.fg.black}{self.name} Sort de Prison !{colours.reset}")

    def in_prison(self):
        print(f"Tour de {self.name} qui a {colours.fg.yellow}{player.money}€{colours.reset} est en Prison")


class TileDebugDisplayer:
    def __init__(self, name, colour):
        self.name = name
        self.colour = colour

    def __call__(self):
        print(f"\tSur la case {self.colour}{self.name}{colours.reset}")


class ChanceDebugDisplayer:
    def __call__(self):
        print(f"\tSur la case {colours.bg.red}Chance{colours.reset}")

    def effect(self, description):
        print(f"\t\t{colours.bold}{description}{colours.reset}")


class CaisseDebugDisplayer:
    def __call__(self):
        print(f"\tSur la case {colours.bg.blue}Caisse{colours.reset}")

    def effect(self, description):
        print(f"\t\t{colours.bold}{description}{colours.reset}")


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
                return True # stay in prison
        
        elif self.turns_in_prison < 3:
            if dice1 != dice2:
                return True # stay in prison

        player.leave_prison()
        return False

    def buy(self, tile):
        self.lose(tile.price)
        group = type(tile)
        self.wallet[group].add(tile)
        tile.owner = self
        tile.buy_update_rent(self.wallet[group])


class Board:
    def __init__(self, players):
        self.players = cycle(players)
        self.chance_deck = Chance.make_deck()
        self.caisse_deck = Caisse.make_deck()
        self.tiles = [
            # fmt: on
            Tile(
                TileDebugDisplayer("Départ", colours.bold)
            ),
            Brown(60, 50, (2, 10, 30, 90, 160, 250), 
                TileDebugDisplayer("Boulevard de Belleville", colours.fg.brown)
            ),
            Caisse(
                self.caisse_deck,
                CaisseDebugDisplayer()
            ),
            Brown(60, 50, (4, 20, 60, 180, 320, 450), 
                TileDebugDisplayer("Rue Lecourbe", colours.fg.brown)
            ),
            Tax(200, 
                TileDebugDisplayer("Impôt sur le revenu", colours.bold)
            ),
            Station(
                TileDebugDisplayer("Gare Montparnasse", colours.fg.darkgrey)
            ),
            Grey(100, 50, (6, 30, 90, 270, 400, 550), 
                TileDebugDisplayer("Rue Vaugirard", colours.fg.lightgrey)
            ),
            Chance(
                self.chance_deck,
                ChanceDebugDisplayer()
            ),
            Grey(100, 50, (6, 30, 90, 270, 400, 550), 
                TileDebugDisplayer("Rue de Courcelles", colours.fg.lightgrey)
            ),
            Grey(120, 50, (8, 40, 100, 300, 450, 600), 
                TileDebugDisplayer("Avenue de la République", colours.fg.lightgrey)
            ),
            Tile(
                TileDebugDisplayer("Simple Visite", colours.bold)
            ),
            Pink(140, 100, (10, 50, 150, 450, 625, 750), 
                TileDebugDisplayer("Boulevard de la Villette", colours.fg.pink)
            ),
            Company(
                TileDebugDisplayer("Service de distribution d'éléctricité", colours.bold)
            ),
            Pink(140, 100, (10, 50, 150, 450, 625, 750), 
                TileDebugDisplayer("Avenue de Neuilly", colours.fg.pink)
            ),
            Pink(160, 100, (12, 60, 180, 500, 700, 900), 
                TileDebugDisplayer("Rue de Paradis", colours.fg.pink)
            ),
            Station(
                TileDebugDisplayer("Gare de Lyon", colours.fg.darkgrey)
            ),
            Orange(180, 100, (14, 70, 200, 550, 750, 950), 
                TileDebugDisplayer("Avenue Mozart", colours.fg.brown)
            ),
            Caisse(
                self.caisse_deck,
                CaisseDebugDisplayer()
            ),
            Orange(180, 100, (14, 70, 200, 550, 750, 950), 
                TileDebugDisplayer("Boulevard Saint-Michel", colours.fg.brown)
            ),
            Orange(200, 100, (16, 80, 220, 600, 800, 1000), 
                TileDebugDisplayer("Place Pigalle", colours.fg.brown)
            ),
            Tile(
                TileDebugDisplayer("Parc gratuit", colours.bold)
            ),
            Red(220, 150, (18, 90, 250, 700, 875, 1050), 
                TileDebugDisplayer("Avenue Matignon", colours.fg.red)
            ),
            Chance(
                self.chance_deck,
                ChanceDebugDisplayer()
            ),
            Red(220, 150, (18, 90, 250, 700, 875, 1050), 
                TileDebugDisplayer("Boulevard Malesherbes", colours.fg.red)
            ),
            Red(240, 150, (20, 100, 300, 750, 925, 1100), 
                TileDebugDisplayer("Avenue Henri-Martin", colours.fg.red)
            ),
            Station(
                TileDebugDisplayer("Gare du Nord", colours.fg.darkgrey)
            ),
            Yellow(260, 150, (22, 110, 330, 800, 975, 1150), 
                TileDebugDisplayer("Faubourg Saint-Honoré", colours.fg.yellow)
            ),
            Yellow(260, 150, (22, 110, 330, 800, 975, 1150), 
                TileDebugDisplayer("Place de la bourse", colours.fg.yellow)
            ),
            Company(
                TileDebugDisplayer("Service de distribution des eaux", colours.bold)
            ),
            Yellow(280, 150, (24, 120, 360, 850, 1025, 1200), 
                TileDebugDisplayer("Rue la Fayette", colours.fg.yellow)
            ),
            Prison(
                TileDebugDisplayer("Prison", colours.bold)
            ),
            Green(300, 200, (26, 130, 390, 900, 1100, 1275), 
                TileDebugDisplayer("Avenue de Breteuil", colours.fg.green)
            ),
            Green(300, 200, (26, 130, 390, 900, 1100, 1275), 
                TileDebugDisplayer("Avenue Foch", colours.fg.green)
            ),
            Caisse(
                self.caisse_deck,
                CaisseDebugDisplayer()
            ),
            Green(320, 200, (28, 150, 450, 1000, 1200, 1400), 
                TileDebugDisplayer("Boulevard des Capucines", colours.fg.green)
            ),
            Station(
                TileDebugDisplayer("Gare Saint-Lazare", colours.fg.darkgrey)
            ),
            Chance(
                self.chance_deck,
                ChanceDebugDisplayer()
            ),
            Blue(350, 200, (35, 175, 500, 1100, 1300, 1500), 
                TileDebugDisplayer("Avenue des Champs-Élysées", colours.fg.blue)
            ),
            Tax(100, 
                TileDebugDisplayer("Taxe de Luxe", colours.bold)
            ),
            Blue(400, 200, (50, 200, 600, 1400, 1700, 2000), 
                TileDebugDisplayer("Rue de la paix", colours.fg.blue)
            ),
            # fmt: on
        ]

        # TODO : Dirty monkey patching
        groups = defaultdict(set)
        for t in self.tiles:
            groups[type(t)].add(t)

        for t in self.tiles:
            t.group = groups[type(t)]


players = [Player(PlayerDebugDisplayer("Toto")), Player(PlayerDebugDisplayer("Tata"))]
board = Board(players)

for _ in range(100):
    player = next(board.players)
    dice1, dice2 = random.randint(1, 7, 2)

    # Special cases
    if player.position == Tile.PRISON:
        stay = player.in_prison_and_stay(dice1, dice2, board)
        if stay:
            continue
    elif player.too_many_doubles(dice1, dice2):
        player.go_to_prison()
        continue

    # Normal move
    player.displayer(player)
    player.move_from_dice(dice1, dice2)
    tile = board.tiles[player.position]
    tile.displayer()

    double = False

    if isinstance(tile, Prison):
        player.go_to_prison()
        continue
    elif isinstance(tile, Tax):
        tile.tax_from(player)
    elif isinstance(tile, Chance) or isinstance(tile, Caisse):
        moved, double = tile.action(player, players)
        if moved:
            if player.position == Tile.PRISON:
                player.go_to_prison()
                continue
            tile = board.tiles[player.position]
            tile.displayer()
    if isinstance(tile, Purchasable):
        if tile.owner:
            tile.rent_from(player, double, dice1, dice2)
        elif player.veut_acheter(tile) and player.money >= tile.price:
            player.buy(tile)

    print("Add constructions")
