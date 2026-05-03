leaderboardMap = {
	Leaderboards.Hay: "LHay",
	Leaderboards.Hay_Single: "LHaySingle",
	Leaderboards.Wood: "LWood",
	Leaderboards.Wood_Single: "LWoodSingle",
	Leaderboards.Carrots: "LCarrots",
	Leaderboards.Carrots_Single: "LCarrotsSingle",
	Leaderboards.Pumpkins: "LPumpkins",
	Leaderboards.Pumpkins_Single: "LPumpkinsSingle",
	Leaderboards.Sunflowers: "LSunflowers",
	Leaderboards.Sunflowers_Single: "LSunflowersSingle",
	Leaderboards.Cactus: "LCactus",
	Leaderboards.Cactus_Single: "LCactusSingle",
	Leaderboards.Dinosaur: "LDinosaur",
	Leaderboards.Maze: "LMaze",
	Leaderboards.Maze_Single: "LMazeSingle",
	Leaderboards.Fastest_Reset: "LFull"
}

leaderboard = Leaderboards.Hay

leaderboard_run(leaderboard, leaderboardMap[leaderboard], 100000)