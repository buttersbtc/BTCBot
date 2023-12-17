CURRENCY_FORMAT_DICT = {
    "default": "${:,.2f} ",
    "gbp": "£{:,.2f} British Pounds",
    "eur": "€{:,.2f} Euros",
    "brl": "R${:,.2f} Brazillian Reais",
    "vef": "B${:,.0f} Venezuelan Bolívar",
    "jpy": "¥{:,.0f} Japanese Yen",
    "cny": "¥{:,.0f} Chinese Renminbi",
    "ils": "₪{:,.0f} Israeli Shekalim",
    "inr": "₹{:,.2f} Indian Rupees",
    "zar": "R{:,.2f} South African Rands",
    "rub": "₽{:,.2f} Russian Rubles",
    "xau": "{:,.2f} ounces of gold",
    "xag": "{:,.2f} ounces of silver",
	"btc": "{:,.0f} Bitcoin"
}

ITEM_DICT = {
    "mac": {"cost": 5.71, "name": "Big Macs", "emoji": ":hamburger:", "single": False},
    "mcr": {"cost": 4.29, "name": "McRibs", "emoji": ":pig2:", "single": False},
    "cru": {
        "cost": 2.99,
        "name": "Crunchwraps Supreme",
        "emoji": ":taco:",
        "single": False,
    },
    "beer": {"cost": 4.75, "name": "Pints of Beer", "emoji": ":beer:", "single": False},
    "but": {
        "cost": 0.75,
        "name": "Sticks of Butter",
        "emoji": ":butter:",
        "single": False,
    },
    "coldcards": {
        "cost": 119.27,
        "name": "Coldcards",
        "emoji": ":pager:",
        "single": False,
    },
    "egg": {"cost": 0.1208333, "name": "Large Eggs", "emoji": ":egg:", "single": False},
    "420": {
        "cost": 200,
        "name": "Ounces of Marijuana",
        "emoji": ":maple_leaf:",
        "single": False,
    },
    "gum": {
        "cost": 8.37,
        "name": "Kilograms of Gummie Bears",
        "emoji": ":teddy_bear:",
        "single": False,
    },
    "rbx": {"cost": 0.0125, "name": "Robux", "emoji": ":bricks:", "single": False},
    "thc": {
        "cost": 40,
        "name": "THC distillate cartridges (1 gram)",
        "emoji": ":maple_leaf:",
        "single": False,
    },
    "pod": {"cost": 5.2475, "name": "JUUL pods", "emoji": ":smoking:", "single": False},
    "furby": {"cost": 300, "name": "Rare Furbies", "emoji": ":owl:", "single": False},
    "avo": {
        "cost": 10,
        "name": "Serves of Avocado Toast",
        "emoji": ":avocado:",
        "single": False,
    },
    "chicken": {
        "cost": 2.85,
        "name": "Rhode Island Red Chickens",
        "emoji": ":chicken:",
        "single": False,
    },
    "nana": {"cost": 0.23, "name": "Bananas", "emoji": ":banana:", "single": False},
    "bre": {
        "cost": 2.04,
        "name": "Loaves of bread",
        "emoji": ":bread:",
        "single": False,
    },
    # Seperating out items that should be displayed as cost for a single item
    "lam": {
        "cost": 521465,
        "name": "Lamborghini Aventador SVJ",
        "emoji": ":race_car:",
        "single": True,
    },
    "act": {
        "cost": 32410,
        "name": "Average College Tuition (4 years)",
        "emoji": ":student:",
        "single": True,
    },
    "lar": {
        "cost": 259000,
        "name": "McLaren 600LT 2020",
        "emoji": ":race_car:",
        "single": True,
    },
    "tm3": {
        "cost": 36990,
        "name": "Tesla Model 3",
        "emoji": ":red_car:",
        "single": True,
    },
    "rds": {
        "cost": 200000,
        "name": "Tesla Roadster 2020",
        "emoji": ":race_car:",
        "single": True,
    },
    "f40": {
        "cost": 1350000,
        "name": "Ferrari F40",
        "emoji": ":race_car:",
        "single": True,
    },
    "tay": {
        "cost": 232904,
        "name": "Porche Taycan Turbo S",
        "emoji": ":red_car:",
        "single": True,
    },
    "mus": {
        "cost": 75000,
        "name": "Ford Mustang Shelby GT500 2020",
        "emoji": ":blue_car:",
        "single": True,
    },
    "fc9": {
        "cost": 62000000,
        "name": "SpaceX Falcon 9 Launch",
        "emoji": ":rocket:",
        "single": True,
    },
    "trn": {
        "cost": 139900,
        "name": "Audi RS e-tron GT 2022",
        "emoji": ":race_car:",
        "single": True,
    },
    "bug": {
        "cost": 2990000,
        "name": "Bugatti Chiron 2020",
        "emoji": ":race_car:",
        "single": True,
    },
    "nev": {
        "cost": 2440000,
        "name": "Rimac Nevera",
        "emoji": ":race_car:",
        "single": True,
    },
    "gef": {
        "cost": 1499,
        "name": "Nvidia GEFORCE RTX 3090",
        "emoji": ":desktop_computer:",
        "single": True,
    },
    "rov": {
        "cost": 2725000000,
        "name": "trip to Mars + rover/drone/skycrane package",
        "emoji": ":robot: :rocket:",
        "single": True,
    },
    "bez": {
        "cost": 74598,
        "name": "One minute of Jeff Bezos' time",
        "emoji": ":man_office_worker:",
        "single": True,
    },
    "kid": {
        "cost": 200000,
        "name": "black market kidney",
        "emoji": ":detective: :aubergine:",
        "single": True,
    },
    "ukb": {
        "cost": 850000000000,
        "name": "British banking bailout",
        "emoji": ":flag_gb: :bank:",
        "single": True,
    },
}

BLACKLIST = {"xdg": True, "ltc": True, "eth": True, "xrp": True, "bch": True}

BITCOIN_IN_SATS = 100000000
