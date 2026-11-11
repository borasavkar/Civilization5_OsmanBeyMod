# -*- coding: utf-8 -*-
"""All in-game text (English). Turkish letters the Civ V font cannot draw are converted at build time."""

TEXT = {}


def t(tag, text):
    TEXT[tag] = text


# ======================================================================
# Civilization and leader
# ======================================================================
t("TXT_KEY_CIV_OB_OTTOMAN_DESC", "Ottoman Beylik")
t("TXT_KEY_CIV_OB_OTTOMAN_SHORT_DESC", "Ottoman Beylik")
t("TXT_KEY_CIV_OB_OTTOMAN_ADJECTIVE", "Ottoman")
t("TXT_KEY_LEADER_OB_OSMAN", "Osman Bey")
t("TXT_KEY_LEADER_OB_OSMAN_PEDIA", "Osman Bey")

t("TXT_KEY_TRAIT_OB_OSMAN_SHORT", "Osman's Dream")
t("TXT_KEY_TRAIT_OB_OSMAN",
  "Captured cities have no [ICON_RESISTANCE] Resistance and grant [ICON_GOLD] Gold equal to 10 times their "
  "population. Great Generals are earned 50% faster.")

t("TXT_KEY_CIV5_DAWN_OB_OTTOMAN_TEXT",
  "Hail, Osman Bey, son of Ertugrul! On the uneasy frontier between the fading Sultanate of the Seljuks and the "
  "walls of the Eastern Roman Empire, your tribe has made its home in the green valley of Sögüt. One night, as a "
  "guest in the house of Sheikh Edebali, you dreamt that a great tree grew from your breast, and that its branches "
  "shaded mountains, rivers and cities from one horizon to the other. The sheikh read the dream as a promise: your "
  "house would rule the world it shaded.[NEWLINE][NEWLINE]It is the year 1299. Bursa and Nicaea still answer to "
  "Constantinople, the Mongol Ilkhans claim the east of Anatolia, and rival beyliks watch your every move. Gather "
  "your gazis, Osman Bey. Can you turn a frontier principality into an empire that stretches from Vienna to Arabia?")

t("TXT_KEY_CIVILOPEDIA_LEADERS_OB_OSMAN_NAME", "Osman Bey")
t("TXT_KEY_CIVILOPEDIA_LEADERS_OB_OSMAN_SUBTITLE", "Founder of the Ottoman State")
t("TXT_KEY_CIVILOPEDIA_LEADERS_OB_OSMAN_LIVED", "c. 1258 - 1323/24")
t("TXT_KEY_CIVILOPEDIA_LEADERS_OB_OSMAN_TITLES_1", "Osman Gazi")
t("TXT_KEY_CIVILOPEDIA_LEADERS_OB_OSMAN_TITLES_2", "Bey of Sögüt")
t("TXT_KEY_CIVILOPEDIA_LEADERS_OB_OSMAN_HEADING_1", "The Frontier Bey")
t("TXT_KEY_CIVILOPEDIA_LEADERS_OB_OSMAN_TEXT_1",
  "Osman, the son of Ertugrul, led a small Turkmen community settled around Sögüt in north-western Anatolia, on "
  "the border between the declining Seljuk Sultanate of Rum and the Byzantine province of Bithynia. Very little "
  "about his early life can be stated with certainty: the earliest surviving Ottoman chronicles were written more "
  "than a century after his death, and they mix history with legend. What is clear is that Osman and his warriors "
  "steadily took Byzantine forts and towns such as Karacahisar, Bilecik and Yenisehir, and that in 1302 he defeated "
  "a Byzantine army at Bapheus near Nicomedia, a victory that made his name known far beyond the frontier.")
t("TXT_KEY_CIVILOPEDIA_LEADERS_OB_OSMAN_HEADING_2", "The Dream")
t("TXT_KEY_CIVILOPEDIA_LEADERS_OB_OSMAN_TEXT_2",
  "According to Ottoman tradition, Osman dreamt in the house of Sheikh Edebali that a moon rose from the sheikh's "
  "breast and sank into his own, and that a tree then grew from his body whose branches covered the world. Edebali "
  "interpreted the dream as a sign that Osman's descendants would rule, and gave him his daughter in marriage. "
  "Whether or not it was ever dreamt, the story became the founding legend of the dynasty that took its name from "
  "Osman.")
