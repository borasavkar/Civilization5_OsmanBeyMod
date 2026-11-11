#!/usr/bin/env python3
"""
Loads the real Civilization V: Brave New World gameplay XML into SQLite, then applies both mods in
.modinfo order and checks the results. Catches SQL errors, missing columns and broken references
without starting the game. Database.log in the game stays the final judge.

Usage: python tools/test_sql.py ["<Civ V install folder>"]
"""
import glob
import os
import sqlite3
import sys
import xml.etree.ElementTree as ET

TOOLS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(TOOLS)
GAME = sys.argv[1] if len(sys.argv) > 1 else r"D:\SteamLibrary\steamapps\common\Sid Meier's Civilization V"
ASSETS = os.path.join(GAME, "Assets")
SOURCES = [os.path.join(ASSETS, "Sounds", "XML"), os.path.join(ASSETS, "Gameplay", "XML"), os.path.join(ASSETS, "DLC", "Expansion", "Gameplay", "XML"),
           os.path.join(ASSETS, "DLC", "Expansion2", "Gameplay", "XML")]
SKIP_DIRS = ("Text", "AI", "WorldBuilder")


def xml_files(folder):
    for f in glob.glob(os.path.join(folder, "**", "*.xml"), recursive=True):
        rel = os.path.relpath(f, folder)
        if not rel.split(os.sep)[0] in SKIP_DIRS:
            yield f


def parse(path):
    try:
        return ET.parse(path).getroot()
    except ET.ParseError:
        return None


def build_game_db():
    db = sqlite3.connect(":memory:")
    defined = {}           # table -> source index
    rows = {}              # table -> list of (source index, row dict)
    for si, src in enumerate(SOURCES):
        for f in xml_files(src):
            root = parse(f)
            if root is None or root.tag != "GameData":
                continue
            for el in root:
                if el.tag == "Table":
                    name = el.get("name")
                    cols = []
                    for c in el.findall("Column"):
                        spec = '"%s" %s' % (c.get("name"), (c.get("type") or "text").upper())
                        if c.get("primarykey") == "true":
                            spec += " PRIMARY KEY"
                        if c.get("autoincrement") == "true":
                            spec += " AUTOINCREMENT"
                        if c.get("unique") == "true" and c.get("primarykey") != "true":
                            spec += " UNIQUE"
                        if c.get("default") is not None and c.get("default") != "NULL":
                            d = c.get("default")
                            spec += " DEFAULT %s" % ({"true": "1", "false": "0"}.get(d, "'%s'" % d.replace("'", "''")))
                        cols.append(spec)
                    if cols:
                        defined[name] = (si, cols)
                else:
                    for r in el.findall("Row"):
                        row = dict(r.attrib)
                        for c in r:
                            row[c.tag] = c.text
                        rows.setdefault(el.tag, []).append((si, row))
    for name, (si, cols) in defined.items():
        db.execute('CREATE TABLE "%s" (%s)' % (name, ", ".join(cols)))
    for name, lst in rows.items():
        if name not in defined:
            continue
        top = max(si for si, _ in lst)
        # Expansion2 files are complete copies: use rows from the newest source that has any.
        for si, row in lst:
            if si != top and name in ("Units", "Buildings", "Civilizations", "MinorCivilizations", "UnitPromotions",
                                      "Unit_FreePromotions", "Unit_ResourceQuantityRequirements", "Building_YieldChanges"):
                continue
            insert(db, name, row, ignore=True)
    db.execute("CREATE TABLE Language_en_US (Tag TEXT UNIQUE, Text TEXT)")
    # Audio tables are built into the game engine (not defined in XML); these are their documented columns.
    db.execute("CREATE TABLE Audio_Sounds (SoundID TEXT UNIQUE, Filename TEXT, LoadType TEXT, bDontCache BOOLEAN, "
               "bOnlyLoadOneVariationEachTime BOOLEAN, DontTriggerDuplicates BOOLEAN)")
    db.execute("CREATE TABLE Audio_2DSounds (ScriptID TEXT UNIQUE, SoundID TEXT, SoundType TEXT, MinVolume INTEGER, "
               "MaxVolume INTEGER, IsMusic BOOLEAN, Looping BOOLEAN, MinTimeMustNotPlayAgain INTEGER, "
               "MaxTimeMustNotPlayAgain INTEGER, MinTimeDelay INTEGER, MaxTimeDelay INTEGER, StartFromRandomPosition BOOLEAN, "
               "OnlyTriggerOnUnitRuns BOOLEAN, DontPlay BOOLEAN, DontTriggerDuplicates BOOLEAN, Priority INTEGER)")
    return db


def to_sql(v):
    if v is None:
        return None
    return {"true": 1, "false": 0}.get(v, v)


_COLS = {}


