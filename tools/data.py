# -*- coding: utf-8 -*-
"""
Historical data shared by the build scripts: start positions, city-state sites,
the cities each power holds in 1299 and the new city-states of the scenario.
Coordinates are (longitude, latitude).
"""

# ------------------------------------------------------------------ major civilizations
# Historic start positions for the map script, in priority order.
# Civilizations missing from a game are simply skipped.
MAJOR_STARTS = [
    ("CIVILIZATION_OB_OTTOMAN", 30.18, 40.02, "Sogut"),
    ("CIVILIZATION_BYZANTIUM", 28.70, 41.02, "Constantinople"),
    ("CIVILIZATION_MONGOL", 46.29, 38.08, "Tabriz (Ilkhanate)"),
    ("CIVILIZATION_EGYPT", 31.24, 30.04, "Cairo (Mamluks)"),
    ("CIVILIZATION_VENICE", 12.33, 45.44, "Venice"),
    ("CIVILIZATION_AUSTRIA", 16.37, 48.21, "Vienna"),
    ("CIVILIZATION_POLAND", 19.94, 50.06, "Krakow"),
    ("CIVILIZATION_MOROCCO", -4.98, 34.03, "Fez (Marinids)"),
    ("CIVILIZATION_OTTOMAN", 26.56, 41.67, "Edirne"),
    ("CIVILIZATION_ARABIA", 39.83, 21.42, "Mecca"),
    ("CIVILIZATION_PERSIA", 51.67, 32.65, "Isfahan"),
    ("CIVILIZATION_GREECE", 23.73, 37.98, "Athens"),
    ("CIVILIZATION_ROME", 12.50, 41.90, "Rome"),
    ("CIVILIZATION_HUNS", 19.00, 47.00, "Pannonia"),
    ("CIVILIZATION_FRANCE", 2.35, 48.85, "Paris"),
    ("CIVILIZATION_SPAIN", -3.70, 40.42, "Madrid"),
    ("CIVILIZATION_CARTHAGE", 10.32, 36.85, "Carthage"),
    ("CIVILIZATION_ASSYRIA", 43.15, 36.36, "Nineveh"),
    ("CIVILIZATION_BABYLON", 44.42, 32.54, "Babylon"),
    ("CIVILIZATION_ETHIOPIA", 38.72, 14.13, "Aksum"),
    ("CIVILIZATION_SONGHAI", -0.04, 16.27, "Gao"),
    ("CIVILIZATION_GERMANY", 13.40, 50.80, "Saxony (map edge)"),
    ("CIVILIZATION_RUSSIA", 37.60, 50.60, "Kursk (map edge)"),
    # Civilizations from the "Turkish Leaders" mod, if it is also active
    ("CIVILIZATION_TL_FATIH", 28.70, 41.02, "Istanbul"),
    ("CIVILIZATION_TL_ORHAN", 29.06, 40.18, "Bursa"),
    ("CIVILIZATION_TL_OSMAN", 30.18, 40.02, "Sogut"),
    ("CIVILIZATION_TL_BATTAL", 38.31, 38.35, "Malatya"),
    ("CIVILIZATION_TL_ATATURK", 32.86, 39.93, "Ankara"),
    ("CIVILIZATION_TL_YAVUZ", 35.83, 40.65, "Amasya"),
]

