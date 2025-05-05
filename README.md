# COMP-61-2025 Game Design README
Alek Newman
## Demo Video:
(https://youtu.be/izRT6_KZCao)
## Setup:
import pygame
import random
from PIL import Image  # Import Pillow to handle GIFs

# Initialize pygame and the mixer module for sounds
pygame.init()
pygame.mixer.init()  # Initialize the mixer module for sound

# Screen setup
WIDTH, HEIGHT = 800, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Superman and the Jaws of Death")

# Colors and font
WHITE, BLUE, BLACK, DARK_GRAY = (255, 255, 255), (50, 150, 255), (0, 0, 0), (169, 169, 169)
font = pygame.font.SysFont(None, 48)

# Clock and FPS
clock = pygame.time.Clock()
FPS = 60

# Load background image (make sure the path is correct)
start_page_background = pygame.image.load('start_page_background.png')  # Ensure correct file path
start_page_background = pygame.transform.scale(start_page_background, (WIDTH, HEIGHT))  # Scale to fit the screen

# Load player ball image (replace 'player_ball.jpeg' with your actual image file)
player_ball_img = pygame.image.load('player_ball.jpeg')
player_ball_img = pygame.transform.scale(player_ball_img, (40, 40))  # Scale it to the size of the ball

# Load heart image (for win condition)
heart_img = pygame.image.load('heart.png')  # Provide the correct path
heart_img = pygame.transform.scale(heart_img, (500, 500))  # Resize as needed

# Splash screen animation parameters
splash_title_text = "Super Man and the Jaws of Death"
splash_name_text = "By Alek Newman"
fade_speed = 100  # Controls the fade speed of the text

# Load the GIF and extract frames using Pillow
def load_gif_frames(gif_path):
    img = Image.open(gif_path)  # Open the GIF file
    frames = []
    try:
        while True:
            frame = img.copy()
            frames.append(pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode))
            img.seek(img.tell() + 1)  # Go to the next frame
    except EOFError:
        pass  # End of frames in GIF
    return frames

# Load GIF frames for animation
gif_frames = load_gif_frames('explode_gif.gif')  # Replace with the path to your GIF
gif_frame_count = len(gif_frames)

