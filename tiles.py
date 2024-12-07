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


class Prison(Tile):
	pass


class Tax(Tile):
	def __init__(self, value):
		self.value = value

	def tax_from(self, player):
		player.lose(self.value)


class Purchasable(Tile):
	def __init__(self, price):
		self.price = price
		self.owner = None


class Station(Purchasable):
	def __init__(self):
		super().__init__(200)

	def buy_update_rent(self, wallet_group):
		rent = 25 * len(wallet_group)
		for t in wallet_group:
			t.compute_rent = lambda double, dice1, dice2: rent


class Company(Purchasable):
	def __init__(self):
		super().__init__(150)

	def buy_update_rent(self, wallet_group):
		monopoly = wallet_group == self.group
		multiplier = 10 if monopoly else 4
		for t in wallet_group:
			t.compute_rent = lambda double, dice1, dice2: multiplier * (dice1 + dice2)


class Coloured(Purchasable):
	HOTEL = 5  # Pas de crise du logement pris en compte

	def __init__(self, price, construction, rents):
		super().__init__(price)
		self.construction = construction
		self.rents = rents

	def buy_update_rent(self, wallet_group):
		monopoly = wallet_group == self.group
		for t in wallet_group:
			t.compute_rent = lambda double, dice1, dice2: t.rents[0] * (1 + monopoly)

	def construct_update_rent(self, wallet_group):
		assert wallet_group == self.group
		assert self.construction < Coloured.HOTEL
		self.construction += 1
		for t in wallet_group:
			t.compute_rent = lambda double, dice1, dice2: t.rents[t.construction]


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

	def __init__(self, deck):
		self.deck = deck

	def make_deck():
		deck = list(range(Chance.TOTAL))
		random.shuffle(deck)
		return deck

	def action(self, player, players):
		card = self.deck.pop(0)  # enlève la card du sommet du deck

		if card == Chance.SORTIE_DE_PRISON:
			player.chance_out = True  # ajoute à la main du player
			return False, False, False  # not prison, not moved, not doubling

		self.deck.append(card)  # repose la card dans le deck
		if card == Chance.AVANCEZ_DEPART:
			player.move_to(Tile.DEPART)
			return False, True, False  # not prison, moved, not doubling
		elif card == Chance.ALLEZ_EN_PRISON:
			player.go_to_prison()
			return True, True, False  # prison, not moved, not doubling
		elif card == Chance.DIVIDENDE:
			player.win(50)
		elif card == Chance.IMMEUBLE:
			player.win(150)
		elif card == Chance.EXCES_DE_VITESSE:
			player.lose(15)
		elif card == Chance.PRESIDENT:
			for j in players:
				player.pay(j, 50)
		elif card == Chance.REPARATION:
			player.tax_construction(25, 100)
		elif card == Chance.RUE_DE_LA_PAIX:
			player.move_to(Tile.RUE_DE_LA_PAIX)
			return False, True, False  # not prison, moved, not doubling
		elif card == Chance.AVANCEZ_BOULEVARD_DE_LA_VILLETTE:
			player.move_to(Tile.BOULEVARD_DE_LA_VILLETTE)
			return False, True, False  # not prison, moved, not doubling
		elif card == Chance.RENDEZ_VOUS_AVENUE_HENRI_MARTIN:
			player.move_to(Tile.AVENUE_HENRI_MARTIN)
			return False, True, False  # not prison, moved, not doubling
		elif card == Chance.ALLEZ_GARE_MONTPARNASSE:
			player.move_to(Tile.GARE_MONTPARNASSE)
			return False, True, False  # not prison, moved, not doubling
		elif card == Chance.RECULEZ_DE_TROIS_CASES:
			player.move_to((player.position - 3) % Tile.TOTAL, step=-1)
			return False, True, False  # not prison, moved, not doubling
		elif card in Chance.GARE_PLUS_PROCHE:
			player.move_to(Tile.closest_station(player.position))
			return False, True, True  # doubling, moved
		elif card == Chance.COMPAGNIE_PLUS_PROCHE:
			player.move_to(Tile.closest_company(player.position))
			return False, True, True  # doubling, moved
		return False, False, False  # not prison, not moved, not doubling


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

	def __init__(self, deck):
		self.deck = deck

	def make_deck():
		deck = list(range(Caisse.TOTAL))
		random.shuffle(deck)
		return deck

	def action(self, player, players):
		card = self.deck.pop(0)  # enlève la card du sommet du deck

		if card == Caisse.SORTIE_DE_PRISON:
			player.caisse_out = True  # ajoute à la main du player
			return False, False, False  # not prison, not moved, not doubling

		self.deck.append(card)  # repose la card dans le deck
		if card == Caisse.AVANCEZ_DEPART:
			player.move_to(Tile.DEPART)
			return False, True, False  # not prison, moved, not doubling
		elif card == Caisse.ALLEZ_EN_PRISON:
			player.go_to_prison()
			return True, True, False  # prison, not moved, not doubling
		elif card == Caisse.ASSURANCE_VIE:
			player.win(100)
		elif card == Caisse.IMPOTS:
			player.win(20)
		elif card == Caisse.PLACEMENT:
			player.win(100)
		elif card == Caisse.HERITAGE:
			player.win(100)
		elif card == Caisse.BANQUE:
			player.win(200)
		elif card == Caisse.BEAUTE:
			player.win(10)
		elif card == Caisse.EXPERT:
			player.win(25)
		elif card == Caisse.STOCK:
			player.win(50)
		elif card == Caisse.HOSPITALISATION:
			player.lose(100)
		elif card == Caisse.MEDECIN:
			player.lose(50)
		elif card == Caisse.SCOLARITE:
			player.lose(50)
		elif card == Caisse.ANNIVERSAIRE:
			for j in players:
				j.pay(player, 10)
		elif card == Caisse.TRAVAUX:
			player.tax_construction(40, 115)
		return False, False, False  # not prison, not moved, not doubling


