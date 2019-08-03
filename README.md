Puzzle Box

Basic Design Philosophy: A puzzle game where little to no information about the level is hidden from the player. Goal is that the player can solve the majority of the puzzle in their mind before moving. Current plans are that the game will be a sequence of levels in which the entire level occupies a single screen (No scrolling) and that the player can see the entire level to begin with.

Used libraries:
Pygame

Player Mechanics: Player will have left/right movement, the ability to jump, and the ability to interact with and carry/throw objects.

Proposed Control Scheme: A/D:Left/Right J:Jump K:Interact S:Save

List of current interactive objects:

1: Door to end level

2: Player Barrier (Blocks player movement, can be turned on/off via pressure plates, levers and buttons)

3: Colored boxes (Red, Green, Blue) (Activates Pressure Plates, Players can stand on them and carry/throw them) 

4: Teleporters for player movement

5: Pressure plates (will turn on/off depending on if something is on it)

6: Wall-Button (Player interaction sets state pressed, cannot undo like levers and pressure plates)

7: Level saving (can save on any level by pressing the S key, can load from the title screen)

List of currently planned objects:

1: Levers (Player interaction switches it on/off)

6: Moving Platforms

3: Colored Barriers (Red, Green, Blue) (Does not block player movement, but prevents boxes other than the specified color from passing through.

Setting: Futuristic, Sci-Fi

Art Style: TBD

Sound/Music: TBD

Future possibilities:
Player Key Remapping
Player Window Resizing
Controller Support

Work separation:
Artir Hyseni: title screen graphics, title screen setup, title/game transition, font rendering.
Raymond Chen: lead designer, graphic acquisition, gravity/fall mechanics, collision mechanics, game framework, music acquisition, art acquisition.
Gregory Terrell: floor/wall collision, game framework, level initialization, level saving/loading, art acquisition.