# Player class
class Player:
    def __init__(self):
        self.x, self.y = 100, HEIGHT // 2
        self.radius = 20
        self.velocity, self.gravity, self.lift = 0, 0.5, -10

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity
        if self.y > HEIGHT - self.radius: self.y, self.velocity = HEIGHT - self.radius, 0
        if self.y < self.radius: self.y, self.velocity = self.radius, 0

    def jump(self):
        self.velocity = self.lift

    def draw(self):
        screen.blit(player_ball_img,
                    (self.x - player_ball_img.get_width() // 2, self.y - player_ball_img.get_height() // 2))

# Function to start playing background music
def start_background_music():
    pygame.mixer.music.load('beast_background.mp3')  # Load the music (ensure the path is correct)
    pygame.mixer.music.play(-1)  # Play music indefinitely (-1 means loop forever)
    pygame.mixer.music.set_volume(0.5)  # Set the volume (0.0 to 1.0)

# Pipe class with monster teeth
class Pipe:
    def __init__(self, speed):  # Now accepts the speed as an argument
        self.width, self.gap, self.x = 80, 200, WIDTH
        self.top = random.randint(50, HEIGHT - self.gap - 50)
        self.bottom = self.top + self.gap
        self.speed = speed  # Assign the speed passed as argument

    def update(self):
        self.x -= self.speed

    def draw(self):
        # Draw top triangle (white)
        points_top = [(self.x, 0), (self.x + self.width // 2, self.top), (self.x + self.width, 0)]
        pygame.draw.polygon(screen, WHITE, points_top)

        # Draw bottom triangle (white)
        points_bottom = [(self.x, self.bottom), (self.x + self.width // 2, self.bottom - self.gap),
                         (self.x + self.width, self.bottom)]
        pygame.draw.polygon(screen, WHITE, points_bottom)

        # Draw the pipe parts (colored sections)
        pygame.draw.rect(screen, (120, 120, 120), (self.x, 0, self.width, self.top))
        pygame.draw.rect(screen, (150, 150, 150), (self.x, self.bottom, self.width, HEIGHT - self.bottom))

    def off_screen(self):
        return self.x + self.width < 0

    def hits(self, player):
        return (player.x + player.radius > self.x and player.x - player.radius < self.x + self.width) and (
                player.y - player.radius < self.top or player.y + player.radius > self.bottom)


# Function to wrap text into multiple lines if it exceeds the screen width
def wrap_text(text, font, max_width):
    lines = []
    words = text.split(' ')
    current_line = ""

    for word in words:
        # Add word to current line and check if the width exceeds max_width
        test_line = current_line + ' ' + word if current_line else word
        test_width, _ = font.size(test_line)
        if test_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    # Add the last line
    if current_line:
        lines.append(current_line)

    return lines

pipe_pass_sound = pygame.mixer.Sound('5th_pipe_roar.mp3')  # Make sure the sound file path
pipe_pass_sound_2 = pygame.mixer.Sound('10th_pipe_roar.mp3')  # Make sure the sound file path

# Main game function
def game():
    start_background_music()  # Start background music when the game starts
    player, pipes = Player(), []
    score, level, frame_count, pipe_speed, passed_pipes = 0, 1, 0, 4, 0  # Added passed_pipes to count passed pipes
    game_over, game_paused = False, False
    heart_shown = False  # Flag to track if the heart is shown
    heart_position = None  # Store the heart's position once it should appear
    gif_frame_index = 0  # To track the current frame of the GIF

    while True:
        clock.tick(FPS)

        # Draw background
        screen.blit(start_page_background, (0, 0))  # Ensure the background is drawn here

        # Display GIF near the heart (when it is shown)
        if heart_shown:
            # Display the current GIF frame near the heart
            gif_frame = gif_frames[gif_frame_index]  # Get the current GIF frame
            gif_frame_rect = gif_frame.get_rect(center=(heart_position[0] + heart_img.get_width() // 2, heart_position[1]))
            screen.blit(gif_frame, gif_frame_rect)

            # Update the GIF frame every few ticks to animate it
            gif_frame_index = (gif_frame_index + 1) % len(gif_frames)  # Loop through frames

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    player.jump()
                if event.key == pygame.K_p:  # Pause the game
                    game_paused = True
                if event.key == pygame.K_r and game_over:  # Restart game
                    game()
                if event.key == pygame.K_m and game_over:  # Go to main menu
                    show_main_menu()

        if game_paused:
            show_pause_menu()
            continue  # Skip game logic to keep the game paused

        if not game_over:
            player.update()
            frame_count += 1

            # Add pipes to the game
            if frame_count % 90 == 0 and not heart_shown:  # Only add pipes if heart hasn't appeared
                pipes.append(Pipe(pipe_speed))  # Pass pipe_speed to the Pipe constructor

            for pipe in pipes:
                pipe.update()
                pipe.draw()
                if pipe.hits(player):
                    game_over = True  # End the game if player hits pipe

                # Increment score if the player successfully passes a pipe
                if pipe.x + pipe.width < player.x and not getattr(pipe, 'scored', False):
                    score += 1  # Increase score when passing the pipe
                    passed_pipes += 1  # Increment the count of passed pipes
                    pipe.scored = True  # Mark the pipe as scored

                    # Play sound every 5th pipe passed
                    if passed_pipes % 5 == 0:
                        pipe_pass_sound.play()

                    if passed_pipes % 10 == 0:
                        pipe_pass_sound_2.play()

                    # Every 5th pipe passed, increase the level
                    if passed_pipes % 5 == 0:
                        level += 1
                        pipe_speed += 0.1  # Optionally, increase pipe speed for more difficulty

            pipes = [pipe for pipe in pipes if not pipe.off_screen()]

            # Show the heart after the 50th pipe
            if score >= 27 and not heart_shown:
                heart_shown = True
                heart_position = (
                    WIDTH + 200, HEIGHT // 1.3 - heart_img.get_height() // 2)  # Set heart position off-screen initially

            # Display the heart once it's time to show it
            if heart_shown:
                heart_position = (heart_position[0] - 5, heart_position[1])  # Move the heart leftwards
                heart_rect = heart_img.get_rect(center=heart_position)
                screen.blit(heart_img, heart_rect)

                # If the player flies into the heart (win condition)
                if heart_rect.colliderect(
                        pygame.Rect(player.x - player.radius, player.y - player.radius, player.radius * 2,
                                    player.radius * 2)):
                    display_win_message()  # Show win message and go to the win screen
                    game_over = True  # End the game when the player hits the heart

        player.draw()

        # Red text for the score
        score_text = font.render(f"Score: {score}", True, (255, 0, 0))  # Red
        # Blue text for the level
        level_text = font.render(f"Level: {level}", True, (0, 0, 255))  # Blue

        screen.blit(score_text, (10, 10))  # Draw score in the top-left corner
        screen.blit(level_text, (WIDTH - level_text.get_width() - 10, 10))  # Draw level in the top-right corner

        # Game over text in white
        if game_over:
            over_text = font.render("Game Over! Press R to Restart or M for Menu", True, (255, 255, 255))  # White
            screen.blit(over_text, over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))

        pygame.display.update()




def display_win_message():
    # Text for the win message
    win_message = "You Killed It!!! You flew through the heart and killed the Beast!!! You have just saved the Universe and us all! You have the mark of a true Hero! Press R to Restart or M for Menu"

    # Wrap the text to fit the screen
    wrapped_text = wrap_text(win_message, font, WIDTH - 40)  # Add some padding to avoid text cut off

    # Create the red win text
    win_text = [font.render(line, True, (255, 0, 0)) for line in wrapped_text]  # Red text

    # Load the medal icon (make sure the path is correct)
    medal_icon = pygame.image.load('medal_icon.png')  # Replace with the correct path
    medal_icon = pygame.transform.scale(medal_icon, (500, 500))  # Scale to desired size

    # Load the sound (replace with the correct path to your sound file)
    sound_effect = pygame.mixer.Sound('explosion.wav')  # Load the sound effect for going through the heart

    # Play the sound effect
    sound_effect.play()

    # Clear the screen and display the win message
    screen.fill(WHITE)

    # Position the icon above the win message
    icon_position = (WIDTH // 2 - medal_icon.get_width() // 2, HEIGHT // 2 - medal_icon.get_height() // 2)
    screen.blit(medal_icon, icon_position)

    # Draw the wrapped text on the screen
    y_position = HEIGHT // 3  # Start from the top third of the screen, adjust after the icon
    for line in win_text:
        screen.blit(line, (WIDTH // 2 - line.get_width() // 2, y_position))
        y_position += line.get_height() + 5  # Move down with a small margin between lines

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game()  # Restart the game
                elif event.key == pygame.K_m:  # Press 'M' to go back to the main menu
                    show_main_menu()  # Go to the main menu

# Function to display the splash screen with a fade-in effect for the image
def show_splash_screen():
    # Create a new window for the splash screen
    splash_screen = pygame.display.set_mode((WIDTH, HEIGHT))  # New window for splash screen
    splash_screen.fill(WHITE)

    # Load and scale your image (replace 'your_image.png' with the path to your actual image)
    splash_image = pygame.image.load('splash_page.png')  # Provide the correct path to the image
    splash_image = pygame.transform.scale(splash_image, (WIDTH // 2, HEIGHT // 3))  # Resize the image to fit the screen

    # Position the image at the top center of the screen
    image_x = WIDTH // 2 - splash_image.get_width() // 2  # Center the image horizontally
    image_y = HEIGHT // 6  # Position the image slightly below the top of the screen

    # Create a bigger font for the splash screen
    title_font = pygame.font.SysFont(None, 100)  # Set a larger font size for the title
    name_font = pygame.font.SysFont(None, 48)  # Set a slightly smaller font for the author name

    # Create the title and name texts with the new font size
    title_text = title_font.render("Superman and the Jaws of Death", True, (255, 0, 0))  # Red text for the title
    name_text = name_font.render("By Alek Newman", True, (0, 0, 0))  # Black text for the author's name

    # Ensure title and name fit within the screen
    # If the title is too long, reduce the font size
    max_title_width = WIDTH - 40  # Give some padding
    if title_text.get_width() > max_title_width:
        while title_text.get_width() > max_title_width:
            title_font = pygame.font.SysFont(None, title_font.get_height() - 5)
            title_text = title_font.render("Superman and the Jaws of Death", True, (255, 0, 0))

    # If the name is too long, adjust the font size for the author's name
    if name_text.get_width() > max_title_width:
        while name_text.get_width() > max_title_width:
            name_font = pygame.font.SysFont(None, name_font.get_height() - 5)
            name_text = name_font.render("By Alek Newman", True, (0, 0, 0))

    # Display the image on the screen
    splash_screen.blit(splash_image, (image_x, image_y))

    # Adjust positioning of the text based on the image and text sizes
    title_y = image_y + splash_image.get_height() + 10  # Position title text below the image
    name_y = title_y + title_text.get_height() + 10  # Position name text below the title

    # Display the title and name text
    splash_screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, title_y))
    splash_screen.blit(name_text, (WIDTH // 2 - name_text.get_width() // 2, name_y))

    # Fade-in effect for the image
    fade_in_speed = 1  # How quickly the image fades in
    alpha = 0  # Start with the image fully transparent

    # Gradually increase the alpha (opacity) of the image
    for i in range(0, 256, fade_in_speed):
        alpha = i
        splash_image.set_alpha(alpha)  # Set the alpha value of the image
        splash_screen.fill(WHITE)  # Clear the screen
        splash_screen.blit(splash_image, (image_x, image_y))  # Re-render the image with updated alpha
        splash_screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, title_y))  # Re-render title
        splash_screen.blit(name_text, (WIDTH // 2 - name_text.get_width() // 2, name_y))  # Re-render name text
        pygame.display.update()  # Update the screen
        pygame.time.wait(10)  # Wait a short time before increasing alpha again

    # Wait for 3 seconds (3000 milliseconds) before transitioning to the main menu
    pygame.time.wait(3000)

    # Transition to the main menu
    show_main_menu()



# Function to display the main menu
def show_main_menu():
    screen.blit(start_page_background, (0, 0))  # Draw the background image

    # Split the welcome text into two parts with the new title
    welcome_text_line1 = font.render("Greetings! Welcome to", True, (255, 0, 0))  # Red text
    welcome_text_line2 = font.render("Superman and the Jaws of Death!", True, (0, 0, 255))  # Blue text

    # Position the text on two separate lines
    screen.blit(welcome_text_line1, (WIDTH // 2 - welcome_text_line1.get_width() // 2, HEIGHT // 4))
    screen.blit(welcome_text_line2,
                (WIDTH // 2 - welcome_text_line2.get_width() // 2, HEIGHT // 4 + welcome_text_line1.get_height()))

    # Menu options
    play_text = font.render("Start Game", True, (255, 255, 255))  # White text
    mission_task_text = font.render("Mission Task", True, (255, 0, 0))  # Red text
    instructions_text = font.render("Instructions", True, (0, 0, 255))  # Blue text
    quit_text = font.render("Quit Game", True, (255, 255, 255))  # White text

    # Position the menu text
    screen.blit(play_text, (WIDTH // 2 - play_text.get_width() // 2, HEIGHT // 2 - 100))
    screen.blit(mission_task_text, (WIDTH // 2 - mission_task_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(instructions_text, (WIDTH // 2 - instructions_text.get_width() // 2, HEIGHT // 2))
    screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 50))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Start Game Button
                if WIDTH // 2 - play_text.get_width() // 2 < mouse_x < WIDTH // 2 + play_text.get_width() // 2 and \
                        HEIGHT // 2 - 100 < mouse_y < HEIGHT // 2 - 50:
                    game()

                # Mission Task Button
                if WIDTH // 2 - mission_task_text.get_width() // 2 < mouse_x < WIDTH // 2 + mission_task_text.get_width() // 2 and \
                        HEIGHT // 2 - 50 < mouse_y < HEIGHT // 2:
                    show_mission_task()

                # Instructions Button
                if WIDTH // 2 - instructions_text.get_width() // 2 < mouse_x < WIDTH // 2 + instructions_text.get_width() // 2 and \
                        HEIGHT // 2 < mouse_y < HEIGHT // 2 + 50:
                    show_instructions()

                # Quit Game Button
                if WIDTH // 2 - quit_text.get_width() // 2 < mouse_x < WIDTH // 2 + quit_text.get_width() // 2 and \
                        HEIGHT // 2 + 50 < mouse_y < HEIGHT // 2 + 100:
                    pygame.quit()
                    exit()



def show_mission_task():
    screen.fill(WHITE)

    # Load the alarm icon (make sure the path is correct)
    alarm_icon = pygame.image.load('alarm.png')  # Replace with the correct path
    alarm_icon = pygame.transform.scale(alarm_icon, (100, 100))  # Scale to desired size

    # Position the icon in the middle and at the very top of the screen
    icon_position = (WIDTH // 2 - alarm_icon.get_width() // 2, 20)  # 10 pixels from the top

    # Draw the alarm icon at the top
    screen.blit(alarm_icon, icon_position)

    # Mission task text
    mission_text = (
        "The Universe is threatened by an intergalactic monster called 'Death'. He devours planets and is coming straight for Earth. "
        "The humans call upon Superman to save them. This is no easy task for Superman however. He is stuck in a block of ice and "
        "he must go straight into the belly of the beast and fly through the heart to kill it. Watch out though! There are rows and "
        "rows of teeth waiting for whatever the monster devours. They say the heart is just after the 30th tooth. Good Luck Superman! The weight of the universe hangs in the balance. "
        "If you do not find a way, no one will."
    )

    # Max width for the wrapped text
    max_width = WIDTH - 40  # Leave a little padding

    # Wrap the text
    lines = wrap_text(mission_text, font, max_width)

    # Render the wrapped text and draw each line
    y_position = HEIGHT // 5  # Start from the top quarter of the screen
    for line in lines:
        mission_task_text = font.render(line, True, BLACK)
        screen.blit(mission_task_text, (WIDTH // 2 - mission_task_text.get_width() // 2, y_position))
        y_position += mission_task_text.get_height() + 5  # Move to the next line with a small margin

    # Display "Back to Menu" option below the mission text
    back_to_menu_text = font.render("Back to Menu", True, BLACK)
    back_to_menu_rect = back_to_menu_text.get_rect(center=(WIDTH // 2, HEIGHT - 16))  # Adjust position to the bottom
    screen.blit(back_to_menu_text, back_to_menu_rect)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Check if the click is within the "Back to Menu" button
                if back_to_menu_rect.collidepoint(mouse_x, mouse_y):
                    show_main_menu()  # Go back to the main menu



    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if WIDTH // 2 - back_to_menu_text.get_width() // 2 < mouse_x < WIDTH // 2 + back_to_menu_text.get_width() // 2 and \
                        HEIGHT // 2 + 100 < mouse_y < HEIGHT // 2 + 150:
                    show_main_menu()


# Function to display instructions
def show_instructions():
    screen.fill(WHITE)

    # Instructions text
    instructions_text = "Continuously press SPACE to fly through the air and go through the teeth!"

    # Wrap the instructions text to fit the screen
    wrapped_instructions = wrap_text(instructions_text, font, WIDTH - 40)  # Wrap text to fit within the screen width, leaving padding

    # Render each line of the wrapped text
    y_position = HEIGHT // 4  # Start from the top quarter of the screen
    for line in wrapped_instructions:
        instruction_line = font.render(line, True, BLACK)
        screen.blit(instruction_line, (WIDTH // 2 - instruction_line.get_width() // 2, y_position))
        y_position += instruction_line.get_height() + 5  # Move to the next line with a small margin between lines

    # Display "Back to Menu" option below the instructions
    back_to_menu_text = font.render("Back to Menu", True, BLACK)
    back_to_menu_rect = back_to_menu_text.get_rect(center=(WIDTH // 2, HEIGHT - 100))  # Adjust position to the bottom
    screen.blit(back_to_menu_text, back_to_menu_rect)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Check if the click is within the "Back to Menu" button
                if back_to_menu_rect.collidepoint(mouse_x, mouse_y):
                    show_main_menu()  # Go back to the main menu



# Start the game with the splash screen
show_splash_screen()
pygame.quit()

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
