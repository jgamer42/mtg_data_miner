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
        },
        {"name": "Breeding Pool", "cuantity": "3 "},
        {
            "name": "Cragcrown Pathway",
            "cuantity": "2 ",
        },
        {
            "name": "Den of the Bugbear",
            "cuantity": "2 ",
        },
        {
            "name": "Dreamroot Cascade",
            "cuantity": "1 ",
        },
        {
            "name": "Lair of the Hydra",
            "cuantity": "1 ",
        },
        {
            "name": "Rockfall Vale",
            "cuantity": "2 ",
        },
        {
            "name": "Rootbound Crag",
            "cuantity": "1 ",
        },
        {
            "name": "Sokenzan, Crucible of Defiance",
            "cuantity": "1 ",
        },
        {
            "name": "Steam Vents",
            "cuantity": "1 ",
        },
        {
            "name": "Stomping Ground",
            "cuantity": "4 ",
        },
        {
            "name": "Stormcarved Coast",
            "cuantity": "3 ",
        },
        {
            "name": "Sulfur Falls",
            "cuantity": "1 ",
        },
        {
            "name": "Koma, Cosmos Serpent",
            "cuantity": "2 ",
        },
        {
            "name": "Titan of Industry",
            "cuantity": "2 ",
        },
        {
            "name": "Fire Prophecy",
            "cuantity": "3 ",
        },
        {
            "name": "Flame-Blessed Bolt",
            "cuantity": "2 ",
        },
        {
            "name": "Strangle",
            "cuantity": "3 ",
        },
        {
            "name": "Transmogrify",
            "cuantity": "4 ",
        },
        {
            "name": "Valakut Awakening",
            "cuantity": "1 ",
        },
        {
            "name": "Careful Cultivation",
            "cuantity": "4 ",
        },
        {
            "name": "Courier's Briefcase",
            "cuantity": "4 ",
        },
        {
            "name": "Esika's Chariot",
            "cuantity": "4 ",
        },
        {
            "name": "Fable of the Mirror-Breaker",
            "cuantity": "4 ",
        },
        {
            "name": "Lukka, Coppercoat Outcast",
            "cuantity": "2 ",
        },
        {
            "name": "Nissa, Voice of Zendikar",
            "cuantity": "2 ",
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
            }
        ],
        "Planeswalkers(9)": [
            {
                "name": "Narset, Parter of Veils",
                "cuantity": "\n1\n",
            },
            {
                "name": "The Wandering Emperor",
                "cuantity": "\n4\n",
            },
            {
                "name": "Teferi, Hero of Dominaria",
                "cuantity": "\n4\n",
            },
        ],
        "Spells(27)": [
            {
                "name": "Bloodchief's Thirst",
                "cuantity": "\n1\n",
            },
            {
                "name": "Fatal Push",
                "cuantity": "\n4\n",
            },
            {
                "name": "Thoughtseize",
                "cuantity": "\n4\n",
            },
            {
                "name": "Doom Blade",
                "cuantity": "\n1\n",
            },
            {
                "name": "Dovin's Veto",
                "cuantity": "\n2\n",
            },
            {
                "name": "Heartless Act",
                "cuantity": "\n1\n",
            },
            {
                "name": "Vanishing Verse",
                "cuantity": "\n2\n",
            },
            {
                "name": "Absorb",
                "cuantity": "\n3\n",
            },
            {
                "name": "Void Rend",
                "cuantity": "\n2\n",
            },
            {
                "name": "Memory Deluge",
                "cuantity": "\n4\n",
            },
            {
                "name": "Supreme Verdict",
                "cuantity": "\n3\n",
            },
        ],
        "Enchantments(8)": [
            {
                "name": "Omen of the Sea",
                "cuantity": "\n4\n",
            },
            {
                "name": "Oath of Kaya",
                "cuantity": "\n2\n",
            },
            {
                "name": "Shark Typhoon",
                "cuantity": "\n2\n",
            },
        ],
        "Lands(36)": [
            {
                "name": "Deserted Beach",
                "cuantity": "\n4\n",
            },
            {
                "name": "Drowned Catacomb",
                "cuantity": "\n2\n",
            },
            {
                "name": "Eiganjo, Seat of the Empire",
                "cuantity": "\n1\n",
            },
            {
                "name": "Fetid Pools",
                "cuantity": "\n3\n",
            },
            {
                "name": "Glacial Fortress",
                "cuantity": "\n4\n",
            },
            {
                "name": "Godless Shrine",
                "cuantity": "\n4\n",
            },
            {
                "name": "Hallowed Fountain",
                "cuantity": "\n2\n",
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
            },
            {
                "name": "Shambling Vent",
                "cuantity": "\n3\n",
            },
            {
                "name": "Shipwreck Marsh",
                "cuantity": "\n1\n",
            },
            {
                "name": "Watery Grave",
                "cuantity": "\n4\n",
            },
        ],
        "Sideboard(15) including Companion": [
            {
                "name": "Aether Gust",
                "cuantity": "\n4\n",
            },
            {
                "name": "Malevolent Hermit",
                "cuantity": "\n3\n",
            },
            {
                "name": "Graveyard Trespasser",
                "cuantity": "\n3\n",
            },
            {
                "name": "Kaya, Orzhov Usurper",
                "cuantity": "\n1\n",
            },
            {
                "name": "Mystical Dispute",
                "cuantity": "\n2\n",
            },
            {
                "name": "Narset, Parter of Veils",
                "cuantity": "\n1\n",
            },
        ],
    },
    "link": "https://www.mtggoldfish.com/archetype/pioneer-esper-control-8413f5ae-6d65-4826-992a-9c2e3511890d",
}

d1 = Deck(deck_1_raw)
d1.get_info()
d2 = Deck(deck_2_raw)
d2.get_info()