# ------------------------------------------------------------------ city-states
# Base-game city-states that have a home on this map.
BASE_MINOR_SITES = [
    ("MINOR_CIV_RAGUSA", 18.09, 42.65), ("MINOR_CIV_GENOA", 8.93, 44.41), ("MINOR_CIV_FLORENCE", 11.25, 43.77),
    ("MINOR_CIV_MILAN", 9.19, 45.46), ("MINOR_CIV_VATICAN_CITY", 12.45, 41.90), ("MINOR_CIV_BUDAPEST", 19.04, 47.50),
    ("MINOR_CIV_BELGRADE", 20.46, 44.82), ("MINOR_CIV_SOFIA", 23.32, 42.70), ("MINOR_CIV_PRAGUE", 14.42, 50.08),
    ("MINOR_CIV_KIEV", 30.52, 50.45), ("MINOR_CIV_ORMUS", 56.46, 27.10), ("MINOR_CIV_BRATISLAVA", 17.10, 48.15),
    ("MINOR_CIV_BUCHAREST", 26.10, 44.43), ("MINOR_CIV_JERUSALEM", 35.21, 31.77), ("MINOR_CIV_SIDON", 35.37, 33.56),
    ("MINOR_CIV_TYRE", 35.20, 33.27), ("MINOR_CIV_BYBLOS", 35.65, 34.12), ("MINOR_CIV_YEREVAN", 44.50, 40.18),
    ("MINOR_CIV_UR", 46.10, 30.96), ("MINOR_CIV_VALLETTA", 14.51, 35.90), ("MINOR_CIV_MONACO", 7.42, 43.74),
    ("MINOR_CIV_GENEVA", 6.14, 46.20), ("MINOR_CIV_ZURICH", 8.54, 47.37), ("MINOR_CIV_BRUSSELS", 4.35, 50.85),
    ("MINOR_CIV_ANTWERP", 4.40, 50.90), ("MINOR_CIV_WITTENBERG", 12.65, 50.90),
]

# Base city-states kept by the 1299 scenario; every other base city-state is removed there.
SCENARIO_KEEP_BASE_MINORS = ["MINOR_CIV_RAGUSA", "MINOR_CIV_GENOA", "MINOR_CIV_FLORENCE", "MINOR_CIV_VATICAN_CITY",
                             "MINOR_CIV_BUDAPEST", "MINOR_CIV_BELGRADE", "MINOR_CIV_PRAGUE", "MINOR_CIV_KIEV",
                             "MINOR_CIV_ORMUS"]

# New city-states of 1299.
# key: (name, adjective, trait, art style, lon, lat, color, [city names], civilopedia text)
STYLE_EURO = ("ARTSTYLE_EUROPEAN", "_EURO", "EUROPEAN ")
STYLE_MIDEAST = ("ARTSTYLE_MIDDLE_EAST", "_AFRI", "AFRICAN ")
STYLE_GRECO = ("ARTSTYLE_GRECO_ROMAN", "_MED", "MEDITERRANEAN ")

