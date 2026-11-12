-- Runs the map script and the scenario start script against a small mock of the
-- Civilization V Lua API (LuaJIT / Lua 5.1).
-- Usage (from the repository root): luajit tools/test_lua.lua
local ROOT = "./"
local failures = 0
local function check(cond, msg)
	if not cond then failures = failures + 1; io.write("FAIL: ", msg, "\n") end
end

-- ------------------------------------------------------------------ mock API
local realPrint = print
local log = {}
print = function(...) local t = {} for i = 1, select("#", ...) do t[#t + 1] = tostring(select(i, ...)) end log[#log + 1] = table.concat(t, " ") end
include = function() end

GameDefines = {MAX_MAJOR_CIVS = 22, MAX_CIV_PLAYERS = 63, MAX_MINOR_CIVS = 41}
PlotTypes = {PLOT_OCEAN = 0, PLOT_LAND = 1, PLOT_HILLS = 2, PLOT_MOUNTAIN = 3}
FlowDirectionTypes = {FLOWDIRECTION_NORTH = 0, FLOWDIRECTION_NORTHEAST = 1, FLOWDIRECTION_SOUTHEAST = 2,
	FLOWDIRECTION_SOUTH = 3, FLOWDIRECTION_SOUTHWEST = 4, FLOWDIRECTION_NORTHWEST = 5}
GameInfoTypes = {TERRAIN_GRASS = 0, TERRAIN_PLAINS = 1, TERRAIN_DESERT = 2, TERRAIN_TUNDRA = 3, TERRAIN_SNOW = 4,
	TERRAIN_COAST = 5, TERRAIN_OCEAN = 6, FEATURE_ICE = 0, UNITCLASS_SETTLER = 1, BUILDING_PALACE = 10,
	BUILDING_WALLS = 11, BUILDING_CASTLE = 12, FEATURE_FOREST = 1, FEATURE_JUNGLE = 2, FEATURE_MARSH = 3,
	RESOURCE_WHEAT = 40, RESOURCE_COW = 41, RESOURCE_SHEEP = 42, RESOURCE_HORSE = 43, RESOURCE_IRON = 44,
	RESOURCE_WINE = 45, RESOURCE_SILK = 46}

local CIVS = {"CIVILIZATION_OB_OTTOMAN", "CIVILIZATION_BYZANTIUM", "CIVILIZATION_MONGOL", "CIVILIZATION_EGYPT",
	"CIVILIZATION_VENICE", "CIVILIZATION_AUSTRIA", "CIVILIZATION_POLAND", "CIVILIZATION_MOROCCO"}
local MINORS = {"MINOR_CIV_OB_KARAMAN", "MINOR_CIV_OB_GERMIYAN", "MINOR_CIV_OB_KARESI", "MINOR_CIV_OB_MENTESE",
	"MINOR_CIV_OB_CANDAR", "MINOR_CIV_OB_TREBIZOND", "MINOR_CIV_OB_GEORGIA", "MINOR_CIV_OB_CILICIA",
	"MINOR_CIV_OB_CYPRUS", "MINOR_CIV_OB_EPIRUS", "MINOR_CIV_OB_ATHENS", "MINOR_CIV_OB_GOLDEN_HORDE",
	"MINOR_CIV_OB_CAFFA", "MINOR_CIV_OB_HAFSIDS", "MINOR_CIV_OB_ZAYYANIDS", "MINOR_CIV_OB_RASULIDS",
	"MINOR_CIV_OB_MECCA", "MINOR_CIV_OB_SICILY", "MINOR_CIV_OB_NAPLES", "MINOR_CIV_OB_MAKURIA",
	"MINOR_CIV_OB_BULGARIA", "MINOR_CIV_RAGUSA", "MINOR_CIV_GENOA", "MINOR_CIV_FLORENCE", "MINOR_CIV_VATICAN_CITY",
	"MINOR_CIV_BUDAPEST", "MINOR_CIV_BELGRADE", "MINOR_CIV_PRAGUE", "MINOR_CIV_KIEV", "MINOR_CIV_ORMUS"}
GameInfo = {Civilizations = {}, MinorCivilizations = {}}
for i, c in ipairs(CIVS) do GameInfo.Civilizations[i - 1] = {Type = c, ID = i - 1} end
for i, m in ipairs(MINORS) do GameInfo.MinorCivilizations[i - 1] = {Type = m, ID = i - 1} end

-- map
local W, H
local plots = {}
local Plot = {}
Plot.__index = Plot
function Plot:GetX() return self.x end
function Plot:GetY() return self.y end
function Plot:IsWater() return self.ptype == PlotTypes.PLOT_OCEAN end
function Plot:IsMountain() return self.ptype == PlotTypes.PLOT_MOUNTAIN end
function Plot:IsHills() return self.ptype == PlotTypes.PLOT_HILLS end
function Plot:IsImpassable() return false end
function Plot:GetTerrainType() return self.terrain end
function Plot:GetFeatureType() return self.feature or -1 end
function Plot:IsRiver() return self.river == true end
function Plot:IsCoastalLand() return false end
function Plot:SetWOfRiver(b, f) assert(f ~= nil, "flow nil"); self.river = true; self.wRiver = f end
function Plot:SetNWOfRiver(b, f) assert(f ~= nil, "flow nil"); self.river = true; self.nwRiver = f end
function Plot:SetNEOfRiver(b, f) assert(f ~= nil, "flow nil"); self.river = true; self.neRiver = f end
function Plot:IsCity() return self.city ~= nil end
function Plot:GetResourceType() return self.res or -1 end
function Plot:SetResourceType(r, n) self.res = r; self.resN = n end
function Plot:SetFeatureType(f) self.feature = f end
function Plot:SetTerrainType(t) self.terrain = t end
function Plot:GetOwner() return self.owner or -1 end
function Plot:GetNumUnits() return 0 end
function Plot:GetPlotCity() return self.city end

local function key(x, y) return y * 1000 + x end
Map = {}
function Map.GetPlot(x, y) if x < 0 or y < 0 or x >= W or y >= H then return nil end return plots[key(x, y)] end
local function cube(x, y) local q = x - (y - y % 2) / 2; return q, y, -q - y end
function Map.PlotDistance(x1, y1, x2, y2)
	local a1, b1, c1 = cube(x1, y1); local a2, b2, c2 = cube(x2, y2)
	return math.max(math.abs(a1 - a2), math.abs(b1 - b2), math.abs(c1 - c2))
end
function Map.GetCustomOption(i) return 1 end
function Map.Rand(n) return 0 end

function GetCoreMapOptions() return nil, nil, nil, nil, {Name = "res"} end
function SetPlotTypes(t)
	for y = 0, H - 1 do for x = 0, W - 1 do
		plots[key(x, y)] = setmetatable({x = x, y = y, ptype = t[y * W + x], terrain = GameInfoTypes.TERRAIN_OCEAN}, Plot)
	end end
end
function GenerateCoasts() end
function SetTerrainTypes(t) for y = 0, H - 1 do for x = 0, W - 1 do plots[key(x, y)].terrain = t[y * W + x] end end end
FeatureGenerator = {Create = function() return {AddFeatures = function() end} end}

-- players
Players = {}
local Player = {}
Player.__index = Player
function Player:IsEverAlive() return true end
function Player:IsAlive() return true end
function Player:GetCivilizationType() return self.civ end
function Player:GetMinorCivType() return self.minor end
function Player:GetStartingPlot() return self.start end
function Player:SetStartingPlot(p) self.start = p end
function Player:GetNumCities() return #self.cities end
function Player:InitCity(x, y)
	local p = Map.GetPlot(x, y)
	local c = {plot = p, name = "?", pop = 1, capital = (#self.cities == 0), b = {}}
	function c:SetName(n) self.name = n end
	function c:SetPopulation(n) self.pop = n end
	function c:IsCapital() return self.capital end
	function c:SetNumRealBuilding(id, n) self.b[id] = n end
	p.city = c; p.owner = self.id
	table.insert(self.cities, c)
	return c
end
function Player:Units()
	local i = 0
	return function() i = i + 1; return self.units[i] end
end
-- units: 1 settler, then a warrior (type 100) that can upgrade to spearman (101) and pikeman (102)
local function mkUnit(t, combat)
	return {t = t, GetUnitClassType = function(u) return u.t == 1 and 1 or 7 end, Kill = function(u) u.dead = true end,
		IsCombatUnit = function() return combat end, GetDomainType = function() return 0 end,
		GetUnitType = function(u) return u.t end, GetX = function() return 5 end, GetY = function() return 5 end}
end
function Player:InitUnit(t, x, y) local u = mkUnit(t, true); table.insert(self.units, u); return u end
function Player:IsBarbarian() return false end
function Player:GetTeam() return self.id end
for i, c in ipairs(CIVS) do
	local pl = setmetatable({id = i - 1, civ = i - 1, cities = {}, units = {}}, Player)
	table.insert(pl.units, mkUnit(1, false))
	table.insert(pl.units, mkUnit(100, true))
	Players[i - 1] = pl
end
local NUM_MINORS = #MINORS
for n = 1, NUM_MINORS do
	Players[n + GameDefines.MAX_MAJOR_CIVS - 1] = setmetatable({id = n + 21, minor = n - 1, cities = {}, units = {}}, Player)
end

-- AssignStartingPlots: random land starts, then the map script's hooks
local function randomLand(seed)
	local n = 0
	for y = 5, H - 6 do for x = 5, W - 6 do
		local p = Map.GetPlot(x, y)
		if not p:IsWater() and not p:IsMountain() then n = n + 1; if n == seed then return p end end
	end end
end
AssignStartingPlots = {}
function AssignStartingPlots.Create()
	local self = {iNumCityStates = NUM_MINORS, city_state_validity_table = {}, cityStatePlots = {}, playerCollisionData = {}}
	function self:GenerateRegions() end
	function self:ChooseLocations() end
	function self:BalanceAndAssign() for i = 0, #CIVS - 1 do Players[i]:SetStartingPlot(randomLand(97 * (i + 1))) end end
	function self:PlaceImpactAndRipples() end
	function self:PlaceResourceImpact() end
	function self:PlaceNaturalWonders() end
	function self:PlaceCityStates()
		for n = 1, NUM_MINORS do
			self.city_state_validity_table[n] = true
			local p = randomLand(53 * n + 11)
			Players[n + 21]:SetStartingPlot(p)
			self.cityStatePlots[n] = {p:GetX(), p:GetY(), 1}
		end
	end
	function self:PlaceResourcesAndCityStates() self:PlaceCityStates() end
	return self
end

-- ------------------------------------------------------------------ map script
dofile(ROOT .. "Osman Bey/Maps/OB_Ottoman1299.lua")
local info = GetMapScriptInfo()
check(info.Name == "TXT_KEY_OB_MAP_NAME", "map name")
local init = GetMapInitData(0)
W, H = init.Width, init.Height
GeneratePlotTypes()
GenerateTerrain()
AddRivers()
AddFeatures()
StartPlotSystem()

local nRiver, nLand = 0, 0
for _, p in pairs(plots) do
	if p.river then nRiver = nRiver + 1 end
	if not p:IsWater() then nLand = nLand + 1 end
end
check(nRiver > 500, "rivers placed: " .. nRiver)

local expected = {}
for _, s in ipairs(OB_MAP.MajorStarts) do if expected[s[1]] == nil then expected[s[1]] = {s[2], s[3]} end end
for i, c in ipairs(CIVS) do
	local sp = Players[i - 1]:GetStartingPlot()
	local e = expected[c]
	local d = Map.PlotDistance(sp:GetX(), sp:GetY(), e[1], e[2])
	check(d <= 3, c .. " start is " .. d .. " tiles from its historic site")
	check(not sp:IsWater() and not sp:IsMountain(), c .. " start on valid land")
end
do
	local sp = Players[0]:GetStartingPlot()
	local found = {}
	for _, p in pairs(plots) do
		if p.res and Map.PlotDistance(p.x, p.y, sp:GetX(), sp:GetY()) <= 5 then found[p.res] = true end
	end
	for _, r in ipairs({"RESOURCE_WHEAT", "RESOURCE_COW", "RESOURCE_HORSE", "RESOURCE_IRON", "RESOURCE_WINE", "RESOURCE_SILK"}) do
		check(found[GameInfoTypes[r]], "Ottoman start has " .. r)
	end
end
local moved = 0
for n = 1, NUM_MINORS do
	local p = Players[n + 21]:GetStartingPlot()
	local site = OB_MAP.MinorSites[MINORS[n]]
	if site ~= nil and Map.PlotDistance(p:GetX(), p:GetY(), site[1], site[2]) <= 4 then moved = moved + 1 end
	for i = 0, #CIVS - 1 do
		local sp = Players[i]:GetStartingPlot()
		check(Map.PlotDistance(p:GetX(), p:GetY(), sp:GetX(), sp:GetY()) >= 4,
			MINORS[n] .. " is too close to " .. CIVS[i + 1])
	end
end
check(moved >= NUM_MINORS - 3, "city-states at historic sites: " .. moved .. "/" .. NUM_MINORS)

-- ------------------------------------------------------------------ scenario start script
DomainTypes = {DOMAIN_LAND = 0}
Teams = setmetatable({}, {__index = function() return {IsHasTech = function(_, t) return t ~= 302 end} end})
GameInfoTypes.TECH_BRONZE = 300; GameInfoTypes.TECH_CIVIL = 301; GameInfoTypes.TECH_GUNPOWDER = 302
local U = {[100] = {ID = 100, Type = "UNIT_WARRIOR"}, [101] = {ID = 101, Type = "UNIT_SPEARMAN", PrereqTech = "TECH_BRONZE"},
	[102] = {ID = 102, Type = "UNIT_PIKEMAN", PrereqTech = "TECH_CIVIL"}, [103] = {ID = 103, Type = "UNIT_MUSKETMAN", PrereqTech = "TECH_GUNPOWDER"}}
for _, u in pairs(U) do U[u.Type] = u end
GameInfo.Units = U
GameInfo.UnitClasses = {UNITCLASS_SPEARMAN = {DefaultUnit = "UNIT_SPEARMAN"}, UNITCLASS_PIKEMAN = {DefaultUnit = "UNIT_PIKEMAN"},
	UNITCLASS_MUSKETMAN = {DefaultUnit = "UNIT_MUSKETMAN"}}
local UP = {UNIT_WARRIOR = "UNITCLASS_SPEARMAN", UNIT_SPEARMAN = "UNITCLASS_PIKEMAN", UNIT_PIKEMAN = "UNITCLASS_MUSKETMAN"}
local function query(f) return function(_, q) local r = f(q); local done = false
	return function() if done or r == nil then return nil end done = true return r end end end
GameInfo.Unit_ClassUpgrades = setmetatable({}, {__call = query(function(q)
	local t = string.match(q, "'(.-)'"); return UP[t] and {UnitClassType = UP[t]} end)})
GameInfo.Civilization_UnitClassOverrides = setmetatable({}, {__call = query(function() return nil end)})
GameInfo.Unit_ResourceQuantityRequirements = setmetatable({}, {__call = query(function() return nil end)})
PreGame = {GetMapScript = function() return "C:/x/Maps/OB_Ottoman1299.lua" end}
Game = {GetGameTurn = function() return 125 end, GetStartTurn = function() return 125 end}
dofile(ROOT .. "Osman Bey 1299 Scenario/Lua/OB1299_Scenario.lua")
local byz = Players[1]
check(#byz.cities == 5, "Byzantium founded " .. #byz.cities .. " cities")
check(byz.cities[1] and byz.cities[1].name == "Constantinople", "Byzantine capital is Constantinople")
check(byz.cities[1] and byz.cities[1].b[GameInfoTypes.BUILDING_WALLS] == 1 and not byz.cities[1].b[GameInfoTypes.BUILDING_CASTLE], "Constantinople has walls but no castle")
check(byz.units[1].dead == true, "Byzantine settler removed")
check(#Players[0].cities == 0 and not Players[0].units[1].dead, "Ottoman beylik keeps its settler")
local ot = Players[0].units
check(ot[2].dead and ot[3] ~= nil and ot[3].t == 102, "Ottoman warrior upgraded to pikeman (stops before gunpowder)")
local total = 0
for i = 1, #CIVS - 1 do total = total + #Players[i].cities end
check(total >= 26, "scenario cities founded: " .. total)
for i = 1, #CIVS - 1 do
	for _, c in ipairs(Players[i].cities) do
		for j = 1, #CIVS - 1 do for _, c2 in ipairs(Players[j].cities) do
			if c ~= c2 then
				check(Map.PlotDistance(c.plot.x, c.plot.y, c2.plot.x, c2.plot.y) >= 3, c.name .. " too close to " .. c2.name)
			end
		end end
	end
end

-- ------------------------------------------------------------------ trait script
local handler
GameEvents = {CityCaptureComplete = {Add = function(f) handler = f end}}
GameInfoTypes.CIVILIZATION_OB_OTTOMAN = 0
dofile(ROOT .. "Osman Bey/Lua/OB_Traits.lua")
check(handler ~= nil, "capture handler registered")
local gold, resist = 0, 4
local pc = {GetResistanceTurns = function() return resist end, ChangeResistanceTurns = function(_, n) resist = resist + n end,
	GetPopulation = function() return 6 end, GetName = function() return "Bursa" end}
local pl = Players[0]
pl.ChangeGold = function(_, n) gold = gold + n end
pl.IsHuman = function() return false end
local tp = Map.GetPlot(50, 50); tp.city = pc
handler(1, false, 50, 50, 0)
check(resist == 0 and gold == 60, "istimalet: resistance " .. resist .. ", gold " .. gold)

print = realPrint
for _, l in ipairs(log) do if string.find(l, "fail") or string.find(l, "error") or string.find(l, "no room") then print("log: " .. l) end end
print(string.format("land %d, river plots %d, city-states at home %d/%d", nLand, nRiver, moved, NUM_MINORS))
if failures == 0 then print("ALL LUA TESTS PASSED") else print(failures .. " FAILURE(S)"); os.exit(1) end
