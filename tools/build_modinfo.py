#!/usr/bin/env python3
"""Scans both mod folders, computes MD5 hashes and writes their .modinfo files."""
import hashlib
import os
import sys
from xml.sax.saxutils import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_mod import MOD1, MOD1_ID, MOD2, MOD2_ID  # noqa: E402

VERSION = 1
BNW_ID = "6DA07636-4123-4018-B643-6575B4EC336B"   # Brave New World (Expansion2.Civ5Pkg)

MODS = [
    {
        "folder": MOD1, "id": MOD1_ID, "file": "Osman Bey (v %d).modinfo",
        "name": "Osman Bey (Ottoman Beylik)",
        "teaser": "Osman Bey and the Ottoman Beylik, with Akinci and Janissary units, three Ottoman buildings and a "
                  "real map of the Ottoman world in 1299.",
        "description": "Adds Osman Bey, founder of the Ottoman state, leading the Ottoman Beylik. Unique abilities: "
                       "Osman's Dream (captured cities have no resistance and pay gold; faster Great Generals), the "
                       "Akinci (replaces the Knight), the Janissary (replaces the Musketman), the Kervansaray, the "
                       "Medrese and the Tophane. Includes the 'Ottoman Frontiers (1299)' map: real geography from "
                       "Vienna to Yemen and from Morocco to the Caspian Sea, with rivers and historical start "
                       "positions. Requires Brave New World.",
        "hide_setup": 0, "multiplayer": 1,
        "db": ["Core/OB_Civilization.xml", "Text/OB_Text.xml", "Core/OB_Promotions.xml", "Core/OB_Audio.xml",
               "Core/OB_Uniques.sql", "Core/OB_Art.sql"],
        "no_import": ["Lua/OB_Traits.lua", "Maps/OB_Ottoman1299.lua"],
        "entry": [("InGameUIAddin", "Lua/OB_Traits.lua", "OB_Traits", "Osman's Dream (captured cities)"),
                  ("MapScript", "Maps/OB_Ottoman1299.lua", "TXT_KEY_OB_MAP_NAME", "TXT_KEY_OB_MAP_HELP")],
        "deps": [],
        "audio": 1,
    },
    {
        "folder": MOD2, "id": MOD2_ID, "file": "Osman Bey 1299 Scenario (v %d).modinfo",
        "name": "Rise of the Ottomans: 1299 (Scenario)",
        "teaser": "Anatolia, 1299: play Osman Bey or one of the great powers of the age, with the cities and "
                  "city-states of the time.",
        "description": "A scenario for the Osman Bey mod. Starts in the Medieval era on the 'Ottoman Frontiers (1299)' "
                       "map with the Ottoman Beylik, the Byzantine Empire, the Ilkhanate, the Mamluks, Venice, "
                       "Austria, Poland and the Marinids. The great powers start with the cities they held in 1299, "
                       "and the city-states are the Anatolian beyliks and the kingdoms of the time. Start it from "
                       "Mods > Single Player > Custom Game. Requires the Osman Bey (Ottoman Beylik) mod and Brave "
                       "New World.",
        "hide_setup": 1, "multiplayer": 0,
        "db": ["Core/OB1299_CityStates.sql", "Text/OB1299_Text.xml"],
        "no_import": ["Lua/OB1299_Scenario.lua", "UI/OB1299_Setup.lua", "UI/OB1299_Setup.xml"],
        "entry": [("Custom", "UI/OB1299_Setup.xml", "TXT_KEY_OB1299_TITLE", "TXT_KEY_OB1299_DESC"),
                  ("InGameUIAddin", "Lua/OB1299_Scenario.lua", "OB1299_Scenario", "Places the cities of 1299")],
        "deps": [(MOD1_ID, "Osman Bey (Ottoman Beylik)")],
        "audio": 0,
    },
]


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def write_modinfo(m):
    folder = m["folder"]
    for f in os.listdir(folder):
        if f.endswith(".modinfo"):
            os.remove(os.path.join(folder, f))
    files = []
    for dirpath, _, names in os.walk(folder):
        for n in names:
            files.append(os.path.relpath(os.path.join(dirpath, n), folder).replace(os.sep, "/"))
    files.sort()
    for f in m["db"] + m["no_import"]:
        assert f in files, "missing file: " + f
    no_import = set(m["db"]) | set(m["no_import"])

    out = ['<?xml version="1.0" encoding="utf-8"?>',
           '<Mod id="%s" version="%d">' % (m["id"], VERSION),
           "  <Properties>",
           "    <Name>%s</Name>" % escape(m["name"]),
           "    <Stability>Beta</Stability>",
           "    <Teaser>%s</Teaser>" % escape(m["teaser"]),
           "    <Description>%s</Description>" % escape(m["description"]),
           "    <Authors>Bora Savkar</Authors>",
           "    <HideSetupGame>%d</HideSetupGame>" % m["hide_setup"],
           "    <AffectsSavedGames>1</AffectsSavedGames>",
           "    <MinCompatibleSaveVersion>0</MinCompatibleSaveVersion>",
           "    <SupportsSinglePlayer>1</SupportsSinglePlayer>",
           "    <SupportsMultiplayer>%d</SupportsMultiplayer>" % m["multiplayer"],
           "    <SupportsHotSeat>%d</SupportsHotSeat>" % m["multiplayer"],
           "    <SupportsMac>1</SupportsMac>",
           "    <ReloadAudioSystem>%d</ReloadAudioSystem>" % m["audio"],
           "    <ReloadLandmarkSystem>0</ReloadLandmarkSystem>",
           "    <ReloadStrategicViewSystem>0</ReloadStrategicViewSystem>",
           "    <ReloadUnitSystem>0</ReloadUnitSystem>",
           "  </Properties>",
           "  <Dependencies>",
           '    <Dlc id="%s" minversion="0" maxversion="999" />' % BNW_ID]
    for dep_id, title in m["deps"]:
        out.append('    <Mod id="%s" minversion="0" maxversion="999" title="%s" />' % (dep_id, escape(title)))
    out += ["  </Dependencies>",
            "  <References />",
            "  <Blocks />",
            "  <Files>"]
    for f in files:
        out.append('    <File md5="%s" import="%s">%s</File>' % (md5(os.path.join(folder, f)), "0" if f in no_import else "1",
                                                              escape(f)))
    out += ["  </Files>", "  <Actions>", "    <OnModActivated>"]
    for f in m["db"]:
        out.append("      <UpdateDatabase>%s</UpdateDatabase>" % f)
    out += ["    </OnModActivated>", "  </Actions>", "  <EntryPoints>"]
    for typ, f, name, desc in m["entry"]:
        out += ['    <EntryPoint type="%s" file="%s">' % (typ, f),
                "      <Name>%s</Name>" % escape(name),
                "      <Description>%s</Description>" % escape(desc),
                "    </EntryPoint>"]
    out += ["  </EntryPoints>", "</Mod>", ""]
    path = os.path.join(folder, m["file"] % VERSION)
    with open(path, "w", encoding="utf-8", newline="\r\n") as fh:
        fh.write("\n".join(out))
    print("modinfo: %s (%d files)" % (os.path.basename(path), len(files)))


def main():
    for m in MODS:
        write_modinfo(m)


if __name__ == "__main__":
    main()