t("TXT_KEY_CIVILOPEDIA_LEADERS_OB_OSMAN_HEADING_3", "Legacy")
t("TXT_KEY_CIVILOPEDIA_LEADERS_OB_OSMAN_TEXT_3",
  "Osman died around 1323 or 1324. Shortly afterwards his son Orhan took Bursa, which became the first real capital "
  "of the state and the place where Osman was buried. The beylik he founded grew into the Ottoman Empire, which "
  "lasted until 1922. The Turkish name of the dynasty and the state, Osmanli, and its European form, Ottoman, both "
  "come from his name.")

t("TXT_KEY_CIV5_OB_OTTOMAN_TEXT_1",
  "The Ottoman Beylik was one of many small Turkmen principalities that emerged in Anatolia as the Seljuk Sultanate "
  "of Rum broke apart under Mongol overlordship at the end of the 13th century. Its position was unusual: it lay "
  "directly on the Byzantine frontier in Bithynia, within reach of the rich cities of Bursa, Nicaea and Nicomedia "
  "and of the straits leading to Europe. Frontier warriors, dervishes and settlers were drawn to it, and the beylik "
  "grew quickly by conquest and by winning over the local population.")
t("TXT_KEY_CIVILOPEDIA_CIVS_OB_OTTOMAN_HEADING_1", "From Beylik to Empire")
t("TXT_KEY_CIVILOPEDIA_CIVS_OB_OTTOMAN_TEXT_1", TEXT["TXT_KEY_CIV5_OB_OTTOMAN_TEXT_1"])
t("TXT_KEY_CIVILOPEDIA_CIVS_OB_OTTOMAN_HEADING_2", "Istimalet")
t("TXT_KEY_CIVILOPEDIA_CIVS_OB_OTTOMAN_TEXT_2",
  "Historians use the Ottoman term istimalet, 'winning over', for the early Ottoman practice of treating conquered "
  "communities leniently. Towns that surrendered usually kept their property, their religion and often their local "
  "leaders, and many Byzantine soldiers and notables entered Ottoman service. Köse Mihal, a Byzantine lord who became "
  "one of Osman's companions, is the best-known example.")
t("TXT_KEY_CIVILOPEDIA_CIVS_OB_OTTOMAN_FACTOID_HEADING", "Did you know?")
t("TXT_KEY_CIVILOPEDIA_CIVS_OB_OTTOMAN_FACTOID_TEXT",
  "The Ottoman dynasty ruled without interruption for more than 600 years, from Osman to the last sultan, "
  "Mehmed VI, who left Istanbul in 1922.")

# ======================================================================
# Unique units
# ======================================================================
UNITS = {
    "AKINCI": ("Akinji",
               "Replaces the Knight. Does not require [ICON_RES_HORSE] Horses, costs less, has +1 sight and can "
               "pillage without spending movement, healing when it does.",
               "The Akinji is a raider. Use its speed and free pillaging to strip enemy improvements, cut trade routes "
               "and catch exposed workers and settlers. Like the Knight it is weak against cities; leave sieges to the "
               "infantry and artillery.",
               "Akinjis (Turkish: akinci, 'raiders') were the light cavalry of the Ottoman frontier. Unpaid volunteers who lived on the spoils of "
               "their raids, they rode far ahead of the main army to spread fear, gather intelligence and weaken the "
               "enemy before a campaign. Their commanders came from a few hereditary families, such as the "
               "Mihaloglu and the Evrenosoglu."),
    "YENICERI": ("Janissary (Yeniceri)",
                 "Replaces the Musketman. Stronger than the Musketman, heals after destroying an enemy, fights with an "
                 "attack bonus and starts with the Drill I promotion.",
                 "Janissaries are elite gunpowder infantry. Use them to lead assaults: each victory heals them, so a "
                 "line of Janissaries can push through an enemy army without stopping to rest.",
                 "The Janissaries (Yeniceri, 'new soldiers') were the standing infantry of the Ottoman sultans, formed "
                 "in the 14th century. They were paid salaries, lived in barracks, wore uniforms and drilled "
                 "together, which made them one of the first permanent professional armies in Europe. By the 16th "
                 "century they were famous for their discipline and their firearms."),
}