NEW_MINORS = {
    "KARAMAN": ("Karaman", "Karamanid", "MINOR_TRAIT_MILITARISTIC", STYLE_MIDEAST, 33.22, 37.18, "PLAYERCOLOR_MINOR_PEACH",
                ["Larende", "Ermenek", "Mut"],
                "The Karamanids were a Turkmen dynasty of south-central Anatolia, based at Larende (modern Karaman) "
                "and Ermenek. For two centuries they were the most persistent rivals of the Ottomans in Anatolia, "
                "and they held Konya for long periods. Their lands were finally annexed by the Ottomans in the "
                "second half of the 15th century."),
    "GERMIYAN": ("Germiyan", "Germiyanid", "MINOR_TRAIT_CULTURED", STYLE_MIDEAST, 29.45, 38.95, "PLAYERCOLOR_MINOR_LIGHT_PURPLE",
                 ["Kutahya", "Simav", "Usak"],
                 "The Germiyanids ruled a powerful frontier principality from Kutahya, the immediate neighbour of "
                 "Osman's small beylik. Their court was a centre of early Anatolian Turkish literature. Much of their "
                 "territory passed to the Ottomans through a marriage alliance in the late 14th century."),
    "KARESI": ("Karesi", "Karesid", "MINOR_TRAIT_MARITIME", STYLE_MIDEAST, 27.88, 39.65, "PLAYERCOLOR_MINOR_GOLDENROD",
               ["Balikesir", "Bergama", "Edremit"],
               "Karesi was a coastal principality around Balikesir facing the Dardanelles. Its seasoned sailors and "
               "soldiers joined the Ottomans after Orhan annexed the beylik in the 1340s, and they helped carry the "
               "Ottoman state across the straits into Europe."),
    "MENTESE": ("Mentese", "Mentese", "MINOR_TRAIT_MARITIME", STYLE_MIDEAST, 27.78, 37.32, "PLAYERCOLOR_MINOR_CYAN",
                ["Milas", "Becin", "Mugla"],
                "Mentese was a seafaring beylik in Caria in south-western Anatolia, with its seat at Milas and Becin. "
                "Its fleets raided the islands of the Aegean, bringing it into conflict with the Knights Hospitaller "
                "and Venice."),
    "CANDAR": ("Candar", "Candarid", "MINOR_TRAIT_MERCANTILE", STYLE_MIDEAST, 33.78, 41.38, "PLAYERCOLOR_MINOR_GREEN",
               ["Kastamonu", "Sinop", "Tosya"],
               "The Candarids, also called the Isfendiyarids, ruled Kastamonu and later the Black Sea port of Sinop. "
               "Among the longest-lived of the Anatolian beyliks, they survived until the reign of Mehmed II."),
    "TREBIZOND": ("Trebizond", "Trapezuntine", "MINOR_TRAIT_MERCANTILE", STYLE_GRECO, 39.72, 41.00, "PLAYERCOLOR_MINOR_YELLOW",
                  ["Trebizond", "Kerasous", "Oinaion"],
                  "The Empire of Trebizond was a Byzantine successor state on the Black Sea coast, ruled by the Grand "
                  "Komnenoi from 1204. Rich from the trade that passed from Tabriz to the sea, it outlived "
                  "Constantinople by eight years and fell to Mehmed II in 1461."),
    "GEORGIA": ("Georgia", "Georgian", "MINOR_TRAIT_RELIGIOUS", STYLE_EURO, 44.79, 41.72, "PLAYERCOLOR_MINOR_BLUE",
                ["Tbilisi", "Kutaisi", "Mtskheta"],
                "The medieval Kingdom of Georgia reached its golden age under Queen Tamar around 1200. By 1299 it was "
                "a vassal of the Ilkhanate, and its throne was contested between rival members of the Bagrationi "
                "dynasty."),
    "CILICIA": ("Cilicia", "Cilician", "MINOR_TRAIT_MERCANTILE", STYLE_EURO, 35.82, 37.45, "PLAYERCOLOR_MINOR_MIDDLE_PURPLE",
                ["Sis", "Tarsus", "Ayas"],
                "The Armenian Kingdom of Cilicia ruled the plain around Adana and the Taurus passes from its capital "
                "at Sis. Its port of Ayas was one of the great markets of the Levant. An ally of the Mongols, it was "
                "conquered by the Mamluks in 1375."),
    "CYPRUS": ("Cyprus", "Cypriot", "MINOR_TRAIT_MARITIME", STYLE_EURO, 33.36, 35.17, "PLAYERCOLOR_MINOR_CYAN",
               ["Nicosia", "Famagusta", "Limassol"],
               "After the fall of Acre in 1291 the Kingdom of Cyprus, ruled by the Lusignan dynasty, became the last "
               "outpost of the crusader states. Famagusta grew into one of the richest ports of the Mediterranean."),
    "EPIRUS": ("Epirus", "Epirote", "MINOR_TRAIT_MILITARISTIC", STYLE_GRECO, 20.99, 39.16, "PLAYERCOLOR_MINOR_MIDDLE_CYAN",
               ["Arta", "Ioannina", "Preveza"],
               "The Despotate of Epirus was a Greek state in the western Balkans founded after the Fourth Crusade. "
               "From its capital at Arta it competed with Nicaea, and later with the restored Byzantine Empire, for "
               "the legacy of Rome."),
    "ATHENS": ("Athens", "Athenian", "MINOR_TRAIT_CULTURED", STYLE_GRECO, 23.73, 37.98, "PLAYERCOLOR_MINOR_BLUE",
               ["Athens", "Thebes", "Livadeia"],
               "The Duchy of Athens was a crusader state founded in 1205 and ruled by the Burgundian de la Roche "
               "family and then the Brienne family. In 1311 it was seized by the mercenaries of the Catalan Company."),
    "GOLDEN_HORDE": ("Golden Horde", "Horde", "MINOR_TRAIT_MILITARISTIC", STYLE_MIDEAST, 47.40, 46.95,
                     "PLAYERCOLOR_MINOR_LIGHT_ORANGE", ["Sarai", "Azak", "Hajji Tarkhan"],
                     "The Golden Horde, or Ulus of Jochi, was the Mongol khanate of the western steppe. From its "
                     "capital Sarai on the lower Volga it collected tribute from the Russian principalities and "
                     "controlled the northern branch of the Silk Road."),
    "CAFFA": ("Caffa", "Genoese", "MINOR_TRAIT_MERCANTILE", STYLE_EURO, 35.38, 45.03, "PLAYERCOLOR_MINOR_LIGHT_BLUE",
              ["Caffa", "Soldaia", "Cembalo"],
              "Caffa was the Genoese trading colony in the Crimea, the hub of Genoa's Black Sea commerce in grain, "
              "furs and slaves. It remained in Genoese hands until the Ottomans took it in 1475."),
    "HAFSIDS": ("Tunis", "Hafsid", "MINOR_TRAIT_MERCANTILE", STYLE_MIDEAST, 10.17, 36.80, "PLAYERCOLOR_MINOR_GREEN",
                ["Tunis", "Bejaia", "Kairouan"],
                "The Hafsid dynasty ruled Ifriqiya from Tunis between 1229 and 1574. Tunis became the leading city of "
                "the Maghreb, until it was drawn into the struggle between the Ottomans and Habsburg Spain."),
    "ZAYYANIDS": ("Tlemcen", "Zayyanid", "MINOR_TRAIT_CULTURED", STYLE_MIDEAST, -1.32, 34.88, "PLAYERCOLOR_MINOR_MIDDLE_BLUE",
                  ["Tlemcen", "Oran", "Algiers"],
                  "The Zayyanid kingdom of Tlemcen controlled the central Maghreb and the trans-Saharan trade routes "
                  "that ended at its gates. In 1299 Tlemcen was enduring a long siege by the Marinids of Fez."),
    "RASULIDS": ("Yemen", "Rasulid", "MINOR_TRAIT_MERCANTILE", STYLE_MIDEAST, 44.02, 13.58, "PLAYERCOLOR_MINOR_LIGHT_YELLOW",
                 ["Ta'izz", "Zabid", "Aden"],
                 "The Rasulid sultans ruled Yemen from Ta'izz and Zabid between 1229 and 1454. Through the port of "
                 "Aden they controlled the spice trade between India and the Red Sea, and their court patronised "
                 "scholars, astronomers and agriculture."),
    "MECCA": ("Mecca", "Meccan", "MINOR_TRAIT_RELIGIOUS", STYLE_MIDEAST, 39.83, 21.42, "PLAYERCOLOR_MINOR_GREEN",
              ["Mecca", "Medina", "Jeddah"],
              "The Sharifs of Mecca were the guardians of the holy cities of Islam. In 1299 they ruled the Hejaz under "
              "the protection of the Mamluk sultans of Egypt; in 1517 that role passed to the Ottomans."),
    "SICILY": ("Sicily", "Sicilian", "MINOR_TRAIT_MARITIME", STYLE_EURO, 13.36, 38.12, "PLAYERCOLOR_MINOR_YELLOW",
               ["Palermo", "Messina", "Syracuse"],
               "After the Sicilian Vespers of 1282 the island of Sicily rejected Angevin rule and chose a king from the "
               "House of Aragon. In 1299 it was still at war with the Angevin Kingdom of Naples."),
    "NAPLES": ("Naples", "Neapolitan", "MINOR_TRAIT_CULTURED", STYLE_EURO, 14.25, 40.85, "PLAYERCOLOR_MINOR_WHITE",
               ["Naples", "Bari", "Taranto"],
               "The Angevin Kingdom of Naples ruled southern Italy after losing Sicily in 1282. Its kings also claimed "
               "lands across the Adriatic in Albania and Greece."),
    "MAKURIA": ("Makuria", "Makurian", "MINOR_TRAIT_RELIGIOUS", STYLE_MIDEAST, 30.48, 18.22, "PLAYERCOLOR_MINOR_DARK_LEMON",
                ["Dongola", "Faras", "Qasr Ibrim"],
                "Makuria was a Christian kingdom of Nubia on the middle Nile with its capital at Old Dongola. For six "
                "centuries it resisted its northern neighbours, but by 1299 it was weakened by Mamluk interventions."),
    "BULGARIA": ("Bulgaria", "Bulgarian", "MINOR_TRAIT_MILITARISTIC", STYLE_EURO, 25.63, 43.08, "PLAYERCOLOR_MINOR_LIGHT_GREEN",
                 ["Tarnovo", "Vidin", "Nikopol"],
                 "The Second Bulgarian Empire, with its capital at Tarnovo, was in 1299 recovering from Mongol "
                 "domination under Tsar Theodore Svetoslav. Tarnovo fell to the Ottomans in 1393."),
}

