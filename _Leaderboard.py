leaderboardMap = {
	Leaderboards.Hay: "L_Hay",
	Leaderboards.Hay_Single: "L_HaySingle",
	Leaderboards.Wood: "L_Wood",
	Leaderboards.Wood_Single: "L_WoodSingle",
	Leaderboards.Carrots: "L_Carrots",
	Leaderboards.Carrots_Single: "L_CarrotsSingle",
	Leaderboards.Pumpkins: "L_Pumpkins",
	Leaderboards.Pumpkins_Single: "L_PumpkinsSingle",
	Leaderboards.Sunflowers: "L_Sunflowers",
	Leaderboards.Sunflowers_Single: "L_SunflowersSingle",
	Leaderboards.Cactus: "L_Cactus",
	Leaderboards.Cactus_Single: "L_CactusSingle",
	Leaderboards.Dinosaur: "L_Dinosaur",
	Leaderboards.Maze: "L_Maze",
	Leaderboards.Maze_Single: "L_MazeSingle",
	Leaderboards.Fastest_Reset: "L_Full"
}

leaderboard = Leaderboards.Hay

leaderboard_run(leaderboard, leaderboardMap[leaderboard], 100000)