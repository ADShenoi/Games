import pygame
import random
import os

pygame.mixer.init()

pygame.init()

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)

# Creating Window
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))

# Home Screen Background Image
home_bgimg= pygame.image.load("Home_screen.jpg")
home_bgimg = pygame.transform.scale(home_bgimg, (screen_width, screen_height)).convert_alpha()

# Game Window Background Image
game_bgimg = pygame.image.load("black_grid.png")
game_bgimg = pygame.transform.scale(game_bgimg, (screen_width, screen_height)).convert_alpha()

# Game Over WIndow Background Image
over_bgimg = pygame.image.load("5.jpg")
over_bgimg = pygame.transform.scale(over_bgimg, (screen_width, screen_height)).convert_alpha()

# Game Title
pygame.display.set_caption("Snake2.0 Reloaded")
pygame.display.update()

clock = pygame.time.Clock()

#  Score Display
font = pygame.font.SysFont(None, 55)


# Display text on screen
def text_screen(text, color, x , y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text,(x,y))


# Plot snake on gamewindow
def plot_snake(gameWindow, color, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(gameWindow, (0, 255, 255), [x, y, snake_size, snake_size])


#Home Screen
def welcome():
    pygame.mixer.music.load('start.mp3')
    pygame.mixer.music.play()
    exit_game = False
    while not exit_game:

        gameWindow.blit(home_bgimg, (0, 0))
        text_screen("Welcome To Snakes 2.0 ", (255, 255, 0), 250, 250)
        text_screen("Press Enter To PLAY", green, 260, 290)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.mixer.music.load('Theme.mp3')
                    pygame.mixer.music.play()
                    game_loop()

        pygame.display.update()
        clock.tick(60)


# Game Loop
def game_loop():

    # Game specific variables
    exit_game = False

    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0

    food_x = random.randint(20, screen_width / 2)
    food_y = random.randint(20, screen_height / 2)
    score = 0
    init_velocity = 3
    snake_size = 10
    fps = 60
    distance = 6
    snk_list = []
    snk_length = 1

    #Automatic File Generation
    if not os.path.exists("highscore.txt"):
        with open("highscore.txt","w") as f:
            f.write("0")

    with open("highscore.txt", "r") as f:
        highscore = f.read()

    while not exit_game:
        if game_over:
            gameWindow.blit(over_bgimg, (0, 0))
            with open("highscore.txt", "w") as f:
                f.write(str(highscore))
            text_screen("Game Over! Press to continue", (0, 0, 55), 200, 400)
            text_screen("Your Score : " + str(score) , (0, 0, 55), 330, 440)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()

        else:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

                    # Cheat Codes
                    if event.key == pygame.K_q:        # Press 'q' to increase the score by 10
                        score += 10
                    if event.key == pygame.K_e:        # Press 'e' to decrease the accuracy of overlapping
                        distance += 2

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if score > int(highscore):
                highscore = score

            if abs(snake_x - food_x) < distance and abs(snake_y - food_y) < distance:
                score += 10
                food_x = random.randint(20, screen_width / 2)
                food_y = random.randint(20, screen_height / 2)
                snk_length += 5

            gameWindow.blit(game_bgimg, (0, 0))
            text_screen("Score :" + str(score) + " HighScore :" + str(highscore) , red, 5, 5)
            pygame.draw.rect(gameWindow, (255,20,147), [food_x, food_y, snake_size, snake_size])

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list)>snk_length:
                del(snk_list[0])
            if head in snk_list[:-1]:
                game_over = True
                pygame.mixer.music.load('Game_over.mp3')
                
                pygame.mixer.music.play()

            if(snake_x > screen_width) or (snake_y > screen_height) or (snake_x < 0) or (snake_y < 0):
                game_over = True
                pygame.mixer.music.load('Game_over.mp3')
                pygame.mixer.music.play()

            plot_snake(gameWindow, black, snk_list, snake_size)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()

    quit()


welcome()

