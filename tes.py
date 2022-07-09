import logging
from src.format.format_controller import Format
from src.deck.deck_controller import Deck

logging.getLogger("scrapy").propagate = False
logging.getLogger("filelock").propagate = False
logging.getLogger("urllib3.connectionpool").propagate = False
# a = Format("pioneer")
# a.get_spiders_data()

deck_1_raw = {
    "source": "mtg_top8_decks_events",
    "name": "Transmogrify",
    "link": "https://mtgtop8.com/event?e=37074&d=478337&f=PI",
    "format": "pioneer",
    "cards": [
        {
            "name": "Boseiju, Who Endures",
            "cuantity": "1 ",
            "rarity": "",
            "mana_cost": "",
        },
        {"name": "Breeding Pool", "cuantity": "3 ", "rarity": "", "mana_cost": ""},
        {"name": "Cragcrown Pathway", "cuantity": "2 ", "rarity": "", "mana_cost": ""},
        {"name": "Den of the Bugbear", "cuantity": "2 ", "rarity": "", "mana_cost": ""},
        {"name": "Dreamroot Cascade", "cuantity": "1 ", "rarity": "", "mana_cost": ""},
        {"name": "Lair of the Hydra", "cuantity": "1 ", "rarity": "", "mana_cost": ""},
        {"name": "Rockfall Vale", "cuantity": "2 ", "rarity": "", "mana_cost": ""},
        {"name": "Rootbound Crag", "cuantity": "1 ", "rarity": "", "mana_cost": ""},
        {
            "name": "Sokenzan, Crucible of Defiance",
            "cuantity": "1 ",
            "rarity": "",
            "mana_cost": "",
        },
        {"name": "Steam Vents", "cuantity": "1 ", "rarity": "", "mana_cost": ""},
        {"name": "Stomping Ground", "cuantity": "4 ", "rarity": "", "mana_cost": ""},
        {"name": "Stormcarved Coast", "cuantity": "3 ", "rarity": "", "mana_cost": ""},
        {"name": "Sulfur Falls", "cuantity": "1 ", "rarity": "", "mana_cost": ""},
        {
            "name": "Koma, Cosmos Serpent",
            "cuantity": "2 ",
            "rarity": "",
            "mana_cost": "",
        },
        {"name": "Titan of Industry", "cuantity": "2 ", "rarity": "", "mana_cost": ""},
        {"name": "Fire Prophecy", "cuantity": "3 ", "rarity": "", "mana_cost": ""},
        {"name": "Flame-Blessed Bolt", "cuantity": "2 ", "rarity": "", "mana_cost": ""},
        {"name": "Strangle", "cuantity": "3 ", "rarity": "", "mana_cost": ""},
        {"name": "Transmogrify", "cuantity": "4 ", "rarity": "", "mana_cost": ""},
        {"name": "Valakut Awakening", "cuantity": "1 ", "rarity": "", "mana_cost": ""},
        {
            "name": "Careful Cultivation",
            "cuantity": "4 ",
            "rarity": "",
            "mana_cost": "",
        },
        {
            "name": "Courier's Briefcase",
            "cuantity": "4 ",
            "rarity": "",
            "mana_cost": "",
        },
        {"name": "Esika's Chariot", "cuantity": "4 ", "rarity": "", "mana_cost": ""},
        {
            "name": "Fable of the Mirror-Breaker",
            "cuantity": "4 ",
            "rarity": "",
            "mana_cost": "",
        },
        {
            "name": "Lukka, Coppercoat Outcast",
            "cuantity": "2 ",
            "rarity": "",
            "mana_cost": "",
        },
        {
            "name": "Nissa, Voice of Zendikar",
            "cuantity": "2 ",
            "rarity": "",
            "mana_cost": "",
        },
    ],
}

