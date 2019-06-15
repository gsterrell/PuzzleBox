Puzzle Box

Basic Design Philosophy: A puzzle game where little to no information about the level is hidden from the player. Goal is that the player can solve the majority of the puzzle in their mind before moving. Current plans are that the game will be a sequence of levels in which the entire level occupies a single screen (No scrolling) and that the player can see the entire level to begin with.

Planned Libraries:
Pygame

Player Mechanics: Player will have left/right movement, the ability to jump, and the ability to interact with and carry/throw objects.

Proposed Control Scheme: A/D:Left/Right J:Jump K:Interact

List of currently planned interactive objects:
1: Door to end level
2: Teleporters for player movement
3: Pressure plates (will turn on/off depending on if something is on it)
4: Levers (Player interaction switches it on/off)
5: Wall-Button (Player interaction sets state pressed, cannot undo like levers and pressure plates)
6: Moving Platforms
7: Player Barrier (Blocks player movement, can be turned on/off via pressure plates, levers and buttons)
8: Colored boxes (Red, Green, Blue) (Activates Pressure Plates, Players can stand on them and carry/throw them)
9: Colored Barriers (Red, Green, Blue) (Does not block player movement, but prevents boxes other than the specified color from passing through.

Setting: Futuristic, Sci-Fi

Art Style: TBD

Sound/Music: TBD

Important Things to Consider:
How to store player and level data.
How to load player and level data.
How to implement Gravity.

Other Considerations:
Player Key Remapping
Player Window Resizing
Controller Support