def insert(db, table, row, ignore=False):
    if ignore:
        if table not in _COLS:
            _COLS[table] = {r[1] for r in db.execute('PRAGMA table_info("%s")' % table)}
        row = {k: v for k, v in row.items() if k in _COLS[table]}
        if not row:
            return
    cols = list(row)
    sql = 'INSERT %s INTO "%s" (%s) VALUES (%s)' % ("OR IGNORE" if ignore else "", table,
                                                    ", ".join('"%s"' % c for c in cols), ", ".join("?" * len(cols)))
    db.execute(sql, [to_sql(row[c]) for c in cols])


def apply_xml(db, path):
    root = ET.parse(path).getroot()
    for el in root:
        for r in el.findall("Row"):
            row = dict(r.attrib)
            for c in r:
                row[c.tag] = c.text
            insert(db, el.tag, row)


def apply_mod(db, folder):
    modinfo = glob.glob(os.path.join(folder, "*.modinfo"))[0]
    root = ET.parse(modinfo).getroot()
    for u in root.iter("UpdateDatabase"):
        path = os.path.join(folder, u.text)
        if path.endswith(".sql"):
            db.executescript(open(path, encoding="utf-8").read())
        else:
            apply_xml(db, path)
        print("  applied", u.text)


def one(db, sql, *args):
    r = db.execute(sql, args).fetchone()
    return r[0] if r else None


