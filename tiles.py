from colours import *
from numpy import random


class Tile:
    # Shortcuts TODO : make those consistent with the plateau list of tiles
    DEPART = 0
    IMPOTS_SUR_LE_REVENU = 4
    GARE_MONTPARNASSE = 5
    SIMPLE_VISITE = 10
    BOULEVARD_DE_LA_VILLETTE = 11
    COMPAGNIE_D_ELECTRICITE = 12
    GARE_DE_LYON = 15
    AVENUE_HENRI_MARTIN = 24
    GARE_DU_NORD = 25
    COMPAGNIE_D_EAU = 28
    PRISON = 30
    GARE_SAINT_LAZARE = 35
    TAXE_DE_LUXE = 38
    RUE_DE_LA_PAIX = 39
    TOTAL = 40

    def closest_station(position):
        if Tile.GARE_MONTPARNASSE <= position < Tile.GARE_DE_LYON:
            return Tile.GARE_DE_LYON
        elif Tile.GARE_DE_LYON <= position < Tile.GARE_DU_NORD:
            return Tile.GARE_DU_NORD
        elif Tile.GARE_DU_NORD <= position < Tile.GARE_SAINT_LAZARE:
            return Tile.GARE_SAINT_LAZARE
        return Tile.GARE_MONTPARNASSE

    def closest_company(position):
        if Tile.COMPAGNIE_D_ELECTRICITE <= position < Tile.COMPAGNIE_D_EAU:
            return Tile.COMPAGNIE_D_EAU
        return Tile.COMPAGNIE_D_ELECTRICITE

    def __init__(self, displayer):
        self.displayer = displayer


class Prison(Tile):
    pass


class Tax(Tile):
    def __init__(self, value, displayer):
        Tile.__init__(self, displayer)
        self.value = value

    def tax_from(self, player):
        player.lose(self.value)


class Purchasable(Tile):
    def __init__(self, price, displayer):
        Tile.__init__(self, displayer)
        self.price = price
        self.owner = None

    def rent_from(self, player, double, dice1, dice2):
        rent = self.compute_rent(double, dice1, dice2)
        payed = player.lose(rent)
        self.owner.win(payed)


class Station(Purchasable):
    def __init__(self, displayer):
        super().__init__(200, displayer)

    def buy_update_rent(self, wallet_group):
        rent = 25 * len(wallet_group)
        for t in wallet_group:
            t.compute_rent = lambda double, dice1, dice2 : rent


class Company(Purchasable):
    def __init__(self, displayer):
        super().__init__(150, displayer)

    def buy_update_rent(self, wallet_group):
        monopoly = wallet_group == self.group
        multiplier = 10 if monopoly else 4
        for t in wallet_group:
            t.compute_rent = lambda double, dice1, dice2 : multiplier * (dice1 + dice2)


class Coloured(Purchasable):
    HOTEL = 5  # Pas de crise du logement pris en compte

    def __init__(self, price, construction, rents, displayer):
        super().__init__(price, displayer)
        self.construction = construction
        self.rents = rents

    def buy_update_rent(self, wallet_group):
        monopoly = wallet_group == self.group
        for t in wallet_group:
            t.compute_rent = lambda double, dice1, dice2 : t.rents[0] * (1 + monopoly)

    def construct_update_rent(self, wallet_group):
        assert wallet_group == self.group
        assert self.construction < Coloured.HOTEL
        self.construction += 1
        for t in wallet_group:
            t.compute_rent = lambda double, dice1, dice2 : t.rents[t.construction]

class Brown(Coloured):
    pass

class Grey(Coloured):
    pass

class Pink(Coloured):
    pass

class Orange(Coloured):
    pass

class Red(Coloured):
    pass

class Yellow(Coloured):
    pass

class Green(Coloured):
    pass

class Blue(Coloured):
    pass