deck_2_raw = {
    "source": "goldfish_decks",
    "name": "\nEsper Control\n",
    "format": "pioneer",
    "format_info": '<div class="archetype-tile-statistic-value">\n1.8%\n<span class="archetype-tile-statistic-value-extra-data">\n(12)\n</span>\n</div>',
    "sections": {
        "Companion(1)": [
            {
                "name": "Yorion, Sky Nomad",
                "cuantity": "\n1\n",
                "rarity": "\n1\u00a0Rare\n",
                "mana_cost": " 3 hyrid white blue hyrid white blue",
            }
        ],
        "Planeswalkers(9)": [
            {
                "name": "Narset, Parter of Veils",
                "cuantity": "\n1\n",
                "rarity": "\n1\u00a0Unc.\n",
                "mana_cost": " 1 blue blue",
            },
            {
                "name": "The Wandering Emperor",
                "cuantity": "\n4\n",
                "rarity": "\n4\u00a0Mythic\n",
                "mana_cost": " 2 white white",
            },
            {
                "name": "Teferi, Hero of Dominaria",
                "cuantity": "\n4\n",
                "rarity": "\n4\u00a0Mythic\n",
                "mana_cost": " 3 white blue",
            },
        ],
        "Spells(27)": [
            {
                "name": "Bloodchief's Thirst",
                "cuantity": "\n1\n",
                "rarity": "\n1\u00a0Unc.\n",
                "mana_cost": " black",
            },
            {
                "name": "Fatal Push",
                "cuantity": "\n4\n",
                "rarity": "\n4\u00a0Unc.\n",
                "mana_cost": " black",
            },
            {
                "name": "Thoughtseize",
                "cuantity": "\n4\n",
                "rarity": "\n4\u00a0Rare\n",
                "mana_cost": " black",
            },
            {
                "name": "Doom Blade",
                "cuantity": "\n1\n",
                "rarity": "\n1\u00a0Comm.\n",
                "mana_cost": " 1 black",
            },
            {
                "name": "Dovin's Veto",
                "cuantity": "\n2\n",
                "rarity": "\n2\u00a0Unc.\n",
                "mana_cost": " white blue",
            },
            {
                "name": "Heartless Act",
                "cuantity": "\n1\n",
                "rarity": "\n1\u00a0Unc.\n",
                "mana_cost": " 1 black",
            },
            {
                "name": "Vanishing Verse",
                "cuantity": "\n2\n",
                "rarity": "\n2\u00a0Rare\n",
                "mana_cost": " white black",
            },
            {
                "name": "Absorb",
                "cuantity": "\n3\n",
                "rarity": "\n3\u00a0Rare\n",
                "mana_cost": " white blue blue",
            },
            {
                "name": "Void Rend",
                "cuantity": "\n2\n",
                "rarity": "\n2\u00a0Rare\n",
                "mana_cost": " white blue black",
            },
            {
                "name": "Memory Deluge",
                "cuantity": "\n4\n",
                "rarity": "\n4\u00a0Rare\n",
                "mana_cost": " 2 blue blue",
            },
            {
                "name": "Supreme Verdict",
                "cuantity": "\n3\n",
                "rarity": "\n3\u00a0Rare\n",
                "mana_cost": " 1 white white blue",
            },
        ],
        "Enchantments(8)": [
            {
                "name": "Omen of the Sea",
                "cuantity": "\n4\n",
                "rarity": "\n4\u00a0Comm.\n",
                "mana_cost": " 1 blue",
            },
            {
                "name": "Oath of Kaya",
                "cuantity": "\n2\n",
                "rarity": "\n2\u00a0Rare\n",
                "mana_cost": " 1 white black",
            },
            {
                "name": "Shark Typhoon",
                "cuantity": "\n2\n",
                "rarity": "\n2\u00a0Rare\n",
                "mana_cost": " 5 blue",
            },
        ],
        "Lands(36)": [
            {
                "name": "Deserted Beach",
                "cuantity": "\n4\n",
                "rarity": "\n4\u00a0Rare\n",
                "mana_cost": "0",
            },
            {
                "name": "Drowned Catacomb",
                "cuantity": "\n2\n",
                "rarity": "\n2\u00a0Rare\n",
                "mana_cost": "0",
            },
            {
                "name": "Eiganjo, Seat of the Empire",
                "cuantity": "\n1\n",
                "rarity": "\n1\u00a0Rare\n",
                "mana_cost": "0",
            },
            {
                "name": "Fetid Pools",
                "cuantity": "\n3\n",
                "rarity": "\n3\u00a0Rare\n",
                "mana_cost": "0",
            },
            {
                "name": "Glacial Fortress",
                "cuantity": "\n4\n",
                "rarity": "\n4\u00a0Rare\n",
                "mana_cost": "0",
            },
            {
                "name": "Godless Shrine",
                "cuantity": "\n4\n",
                "rarity": "\n4\u00a0Rare\n",
                "mana_cost": "0",
            },
            {
                "name": "Hallowed Fountain",
                "cuantity": "\n2\n",
                "rarity": "\n2\u00a0Rare\n",
                "mana_cost": "0",
            },
            {"name": "Island", "cuantity": "\n1\n", "rarity": "\n\n", "mana_cost": "0"},
            {
                "name": "Isolated Chapel",
                "cuantity": "\n1\n",
                "rarity": "\n1\u00a0Rare\n",
                "mana_cost": "0",
            },
            {
                "name": "Otawara, Soaring City",
                "cuantity": "\n1\n",
                "rarity": "\n1\u00a0Rare\n",
                "mana_cost": "0",
            },
            {"name": "Plains", "cuantity": "\n1\n", "rarity": "\n\n", "mana_cost": "0"},
            {
                "name": "Raffine's Tower",
                "cuantity": "\n4\n",
                "rarity": "\n4\u00a0Rare\n",
                "mana_cost": "0",
            },
            {
                "name": "Shambling Vent",
                "cuantity": "\n3\n",
                "rarity": "\n3\u00a0Rare\n",
                "mana_cost": "0",
            },
            {
                "name": "Shipwreck Marsh",
                "cuantity": "\n1\n",
                "rarity": "\n1\u00a0Rare\n",
                "mana_cost": "0",
            },
            {
                "name": "Watery Grave",
                "cuantity": "\n4\n",
                "rarity": "\n4\u00a0Rare\n",
                "mana_cost": "0",
            },
        ],
        "Sideboard(15) including Companion": [
            {
                "name": "Aether Gust",
                "cuantity": "\n4\n",
                "rarity": "\n4\u00a0Unc.\n",
                "mana_cost": " 1 blue",
            },
            {
                "name": "Malevolent Hermit",
                "cuantity": "\n3\n",
                "rarity": "\n3\u00a0Rare\n",
                "mana_cost": " 1 blue",
            },
            {
                "name": "Graveyard Trespasser",
                "cuantity": "\n3\n",
                "rarity": "\n3\u00a0Rare\n",
                "mana_cost": " 2 black",
            },
            {
                "name": "Kaya, Orzhov Usurper",
                "cuantity": "\n1\n",
                "rarity": "\n1\u00a0Mythic\n",
                "mana_cost": " 1 white black",
            },
            {
                "name": "Mystical Dispute",
                "cuantity": "\n2\n",
                "rarity": "\n2\u00a0Unc.\n",
                "mana_cost": " 2 blue",
            },
            {
                "name": "Narset, Parter of Veils",
                "cuantity": "\n1\n",
                "rarity": "\n1\u00a0Unc.\n",
                "mana_cost": " 1 blue blue",
            },
        ],
    },
    "link": "https://www.mtggoldfish.com/archetype/pioneer-esper-control-8413f5ae-6d65-4826-992a-9c2e3511890d",
}

d1 = Deck(deck_1_raw)
d1.get_info()
d2 = Deck(deck_2_raw)
d2.get_info()