def main():
    failures = []

    def check(cond, msg):
        print(("  ok   " if cond else "  FAIL ") + msg)
        if not cond:
            failures.append(msg)

    db = build_game_db()
    print("game database loaded:", one(db, "SELECT COUNT(*) FROM Units"), "units,",
          one(db, "SELECT COUNT(*) FROM MinorCivilizations"), "city-states")
    print("Osman Bey:")
    apply_mod(db, os.path.join(ROOT, "Osman Bey"))
    check(one(db, "SELECT Class FROM Units WHERE Type='UNIT_OB_AKINCI'") == "UNITCLASS_KNIGHT", "Akinci replaces Knight")
    check(one(db, "SELECT COUNT(*) FROM Unit_ResourceQuantityRequirements WHERE UnitType='UNIT_OB_AKINCI'") == 0,
          "Akinci needs no Horses")
    check(one(db, "SELECT Cost FROM Units WHERE Type='UNIT_OB_AKINCI'") < one(db, "SELECT Cost FROM Units WHERE Type='UNIT_KNIGHT'"),
          "Akinci is cheaper than the Knight")
    check(one(db, "SELECT UnitArtInfo FROM Units WHERE Type='UNIT_OB_AKINCI'") == "ART_DEF_UNIT_U_OTTOMAN_SIPAHI",
          "Akinji uses the Sipahi model")
    check(one(db, "SELECT Text FROM Language_en_US WHERE Tag='TXT_KEY_UNIT_OB_AKINCI'") == "Akinji", "unit is named Akinji")
    check(one(db, "SELECT Class FROM Units WHERE Type='UNIT_OB_YENICERI'") == "UNITCLASS_MUSKETMAN", "Janissary replaces Musketman")
    check(one(db, "SELECT Combat FROM Units WHERE Type='UNIT_OB_YENICERI'") == 28, "Janissary strength 28")
    check(one(db, "SELECT COUNT(*) FROM Unit_FreePromotions WHERE UnitType='UNIT_OB_YENICERI'") >= 3,
          "Janissary promotions copied plus Drill I")
    check(one(db, "SELECT COUNT(*) FROM Unit_FreePromotions WHERE UnitType='UNIT_OB_AKINCI' AND PromotionType='PROMOTION_OB_AKINCI_RAID'") == 1,
          "Akinci raider promotion")
    check(one(db, "SELECT COUNT(*) FROM Civilization_UnitClassOverrides WHERE CivilizationType='CIVILIZATION_OB_OTTOMAN'") == 3,
          "three unit overrides")
    check(one(db, "SELECT COUNT(*) FROM Civilization_BuildingClassOverrides WHERE CivilizationType='CIVILIZATION_OB_OTTOMAN'") == 5,
          "five building overrides")
    check(one(db, "SELECT Combat FROM Units WHERE Type='UNIT_OB_AKINCI'") == 24 and
          one(db, "SELECT Moves FROM Units WHERE Type='UNIT_OB_AKINCI'") == 5, "Akinji 24 strength, 5 moves")
    check(one(db, "SELECT Class||'|'||PrereqTech||'|'||RangedCombat||'|'||UnitArtInfo FROM Units WHERE Type='UNIT_OB_SAHI'")
          == "UNITCLASS_TREBUCHET|TECH_MATHEMATICS|24|ART_DEF_UNIT_CANNON", "Great Bombard: Mathematics, 24 ranged, cannon model")
    check(one(db, "SELECT Happiness FROM Buildings WHERE Type='BUILDING_OB_CAMI'") == 1 and
          one(db, "SELECT Yield FROM Building_YieldChanges WHERE BuildingType='BUILDING_OB_CAMI' AND YieldType='YIELD_FAITH'") == 4,
          "Mosque: 4 Faith, 1 Happiness")
    check(one(db, "SELECT SUM(Yield) FROM Building_YieldChanges WHERE BuildingType='BUILDING_OB_KAPALICARSI' AND YieldType='YIELD_GOLD'") >= 4,
          "Grand Bazaar gold")
    check(one(db, "SELECT COUNT(*) FROM Trait_FreePromotionUnitCombats WHERE PromotionType='PROMOTION_OB_GHAZA'") == 5,
          "Ghaza promotion for five unit types")
    check(one(db, "SELECT ExtraEmbarkMoves FROM Traits WHERE Type='TRAIT_OB_OSMAN'") == 1, "embark bonus")
    check(one(db, "SELECT COUNT(*) FROM Building_ClassesNeededInCity WHERE BuildingType='BUILDING_OB_MEDRESE'") >= 1,
          "Medrese needs a Library like the University")
    check(one(db, "SELECT TradeRouteLandGoldBonus FROM Buildings WHERE Type='BUILDING_OB_KERVANSARAY'") ==
          one(db, "SELECT TradeRouteLandGoldBonus FROM Buildings WHERE Type='BUILDING_CARAVANSARY'"), "Kervansaray keeps trade bonus")
    check(one(db, "SELECT COUNT(*) FROM Building_UnitCombatFreeExperiences WHERE BuildingType='BUILDING_OB_TOPHANE'") ==
          one(db, "SELECT COUNT(*) FROM Building_UnitCombatFreeExperiences WHERE BuildingType='BUILDING_ARMORY'")
          or one(db, "SELECT COUNT(*) FROM Building_DomainFreeExperiences WHERE BuildingType='BUILDING_OB_TOPHANE'") > 0,
          "Tophane keeps the Armory experience")
    check(one(db, "SELECT ArtDefineTag FROM Civilizations WHERE Type='CIVILIZATION_OB_OTTOMAN'") ==
          one(db, "SELECT ArtDefineTag FROM Civilizations WHERE Type='CIVILIZATION_OTTOMAN'"), "Ottoman city art")

    # every TXT_KEY the mod references must exist
    texts = {r[0] for r in db.execute("SELECT Tag FROM Language_en_US")}
    refs = []
    for table, cols in (("Civilizations", ("Description", "ShortDescription", "Adjective", "Civilopedia", "DawnOfManQuote")),
                        ("Leaders", ("Description",)), ("Traits", ("Description", "ShortDescription")),
                        ("Units", ("Description", "Help", "Strategy", "Civilopedia")),
                        ("Buildings", ("Description", "Help", "Strategy", "Civilopedia")),
                        ("UnitPromotions", ("Description", "Help")), ("Civilization_CityNames", ("CityName",)),
                        ("Civilization_SpyNames", ("SpyName",))):
        for c in cols:
            for (v,) in db.execute('SELECT "%s" FROM "%s" WHERE "%s" LIKE \'%%_OB_%%\'' % (c, table, c)):
                if v and "_OB_" in v:
                    refs.append(v)
    missing = sorted({r for r in refs if r and r not in texts})
    check(not missing, "all text keys exist" + (": missing " + ", ".join(missing) if missing else ""))

    print("Osman Bey 1299 Scenario:")
    apply_mod(db, os.path.join(ROOT, "Osman Bey 1299 Scenario"))
    n = one(db, "SELECT COUNT(*) FROM MinorCivilizations")
    check(n == 30, "30 city-states of 1299 (got %d)" % n)
    texts = {r[0] for r in db.execute("SELECT Tag FROM Language_en_US")}
    missing = sorted({v for (v,) in db.execute("SELECT Description FROM MinorCivilizations UNION SELECT Civilopedia FROM "
                                               "MinorCivilizations UNION SELECT CityName FROM MinorCivilization_CityNames "
                                               "WHERE CityName LIKE '%_OB_%'") if v and "_OB_" in v and v not in texts})
    check(not missing, "city-state text keys exist" + (": missing " + ", ".join(missing) if missing else ""))
    bad = [r for r in db.execute("SELECT Type FROM MinorCivilizations WHERE MinorCivTrait NOT IN (SELECT Type FROM MinorCivTraits) "
                                 "OR DefaultPlayerColor NOT IN (SELECT Type FROM PlayerColors)")]
    check(not bad, "city-state traits and colours are valid" + (": " + str(bad) if bad else ""))
    print()
    if failures:
        print("%d FAILURE(S)" % len(failures))
        sys.exit(1)
    print("ALL SQL TESTS PASSED")


if __name__ == "__main__":
    main()
