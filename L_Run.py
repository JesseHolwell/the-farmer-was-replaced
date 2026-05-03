leaderboardMap = {
	Leaderboards.Hay: "LHay",
	Leaderboards.Hay_Single: "LHaySingle",
	Leaderboards.Wood: "LWood",
	Leaderboards.Wood_Single: "LWood",
	Leaderboards.Carrots: "LCarrots",
	Leaderboards.Carrots_Single: "LCarrots",
	Leaderboards.Pumpkins: "LPumpkins",
	Leaderboards.Pumpkins_Single: "LPumpkins",
	Leaderboards.Sunflowers: "LSunflowers",
	Leaderboards.Sunflowers_Single: "LSunflowers",
	Leaderboards.Cactus: "LCactus",
	Leaderboards.Cactus_Single: "LCactus",
	Leaderboards.Dinosaur: "LDinosaur",
	Leaderboards.Maze: "LMaze",
	Leaderboards.Maze_Single: "LMaze",
	Leaderboards.Fastest_Reset: "LFull"
}

leaderboard = Leaderboards.Hay

leaderboard_run(leaderboard, leaderboardMap[leaderboard], 100000)