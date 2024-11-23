from numpy import random


class Prison:
    pass


class Tax:
    def __init__(self, value):
        self.value = value

    def action(self, player):
        player.pay(self.value)


class Purchasable:
    def __init__(self, price):
        self.price = price
        self.rent = 0
        self.owner = None

    def action(self, player):
        payed = player.pay(self.rent)
        self.owner.receive(payed)


class Station(Purchasable):
    def __init__(self):
        super().__init__(200)

    def update_rent(self, number_stations):
        self.rent = 25 * number_stations


class Company(Purchasable):
    def __init__(self):
        super().__init__(150)

    def update_rent(self, monopoly):
        # member rent works as a dice multiplier here
        self.rent = 10 if monopoly else 4

    def action(self, player, dices):
        payed = player.pay(self.rent * sum(dices))
        self.owner.receive(payed)


class Coloured(Purchasable):  # Interface
    def __init__(self, price, rents):
        super().__init__(price)
        super().properties.append(self)
        self.rents = rents

    def update_rent(self, monopoly, developpement):
        if developpement == 0 and not monopoly:
            self.rent = 2 * self.rents[0]
        else:
            self.rent = self.rents[developpement]


class Brown(Coloured):
    properties = []


class Grey(Coloured):
    properties = []


class Pink(Coloured):
    properties = []


class Orange(Coloured):
    properties = []


class Red(Coloured):
    properties = []


class Yellow(Coloured):
    properties = []


class Green(Coloured):
    properties = []


class Blue(Coloured):
    properties = []


class Chance:
    SORTIE_DE_PRISON = 0
    AVANCEZ_DEPART = 1
    ALLEZ_EN_PRISON = 2
    RUE_DE_LA_PAIX = 3
    AVANCEZ_BOULEVARD_DE_LA_VILLETTE = 4
    RENDEZ_VOUS_AVENUE_HENRI_MARTIN = 5
    ALLEZ_GARE_MONTPARNASSE = 6
    RECULEZ_DE_TROIS_CASES = 7
    DIVIDENDE = 8
    IMMEUBLE = 9
    EXCES_DE_VITESSE = 10
    PRESIDENT = 11
    REPARATION = 12
    GARE_PLUS_PROCHE = (13, 14)
    COMPAGNIE_PLUS_PROCHE = 15
    TOTAL = 16

    deck = list(range(TOTAL))
    random.shuffle(deck)


class Caisse:
    SORTIE_DE_PRISON = 0
    AVANCEZ_DEPART = 1
    ALLEZ_EN_PRISON = 2
    ASSURANCE_VIE = 3
    IMPOTS = 4
    PLACEMENT = 5
    HERITAGE = 6
    BANQUE = 7
    BEAUTE = 8
    EXPERT = 9
    STOCK = 10
    HOSPITALISATION = 11
    MEDECIN = 12
    SCOLARITE = 13
    ANNIVERSAIRE = 14
    TRAVAUX = 15
    TOTAL = 16

    deck = list(range(TOTAL))
    random.shuffle(deck)