BUILDINGS = {
    "KERVANSARAY": ("Kervansaray",
                    "Replaces the Caravansary. Provides +2 [ICON_GOLD] Gold and +1 [ICON_CULTURE] Culture in "
                    "addition to the Caravansary's trade route bonuses.",
                    "Build the Kervansaray in cities on your caravan routes. Its extra Gold and Culture make it "
                    "worthwhile even before the trade routes it improves are established.",
                    "Caravanserais were fortified roadside inns where merchants, travellers and their animals could "
                    "rest safely. The Seljuks and the Ottomans built them a day's journey apart along the great roads "
                    "of Anatolia, often as charitable foundations, binding the empire together through trade."),
    "MEDRESE": ("Medrese",
                "Replaces the University. Provides +1 [ICON_CULTURE] Culture and +1 [ICON_PEACE] Faith in addition to "
                "the University's [ICON_RESEARCH] Science.",
                "The Medrese advances science, culture and faith at the same time. Build it in your largest cities.",
                "Medreses were colleges of law, theology and the sciences. Orhan founded the first Ottoman medrese at "
                "Iznik in 1331; later the great mosque complexes of Istanbul each had their own colleges, which "
                "trained the judges, teachers and administrators of the empire."),
    "TOPHANE": ("Tophane",
                "Replaces the Armory. Provides +1 [ICON_PRODUCTION] Production and +15% [ICON_PRODUCTION] Production "
                "when building Gunpowder and Siege units, in addition to the Armory's experience bonus.",
                "The Tophane turns a military city into an arsenal. Combine it with the Janissary to field veteran "
                "armies quickly.",
                "The Tophane-i Amire, the imperial cannon foundry, was established in Istanbul after the conquest of "
                "1453. Ottoman gunners were among the best in Europe and Asia, and the foundry cast the guns that "
                "armed the sultans' armies and fortresses for centuries."),
}
for tag, (name, helptext, strat, pedia) in UNITS.items():
    t("TXT_KEY_UNIT_OB_%s" % tag, name)
    t("TXT_KEY_UNIT_HELP_OB_%s" % tag, helptext)
    t("TXT_KEY_UNIT_OB_%s_STRATEGY" % tag, strat)
    t("TXT_KEY_CIV5_UNIT_OB_%s_TEXT" % tag, pedia)
for tag, (name, helptext, strat, pedia) in BUILDINGS.items():
    t("TXT_KEY_BUILDING_OB_%s" % tag, name)
    t("TXT_KEY_BUILDING_OB_%s_HELP" % tag, helptext)
    t("TXT_KEY_BUILDING_OB_%s_STRATEGY" % tag, strat)
    t("TXT_KEY_BUILDING_OB_%s_PEDIA" % tag, pedia)

t("TXT_KEY_PROMOTION_OB_AKINCI_RAID", "Akinji Raider")
t("TXT_KEY_PROMOTION_OB_AKINCI_RAID_HELP", "+1 sight. Pillaging costs no movement and heals the unit.")

t("TXT_KEY_OB_ISTIMALET", "Istimalet: [ICON_RESISTANCE] Resistance in {1_City} has ended and the treasury receives {2_Num} [ICON_GOLD] Gold.")
t("TXT_KEY_OB_ISTIMALET_SHORT", "City won over")

# ======================================================================
# Diplomacy
# ======================================================================
DIPLO = {
    "FIRSTGREETING": "Peace be upon you, stranger. I am Osman, son of Ertugrul, bey of Sögüt. My tent is open to "
                     "friends, and my sword is ready for those who are not.",
    "DEFEATED": "The tree has fallen before its time... but its seed is in the earth. Others of my house will rise.",
    "DOW_GENERIC": "The frontier calls my gazis. Your lands will be ours.",
    "ATTACKED_HOSTILE": "You have chosen war with the house of Osman. You will regret it.",
    "GREETING_HOSTILE_HELLO": "What do you want? Speak quickly.",
    "GREETING_NEUTRAL_HELLO": "Welcome. What brings you to Sögüt?",
    "GREETING_POLITE_HELLO": "Welcome, friend. Sit, and let us talk as neighbours should.",
    "LETS_HEAR_IT": "Let me hear your proposal.",
    "REQUEST": "A small favour, between neighbours. Will you grant it?",
    "WINWAR": "Your walls were strong, but the will of my gazis was stronger.",
    "WORK_WITH_US": "A wise ruler knows the value of friends on his borders. Let us stand together.",
    "WORK_AGAINST_SOMEONE": "This one has troubled us both. Shall we answer him together?",
}
RESPONSE_TYPES = {
    "FIRSTGREETING": "RESPONSE_FIRST_GREETING",
    "DEFEATED": "RESPONSE_DEFEATED",
    "DOW_GENERIC": "RESPONSE_DOW_GENERIC",
    "ATTACKED_HOSTILE": "RESPONSE_ATTACKED_HOSTILE",
    "GREETING_HOSTILE_HELLO": "RESPONSE_GREETING_HOSTILE_HELLO",
    "GREETING_NEUTRAL_HELLO": "RESPONSE_GREETING_NEUTRAL_HELLO",
    "GREETING_POLITE_HELLO": "RESPONSE_GREETING_POLITE_HELLO",
    "LETS_HEAR_IT": "RESPONSE_LETS_HEAR_IT",
    "REQUEST": "RESPONSE_REQUEST",
    "WINWAR": "RESPONSE_WINWAR",
    "WORK_WITH_US": "RESPONSE_WORK_WITH_US",
    "WORK_AGAINST_SOMEONE": "RESPONSE_WORK_AGAINST_SOMEONE",
}
for key, line in DIPLO.items():
    t("TXT_KEY_LEADER_OB_OSMAN_%s_1" % key, line)