# ------------------------------------------------------------------ 1299 scenario
SCENARIO_MAJORS = [
    "CIVILIZATION_OB_OTTOMAN",
    "CIVILIZATION_BYZANTIUM",
    "CIVILIZATION_MONGOL",
    "CIVILIZATION_EGYPT",
    "CIVILIZATION_VENICE",
    "CIVILIZATION_AUSTRIA",
    "CIVILIZATION_POLAND",
    "CIVILIZATION_MOROCCO",
]

# What each base civilization stands for in 1299 (shown on the scenario screen)
SCENARIO_ROLES = {
    "CIVILIZATION_OB_OTTOMAN": "The Ottoman Beylik of Osman Bey, a small frontier principality at Sogut.",
    "CIVILIZATION_BYZANTIUM": "The Eastern Roman (Byzantine) Empire of Andronikos II Palaiologos.",
    "CIVILIZATION_MONGOL": "Represents the Ilkhanate, the Mongol khanate of Ghazan Khan ruling Persia and Iraq.",
    "CIVILIZATION_EGYPT": "Represents the Mamluk Sultanate of Egypt and Syria.",
    "CIVILIZATION_VENICE": "The Republic of Venice, mistress of the Adriatic and of Crete.",
    "CIVILIZATION_AUSTRIA": "Represents the Duchy of Austria under the Habsburg Albert I.",
    "CIVILIZATION_POLAND": "Represents the Kingdom of Poland during its reunification.",
    "CIVILIZATION_MOROCCO": "Represents the Marinid Sultanate of Fez.",
}

