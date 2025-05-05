# COMP-61-2025 Game Design README
Alek Newman
## Demo Video:
(https://youtu.be/izRT6_KZCao)
## Setup:
Go to Extra Credit Game.py for the code and setup. 
## Game Overview:
### Game Title: 
Superman and the Jaws of Death
### Game Summary:
  Superman and the Jaws of Death is a Flappy Bird-like style game. In the game you play as superman flying through a giant intergalatic monsters mouth and throat. You have to avoid its teeth. Your purpose is to jump through the gaps until you reach each checkpoint. If you get far enough you can fly into the heart, kill the monster, and save the universe. 
  To play the game you TAP the spacebar on your keyboard to jump through the air. You are only moving forward so all you must do is not hit the white teeth. If you do hit the teeth, just quit, go back to the main menu, and restart the game. Every time you fly through a gap without hitting something you earn a point. See if you can earn 30 points and get to the heart. Have fun!
### Core Gameplay Loop:
#### Main Player Actions:
Jumping: 
The player presses SPACE to make Superman jump, navigating through teeth (obstacles). The jump is controlled by gravity and lift.
Collision with Pipes: 
If the player collides with the pipes, the game ends.
#### Feedback Loops:
##### Score & Level: 
Every 5th pipe passed increases the score and level. Leveling up also increases pipe speed for more difficulty.
##### Sound Effects: 
Triggered every 5th and 10th pipe passed as auditory feedback for progress.
##### Heart (Win Condition): 
After reaching a certain score, a heart appears. The player must collide with it to win.
##### Game Over: 
Colliding with a pipe results in a game-over screen with options to restart or return to the main menu.
##### GIF Animation: 
A GIF near the heart plays when the player reaches it, adding visual excitement.
## Gameplay Mechanics:
### Controls:
#### Keyboard Input Scheme:
##### Jump: 
SPACE key to trigger jumping.
##### Restart: 
R key to restart the game after game over.
##### Main Menu: 
M key to return to the main menu when the game is over.
### Core Mechanics:
##### Jumping:
Keyboard: SPACE key
### Level Progression:
Advancement: Based on the number of pipes passed and the score. When you pass a pipe (the pipe moves off the screen without the player colliding with it), the score increases. The game tracks the number of pipes passed, and for every fifth pipe passed, the player's level increases by one. The pipe speed also increases slightly by 0.1 each time the player advances by 5 pipes, making the game progressively more challenging. This advancement ensures that as the player progresses, the game becomes more difficult, requiring greater skill to avoid obstacles and continue advancing through the levels.
### Win/loss Conditions:
Success is determined by the player successfully flying through the heart, which is the win condition. Once the player reaches the heart after passing a certain number of pipes (at least 27 pipes), the heart appears on the screen. If the player collides with the heart, the game triggers a win message and the game ends.

Failure in the game occurs when the player collides with a pipe. The collision detection checks if the player’s character (superman) intersects with the top or bottom of a pipe. If a collision happens, the game ends and the player is prompted with a "Game Over" message, along with options to restart or return to the main menu.
## Story and Narrative:
The Universe is threatened by an intergalatic monster called "Death". He devours planets and is coming straight for Earth. The humans call upon Superman to save them. This is no easy task for Superman however. He is stuck in a block of ice and he must go straight into the belly of the beast and fly through the heart to kill it. Watch out though! There are rows and rows of teeth waiting for whatever the monster devours. Good Luck Superman! The weight of the universe hangs in the balance. If you do not find a way, no one will. 