class Chance(Tile):
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

    def __init__(self, deck, displayer):
        super().__init__(displayer)
        self.deck = deck

    def make_deck():
        deck = list(range(Chance.TOTAL))
        random.shuffle(deck)
        return deck

    def action(self, player, players):
        card = self.deck.pop(0)  # enlève la card du sommet du deck

        if card == Chance.SORTIE_DE_PRISON:
            self.displayer.effect("Vous êtes libéré de prison.")
            player.chance_out = True  # ajoute à la main du player
            return False, False # not moved, not doubling

        self.deck.append(card) # repose la card dans le deck
        if card == Chance.AVANCEZ_DEPART:
            self.displayer.effect("Avancez jusqu'à la case départ")
            player.move_to(Tile.DEPART)
            return True, False # moved, not doubling
        elif card == Chance.ALLEZ_EN_PRISON:
            self.displayer.effect("Allez en prison !")
            player.move_to(Tile.PRISON)
            return True, False # moved, not doubling
        elif card == Chance.DIVIDENDE:
            self.displayer.effect("Recevez 50€ de dividendes")
            player.win(50)
        elif card == Chance.IMMEUBLE:
            self.displayer.effect("Vos placements immobiliers vous rapportent 150€")
            player.win(150)
        elif card == Chance.EXCES_DE_VITESSE:
            self.displayer.effect("Excès de vitesse : payez 15€")
            player.lose(15)
        elif card == Chance.PRESIDENT:
            self.displayer.effect("Vous êtes président : payez 50€ à chaque players")
            for j in players:
                player.pay(j, 50)
        elif card == Chance.REPARATION:
            self.displayer.effect("Frais de réparations : payez 25€ par maison et 100€ par hôtel")
            player.tax_construction(25, 100)
        elif card == Chance.RUE_DE_LA_PAIX:
            self.displayer.effect("Avancez rue de la Paix")
            player.move_to(Tile.RUE_DE_LA_PAIX)
            return True, False # moved, not doubling
        elif card == Chance.AVANCEZ_BOULEVARD_DE_LA_VILLETTE:
            self.displayer.effect("Avancez Boulevard de la Villette")
            player.move_to(Tile.BOULEVARD_DE_LA_VILLETTE)
            return True, False # moved, not doubling
        elif card == Chance.RENDEZ_VOUS_AVENUE_HENRI_MARTIN:
            self.displayer.effect("Rendez vous avenue Henri-Martin")
            player.move_to(Tile.AVENUE_HENRI_MARTIN)
            return True, False # moved, not doubling
        elif card == Chance.ALLEZ_GARE_MONTPARNASSE:
            self.displayer.effect("Avancez jusqu'à la gare Montparnasse")
            player.move_to(Tile.GARE_MONTPARNASSE)
            return True, False # moved, not doubling
        elif card == Chance.RECULEZ_DE_TROIS_CASES:
            self.displayer.effect("Reculez de 3 cases")
            player.move_to((player.position - 3) % Tile.TOTAL, step=-1)
            return True, False # moved, not doubling
        elif card in Chance.GARE_PLUS_PROCHE:
            self.displayer.effect("Allez à la gare la plus proche. Payer le loyer double")
            player.move_to(Tile.closest_station(player.position))
            return True, True # doubling, moved
        elif card == Chance.COMPAGNIE_PLUS_PROCHE:
            self.displayer.effect("Allez à la compagnie la plus proche. Payer le loyer double")
            player.move_to(Tile.closest_company(player.position))
            return True, True # doubling, moved
        return False, False # not moved, not doubling


class Caisse(Tile):
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

    def __init__(self, deck, displayer):
        super().__init__(displayer)
        self.deck = deck

    def make_deck():
        deck = list(range(Caisse.TOTAL))
        random.shuffle(deck)
        return deck

    def action(self, player, players):
        card = self.deck.pop(0)  # enlève la card du sommet du deck

        if card == Caisse.SORTIE_DE_PRISON:
            self.displayer.effect("Vous êtes libéré de prison.")
            player.caisse_out = True  # ajoute à la main du player
            return False, False # not moved, not doubling

        self.deck.append(card) # repose la card dans le deck
        if card == Caisse.AVANCEZ_DEPART:
            self.displayer.effect("Avancez jusqu'à la case départ")
            player.move_to(Tile.DEPART)
            return True, False # moved, not doubling
        elif card == Caisse.ALLEZ_EN_PRISON:
            self.displayer.effect("Allez en prison !")
            player.move_to(Tile.PRISON)
            return True, False # moved, not doubling
        elif card == Caisse.ASSURANCE_VIE:
            self.displayer.effect("Votre assurance vie vous rapporte 100€")
            player.win(100)
        elif card == Caisse.IMPOTS:
            self.displayer.effect("Erreur des impôts en votre faveur. Recevez 20€")
            player.win(20)
        elif card == Caisse.PLACEMENT:
            self.displayer.effect("Vos placement vous rapportent 100€")
            player.win(100)
        elif card == Caisse.HERITAGE:
            self.displayer.effect("Vous héritez de 100€")
            player.win(100)
        elif card == Caisse.BANQUE:
            self.displayer.effect("Erreur de la banque en votre faveur. Recevez 200€")
            player.win(200)
        elif card == Caisse.BEAUTE:
            self.displayer.effect("Vous remportez le prix de beauté. Recevez 10€")
            player.win(10)
        elif card == Caisse.EXPERT:
            self.displayer.effect("Expert ? Recevez 25€")
            player.win(25)
        elif card == Caisse.STOCK:
            self.displayer.effect("Vos actions vous rapportent 50€")
            player.win(50)
        elif card == Caisse.HOSPITALISATION:
            self.displayer.effect("Payez 100€ de fraix d'hospitalisation")
            player.lose(100)
        elif card == Caisse.MEDECIN:
            self.displayer.effect("Payez 50€ de fraix de médecin")
            player.lose(50)
        elif card == Caisse.SCOLARITE:
            self.displayer.effect("Payez 50 € de fraix de scolarité")
            player.lose(50)
        elif card == Caisse.ANNIVERSAIRE:
            self.displayer.effect("C'est votre anniversaire. Recevez 10€ de la part de chaque player")
            for j in players:
                j.pay(player, 10)
        elif card == Caisse.TRAVAUX:
            self.displayer.effect("Travaux : payez 40€ par maison et 115€ par hôtel")
            player.tax_construction(40, 115)
        return False, False # not moved, not doubling