class TileDebug:
	def __str__(self):
		return self.name


class PrisonDebug(Prison, TileDebug):
	def __init__(self, name, *args):
		super().__init__(*args)
		self.name = name


class TaxDebug(Tax, TileDebug):
	def __init__(self, name, *args):
		super().__init__(*args)
		self.name = name


class StationDebug(Station, TileDebug):
	def __init__(self, name, *args):
		super().__init__(*args)
		self.name = name


class CompanyDebug(Company, TileDebug):
	def __init__(self, name, *args):
		super().__init__(*args)
		self.name = name


class BrownDebug(Coloured, TileDebug):
	def __init__(self, name, *args):
		super().__init__(*args)
		self.name = name


class GreyDebug(Coloured, TileDebug):
	def __init__(self, name, *args):
		super().__init__(*args)
		self.name = name


class PinkDebug(Coloured, TileDebug):
	def __init__(self, name, *args):
		super().__init__(*args)
		self.name = name


class OrangeDebug(Coloured, TileDebug):
	def __init__(self, name, *args):
		super().__init__(*args)
		self.name = name


class RedDebug(Coloured, TileDebug):
	def __init__(self, name, *args):
		super().__init__(*args)
		self.name = name


class YellowDebug(Coloured, TileDebug):
	def __init__(self, name, *args):
		super().__init__(*args)
		self.name = name


class GreenDebug(Coloured, TileDebug):
	def __init__(self, name, *args):
		super().__init__(*args)
		self.name = name


class BlueDebug(Coloured, TileDebug):
	def __init__(self, name, *args):
		super().__init__(*args)
		self.name = name


class ChanceDebug(Chance, TileDebug):
	def action(self, player, players):
		print(self.deck[0])
		effect = [
			"Vous êtes libéré de prison.",
			"Avancez jusqu'à la case départ",
			"Allez en prison !",
			"Recevez 50€ de dividendes",
			"Vos placements immobiliers vous rapportent 150€",
			"Excès de vitesse : payez 15€",
			"Vous êtes président : payez 50€ à chaque players",
			"Frais de réparations : payez 25€ par maison et 100€ par hôtel",
			"Avancez rue de la Paix",
			"Avancez Boulevard de la Villette",
			"Rendez vous avenue Henri-Martin",
			"Avancez jusqu'à la gare Montparnasse",
			"Reculez de 3 cases",
			"Allez à la gare la plus proche. Payer le loyer double",
			"Allez à la gare la plus proche. Payer le loyer double",
			"Allez à la compagnie la plus proche. Payer le loyer double",
		][self.deck[0]]
		print(f"\t{colours.bg.red}Chance{colours.reset} : {colours.bold}{effect}{colours.reset}")
		return super().action(player, players)


class CaisseDebug(Caisse, TileDebug):
	def action(self, player, players):
		print(self.deck[0])
		effect = [
			"Vous êtes libéré de prison.",
			"Avancez jusqu'à la case départ",
			"Allez en prison !",
			"Votre assurance vie vous rapporte 100€",
			"Erreur des impôts en votre faveur. Recevez 20€",
			"Vos placement vous rapportent 100€",
			"Vous héritez de 100€",
			"Erreur de la banque en votre faveur. Recevez 200€",
			"Vous remportez le prix de beauté. Recevez 10€",
			"Expert ? Recevez 25€",
			"Vos actions vous rapportent 50€",
			"Payez 100€ de fraix d'hospitalisation",
			"Payez 50€ de fraix de médecin",
			"Payez 50 € de fraix de scolarité",
			"C'est votre anniversaire. Recevez 10€ de la part de chaque player",
			"Travaux : payez 40€ par maison et 115€ par hôtel",
		][self.deck[0]]
		print(f"\t{colours.bg.blue}Caisse{colours.reset} : {colours.bold}{effect}{colours.reset}")
		return super().action(player, players)