# Cities held in 1299: (name, lon, lat, population). The first city is the capital.
SCENARIO_CITIES = {
    "CIVILIZATION_BYZANTIUM": [("Constantinople", 28.70, 41.02, 8), ("Thessalonica", 22.94, 40.64, 5),
                               ("Adrianople", 26.56, 41.67, 4), ("Philadelphia", 28.52, 38.35, 3),
                               ("Mistra", 22.37, 37.07, 3)],
    "CIVILIZATION_MONGOL": [("Tabriz", 46.29, 38.08, 8), ("Baghdad", 44.36, 33.31, 6), ("Sultaniyya", 48.79, 36.43, 4),
                            ("Mosul", 43.13, 36.34, 4), ("Erzurum", 41.27, 39.90, 3), ("Sivas", 37.02, 39.75, 4),
                            ("Isfahan", 51.67, 32.65, 5)],
    "CIVILIZATION_EGYPT": [("Cairo", 31.24, 30.04, 9), ("Alexandria", 29.92, 31.20, 5), ("Damascus", 36.29, 33.51, 6),
                           ("Aleppo", 37.16, 36.20, 5), ("Jerusalem", 35.21, 31.77, 3), ("Qus", 32.76, 25.91, 3)],
    "CIVILIZATION_VENICE": [("Venice", 12.33, 45.44, 6), ("Candia", 25.13, 35.34, 3), ("Zara", 15.23, 44.12, 2)],
    "CIVILIZATION_AUSTRIA": [("Vienna", 16.37, 48.21, 5), ("Graz", 15.30, 46.70, 3)],
    "CIVILIZATION_POLAND": [("Krakow", 19.94, 50.06, 4)],
    "CIVILIZATION_MOROCCO": [("Fez", -4.98, 34.03, 6), ("Tangier", -5.80, 35.77, 3), ("Sijilmasa", -4.27, 31.30, 2)],
}
