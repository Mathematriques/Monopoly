from tiles import *
from colours import *
from itertools import cycle
from numpy import random

class PlayerDebugDisplayer:
    def __init__(self, name):
        self.name = name

    def __call__(self, player):
        print(f"{self.name} est en {player.position}")

    def pay(self, amount):
        print(f"\t{self.name} donne {colours.fg.yellow}{amount}€{colours.reset}")

    def win(self, amount):
        print(f"\t{self.name} reçoit {colours.fg.yellow}{amount}€{colours.reset}")

    def go(self, position):
        print(f"{self.name} va en {position}")

    def go_to_prison(self):
        print(f"{colours.bg.red}{colours.fg.black}{self.name} va en Prison !{colours.reset}")

    def leave_prison(self):
        print(f"{colours.bg.gree}{self.name} va en Prison !{colours.reset}")


class TileDebugDisplayer:
    def __init__(self, name, colour):
        self.name = name
        self.colour = colour

    def __call__(self):
        print(f"Sur la case {self.colour}{self.name}{colours.reset}")


class Player:
    def __init__(self, displayer):
        self.displayer = displayer
        self.money = 1500
        self._go(Plateau.DEPART)
        self.doubles_in_a_row = 0
        self.turns_in_prison = 0

    def pay(self, amount):
        self.money -= amount
        self.displayer.pay(amount)
        print("Add player end")

    def win(self, amount):
        self.money += amount
        self.displayer.win(amount)

    def too_many_doubles(self, dice1, dice2):
        double = dice1 == dice2
        self.doubles_in_a_row = self.doubles_in_a_row + 1 if double else 0
        if self.doubles_in_a_row == 3:
            self.doubles_in_a_row = 0
            return True
        return False

    def _go(self, position):
        self.displayer.go(position)
        self.position = position

    def forward(self, position):
        while self.position != (position % Plateau.TOTAL):
            self._go((self.position + 1) % Plateau.TOTAL)
            if self.position == Plateau.DEPART:
                self.win(200)

    def go_to_prison(self):
        self.displayer.go_to_prison()
        self._go(Plateau.PRISON)
        self.turns_in_prison = 0

    def leave_prison(self):
        self.displayer.leave_prison()
        self._go(Plateau.SIMPLE_VISITE)
        self.turns_in_prison = 0


class Plateau:
    DEPART = 0
    SIMPLE_VISITE = 10
    PRISON = 30
    TOTAL = 40

    def __init__(self, players):
        self.players = cycle(players)
        self.tiles = [
            # fmt: off
            Tile(
                TileDebugDisplayer("Départ", colours.bold)
            ),
            Brown(60, 50, (2, 10, 30, 90, 160, 250), 
                TileDebugDisplayer("Boulevard de Belleville", colours.fg.brown)
            ),
            Caisse(
                TileDebugDisplayer("Caisse de Communauté", colours.bg.blue)
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
                TileDebugDisplayer("Chance", colours.bg.red)
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
                TileDebugDisplayer("Caisse de Communauté", colours.bg.blue)
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
                TileDebugDisplayer("Chance", colours.bg.red)
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
                TileDebugDisplayer("Caisse de Communauté", colours.bg.blue)
            ),
            Green(320, 200, (28, 150, 450, 1000, 1200, 1400), 
                TileDebugDisplayer("Boulevard des Capucines", colours.fg.green)
            ),
            Station(
                TileDebugDisplayer("Gare Saint-Lazare", colours.fg.darkgrey)
            ),
            Chance(
                TileDebugDisplayer("Chance", colours.bg.red)
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


plateau = Plateau(
    [Player(PlayerDebugDisplayer("Toto")), Player(PlayerDebugDisplayer("Tata"))]
)
for _ in range(100):
    player = next(plateau.players)
    player.displayer(player)

    if player.position == Plateau.PRISON:
        print("Ajouter les tours en prison")
        continue

    dice1, dice2 = random.randint(1, 7, 2)
    if player.too_many_doubles(dice1, dice2):
        player.go_to_prison()
        continue

    player.forward(player.position + dice1 + dice2)

    tile = plateau.tiles[player.position]
    tile.displayer()
    if type(tile) is Tile:
        print("Rien de spécial")
    elif isinstance(tile, Prison):
        player.go_to_prison()
        continue
    elif isinstance(tile, Purchasable) and tile.owner is None:
        print("Ajouter le mechanisme d'achat")
    elif isinstance(tile, Caisse):
        print("Faire la misère au joueur")
    elif isinstance(tile, Chance):
        print("Faire la misère au joueur")
    else:
        tile.take_money_from(player)
