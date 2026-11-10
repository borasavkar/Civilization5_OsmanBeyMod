-- ============================================================
-- Osman Bey 1299 Scenario - setup screen
-- Lets the player pick a civilization and a difficulty, then
-- starts a game on the "Ottoman Frontiers (1299)" map with the
-- great powers and city-states of 1299.
-- ============================================================
include("IconSupport")

local MAP_MOD_ID = "4f6b2c1e-8a3d-4e57-b0c9-2d1e9a7f1299"
local MAP_FILE = "Maps/OB_Ottoman1299.lua"

local SCENARIO_CIVS = {
	"CIVILIZATION_OB_OTTOMAN",
	"CIVILIZATION_BYZANTIUM",
	"CIVILIZATION_MONGOL",
	"CIVILIZATION_EGYPT",
	"CIVILIZATION_VENICE",
	"CIVILIZATION_AUSTRIA",
	"CIVILIZATION_POLAND",
	"CIVILIZATION_MOROCCO",
}

local g_Selected = 1
local g_Difficulty = nil
local g_Difficulties = {}
local g_Buttons = {}

local function Role(civType)
	local key = "TXT_KEY_OB1299_ROLE_" .. string.gsub(civType, "CIVILIZATION_", "")
	return Locale.ConvertTextKey(key)
end

local function LeaderOf(civ)
	local row = GameInfo.Civilization_Leaders("CivilizationType = '" .. civ.Type .. "'")()
	if row == nil then return nil end
	return GameInfo.Leaders[row.LeaderheadType]
end

local function UpdateDifficultyText()
	local info = GameInfo.HandicapInfos[g_Difficulty]
	if info ~= nil then
		Controls.DifficultyLabel:SetText(Locale.ConvertTextKey("TXT_KEY_OB1299_DIFFICULTY", Locale.ConvertTextKey(info.Description)))
	end
end

local function Refresh()
	for i, ctrl in ipairs(g_Buttons) do
		ctrl.Highlight:SetHide(i ~= g_Selected)
	end
	local civ = GameInfo.Civilizations[SCENARIO_CIVS[g_Selected]]
	local leader = civ and LeaderOf(civ)
	if civ ~= nil and leader ~= nil then
		IconHookup(leader.PortraitIndex, 128, leader.IconAtlas, Controls.Portrait)
		Controls.CivName:SetText(Locale.ConvertTextKey(leader.Description) .. " - " .. Locale.ConvertTextKey(civ.ShortDescription))
		Controls.CivRole:SetText(Role(civ.Type))
	end
	UpdateDifficultyText()
end

local function BuildCivList()
	Controls.CivStack:DestroyAllChildren()
	g_Buttons = {}
	for i, civType in ipairs(SCENARIO_CIVS) do
		local civ = GameInfo.Civilizations[civType]
		local leader = civ and LeaderOf(civ)
		if civ ~= nil and leader ~= nil then
			local ctrl = {}
			ContextPtr:BuildInstanceForControl("CivInstance", ctrl, Controls.CivStack)
			IconHookup(civ.PortraitIndex, 64, civ.IconAtlas, ctrl.Icon)
			ctrl.Name:SetText(Locale.ConvertTextKey(civ.ShortDescription))
			ctrl.Leader:SetText(Locale.ConvertTextKey(leader.Description))
			ctrl.Button:RegisterCallback(Mouse.eLClick, function() g_Selected = i; Refresh() end)
			g_Buttons[i] = ctrl
		end
	end
	Controls.CivStack:CalculateSize()
	Controls.CivStack:ReprocessAnchoring()
	Controls.CivScrollPanel:CalculateInternalSize()
end

local function CycleDifficulty()
	local idx = 1
	for i, id in ipairs(g_Difficulties) do
		if id == g_Difficulty then idx = i end
	end
	idx = idx + 1
	if idx > #g_Difficulties then idx = 1 end
	g_Difficulty = g_Difficulties[idx]
	UpdateDifficultyText()
end

local function StartScenario()
	PreGame.Reset()
	PreGame.SetLoadWBScenario(false)

	local iModVersion = Modding.GetActivatedModVersion(MAP_MOD_ID)
	local mapFile = Modding.GetEvaluatedFilePath(MAP_MOD_ID, iModVersion, MAP_FILE)
	if mapFile == nil or mapFile.EvaluatedPath == nil then
		print("Osman Bey 1299: map script not found - is the Osman Bey mod enabled?")
		return
	end
	PreGame.SetMapScript(mapFile.EvaluatedPath)
	PreGame.SetWorldSize(GameInfo.Worlds.WORLDSIZE_HUGE.ID)
	PreGame.SetGameSpeed(GameInfo.GameSpeeds.GAMESPEED_STANDARD.ID)
	if GameInfo.Eras.ERA_MEDIEVAL ~= nil then
		PreGame.SetEra(GameInfo.Eras.ERA_MEDIEVAL.ID)
	end
	PreGame.RandomizeMapSeed()
	PreGame.SetGameOption("GAMEOPTION_NO_TUTORIAL", true)

	-- Major civilizations: the chosen one goes to slot 0
	PreGame.ResetSlots()
	local order = {SCENARIO_CIVS[g_Selected]}
	for i, c in ipairs(SCENARIO_CIVS) do
		if i ~= g_Selected then table.insert(order, c) end
	end
	for slot, civType in ipairs(order) do
		local s = slot - 1
		PreGame.SetCivilization(s, GameInfo.Civilizations[civType].ID)
		if s > 0 then
			PreGame.SetSlotStatus(s, SlotStatus.SS_COMPUTER)
			PreGame.SetSlotClaim(s, SlotClaim.SLOTCLAIM_ASSIGNED)
		end
	end
	for s = #order, GameDefines.MAX_MAJOR_CIVS - 1 do
		PreGame.SetSlotStatus(s, SlotStatus.SS_CLOSED)
	end

	-- Every city-state left in the database is a city-state of 1299
	local nMinors = 0
	for _ in GameInfo.MinorCivilizations() do nMinors = nMinors + 1 end
	PreGame.SetNumMinorCivs(math.min(nMinors, GameDefines.MAX_MINOR_CIVS or 41))

	PreGame.SetHandicap(0, g_Difficulty)

	Events.SerialEventStartGame()
	UIManager:SetUICursor(1)
end

local function OnBack()
	UIManager:DequeuePopup(ContextPtr)
end

Controls.BackButton:RegisterCallback(Mouse.eLClick, OnBack)
Controls.StartButton:RegisterCallback(Mouse.eLClick, StartScenario)
Controls.DifficultyButton:RegisterCallback(Mouse.eLClick, CycleDifficulty)

ContextPtr:SetInputHandler(function(uiMsg, wParam, lParam)
	if uiMsg == KeyEvents.KeyDown and wParam == Keys.VK_ESCAPE then
		OnBack()
	end
	return true
end)

local function Initialize()
	for info in GameInfo.HandicapInfos("Type <> 'HANDICAP_AI_DEFAULT'") do
		table.insert(g_Difficulties, info.ID)
	end
	local prince = GameInfo.HandicapInfos.HANDICAP_PRINCE
	g_Difficulty = prince and prince.ID or g_Difficulties[1]
	BuildCivList()
	Refresh()
end

Initialize()
