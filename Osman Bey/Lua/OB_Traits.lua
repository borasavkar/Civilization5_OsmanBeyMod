-- ============================================================
-- Osman Bey mod - Osman's Dream
-- Captured cities have no resistance and pay Gold equal to
-- 10 x their population (istimalet, "winning over").
-- ============================================================
print("Osman Bey: OB_Traits.lua loaded")

local GOLD_PER_POP = 10
local iOttomanCiv = GameInfoTypes["CIVILIZATION_OB_OTTOMAN"]

GameEvents.CityCaptureComplete.Add(function(iOldOwner, bIsCapital, iX, iY, iNewOwner)
	if iOttomanCiv == nil then return end
	local pPlayer = Players[iNewOwner]
	if pPlayer == nil or pPlayer:GetCivilizationType() ~= iOttomanCiv then return end
	local pPlot = Map.GetPlot(iX, iY)
	if pPlot == nil then return end
	local pCity = pPlot:GetPlotCity()
	if pCity == nil then return end

	local iResistance = pCity:GetResistanceTurns()
	if iResistance > 0 then
		pCity:ChangeResistanceTurns(-iResistance)
	end
	local iGold = math.max(1, pCity:GetPopulation()) * GOLD_PER_POP
	pPlayer:ChangeGold(iGold)

	if pPlayer:IsHuman() and iNewOwner == Game.GetActivePlayer() then
		local sText = Locale.ConvertTextKey("TXT_KEY_OB_ISTIMALET", pCity:GetName(), iGold)
		local sShort = Locale.ConvertTextKey("TXT_KEY_OB_ISTIMALET_SHORT")
		pPlayer:AddNotification(NotificationTypes.NOTIFICATION_GENERIC, sText, sShort, iX, iY)
	end
end)
