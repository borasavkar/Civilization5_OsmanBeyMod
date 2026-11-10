-- ============================================================
-- Osman Bey mod - city art and map image
-- Copies the appearance of the base-game Ottoman civilization.
-- ============================================================
UPDATE Civilizations SET
	ArtDefineTag   = (SELECT ArtDefineTag   FROM Civilizations WHERE Type = 'CIVILIZATION_OTTOMAN'),
	ArtStyleType   = (SELECT ArtStyleType   FROM Civilizations WHERE Type = 'CIVILIZATION_OTTOMAN'),
	ArtStyleSuffix = (SELECT ArtStyleSuffix FROM Civilizations WHERE Type = 'CIVILIZATION_OTTOMAN'),
	ArtStylePrefix = (SELECT ArtStylePrefix FROM Civilizations WHERE Type = 'CIVILIZATION_OTTOMAN'),
	MapImage       = (SELECT MapImage       FROM Civilizations WHERE Type = 'CIVILIZATION_OTTOMAN')
WHERE Type = 'CIVILIZATION_OB_OTTOMAN'
AND EXISTS (SELECT 1 FROM Civilizations WHERE Type = 'CIVILIZATION_OTTOMAN');