# ======================================================================
# Names
# ======================================================================
CITIES = ["Söğüt", "Bursa", "İznik", "Yenişehir", "Bilecik", "İnegöl", "Eskişehir", "Karacahisar", "İzmit",
          "Gemlik", "Mudanya", "Gelibolu", "Edirne", "Filibe", "Üsküdar", "Ankara", "Kütahya", "Bergama",
          "Balıkesir", "Manisa", "Selanik", "Sofya", "Üsküp", "Tırnova", "Amasya", "Tokat", "Sinop", "Trabzon",
          "Konya", "Kayseri", "Antalya", "Halep", "Şam", "Kahire", "Bağdat", "Belgrad", "Budin", "İstanbul"]
SPIES = ["Turgut Alp", "Samsa Çavuş", "Konur Alp", "Akçakoca", "Abdurrahman Gazi", "Gündüz Alp", "Aykut Alp",
         "Köse Mihal", "Hasan Alp", "Saltuk Alp"]

# ======================================================================
# Map script
# ======================================================================
t("TXT_KEY_OB_MAP_NAME", "Ottoman Frontiers (1299)")
t("TXT_KEY_OB_MAP_HELP",
  "Real geography from Vienna to Yemen and from Morocco to the Caspian Sea, with the rivers of the region. "
  "Anatolia and the Balkans are slightly enlarged so that the Ottoman heartland has room for cities. "
  "Recommended size: Huge.")
t("TXT_KEY_OB_MAP_OPTION_START", "Start Positions")
t("TXT_KEY_OB_MAP_OPTION_START_HISTORIC", "Historical")
t("TXT_KEY_OB_MAP_OPTION_START_RANDOM", "Balanced (random)")

# ======================================================================
# 1299 scenario
# ======================================================================
SCENARIO = {}


def s(tag, text):
    SCENARIO[tag] = text


s("TXT_KEY_OB1299_TITLE", "Rise of the Ottomans: 1299")
s("TXT_KEY_OB1299_DESC",
  "Anatolia, 1299. Lead Osman Bey's frontier principality, or any of the great powers of the age, on a real map "
  "that stretches from Vienna to Arabia.")
s("TXT_KEY_OB1299_INTRO",
  "It is the year 1299. The Seljuk Sultanate of Rum has crumbled under Mongol rule, and a patchwork of Turkmen "
  "beyliks now covers Anatolia. In the north-west, on the very border of the Eastern Roman Empire, Osman Bey rules a "
  "small principality around Sögüt.[NEWLINE][NEWLINE]Constantinople is still the greatest city of the "
  "Christian world, though its empire has shrunk to a few provinces. The Ilkhans rule Persia and Iraq from Tabriz, "
  "the Mamluk sultans hold Egypt, Syria and the holy cities, and Venice commands the sea. Beyond the Danube, Hungary, "
  "Austria and Poland are rising.[NEWLINE][NEWLINE]The great powers begin with the cities they held in 1299. The "
  "Ottoman Beylik begins with a single settler near Bursa. History is yours to write.")
s("TXT_KEY_OB1299_CHOOSE_CIV", "Choose your civilization")
s("TXT_KEY_OB1299_DIFFICULTY", "Difficulty: {1_Name}")
s("TXT_KEY_OB1299_START", "Start Scenario")
s("TXT_KEY_OB1299_SCENARIO_NOTE",
  "Cities of 1299 are placed at the start of the game. City-states are the beyliks and kingdoms of 1299.")
for tag, role in __import__("data").SCENARIO_ROLES.items():
    s("TXT_KEY_OB1299_ROLE_" + tag.replace("CIVILIZATION_", ""), role)

for key, (name, adj, trait, style, lon, lat, color, cities, pedia) in __import__("data").NEW_MINORS.items():
    s("TXT_KEY_CITYSTATE_OB_%s" % key, name)
    s("TXT_KEY_CITYSTATE_OB_%s_ADJ" % key, adj)
    s("TXT_KEY_CIV5_OB_%s_TEXT" % key, pedia)
    for i, c in enumerate(cities):
        s("TXT_KEY_CITYSTATE_OB_%s_CITY_%d" % (key, i + 1), c)
