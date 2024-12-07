from tiles import *
from player import *
from board import *

from colours import *


players = [PlayerDebug("Toto"), PlayerDebug("Tata")]
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
	player = next(board.players_cycle)
	player.sumup()
	board.turn_of(player)
