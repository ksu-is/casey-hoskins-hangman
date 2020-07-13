import pygame
import random
import math

pygame.init()
winHeight = 680
winWidth = 700
win=pygame.display.set_mode((winWidth,winHeight))

BLACK = (0,0, 0)
WHITE = (255,255,255)
RED = (255,0, 0)
GREEN = (0,255,0)
BLUE = (0,0,255)
LIGHT_BLUE = (102,255,255)
RED = (200,0,0)

btn_font = pygame.font.SysFont("arial", 20)
guess_font = pygame.font.SysFont("monospace", 24)
lost_font = pygame.font.SysFont('arial', 45)
difficulty_font = pygame.font.SysFont('comicsansms', 32)
word = ''
buttons = []
guessed = []
hangmanPics = [pygame.image.load('hangman0.png'), pygame.image.load('hangman1.png'), pygame.image.load('hangman2.png'), pygame.image.load('hangman3.png'), pygame.image.load('hangman4.png'), pygame.image.load('hangman5.png'), pygame.image.load('hangman6.png')]
limbs = 0


def redraw_game_window():
    global guessed
    global hangmanPics
    global limbs
    win.fill(GREEN)
    # Buttons
    for i in range(len(buttons)):
        if buttons[i][4]:
            pygame.draw.circle(win, BLACK, (buttons[i][1], buttons[i][2]), buttons[i][3])
            pygame.draw.circle(win, buttons[i][0], (buttons[i][1], buttons[i][2]), buttons[i][3] - 2
                               )
            label = btn_font.render(chr(buttons[i][5]), 1, BLACK)
            win.blit(label, (buttons[i][1] - (label.get_width() / 2), buttons[i][2] - (label.get_height() / 2)))

    spaced = spacedOut(word, guessed)
    label1 = guess_font.render(spaced, 1, BLACK)
    rect = label1.get_rect()
    length = rect[2]
    
    win.blit(label1,(winWidth/2 - length/2, 400))

    pic = hangmanPics[limbs]
    win.blit(pic, (winWidth/2 - pic.get_width()/2 + 20, 150))


    hint_text = difficulty_font.render("Hint", 1, BLACK)
    win.blit(hint_text, (winWidth/2 - hint_text.get_width()/2, 470))
    pygame.draw.circle(win, BLACK, (305,493), 10, 0)

    pygame.display.update()


def randomWord(difficulty_level):
    global word
    if difficulty_level == "Easy":
        file = open('words-easy.txt')
        f = file.readlines()
        i = random.randrange(0, len(f) - 1)
        file = open('words_easy_hint.txt')
        h = file.readlines()
    elif difficulty_level == "Medium":
        file = open('words-medium.txt')
        f = file.readlines()
        i = random.randrange(0, len(f) - 1)
    else:
        file = open('words-hard.txt')
        f = file.readlines()
        i = random.randrange(0, len(f) - 1)

    return f[i][:-1]
    return h[i][:-1]


def hang(guess):
    global word
    if guess.lower() not in word.lower():
        return True
    else:
        return False


def spacedOut(word, guessed=[]):
    spacedWord = ''
    guessedLetters = guessed
    for x in range(len(word)):
        if word[x] != ' ':
            spacedWord += '_ '
            for i in range(len(guessedLetters)):
                if word[x].upper() == guessedLetters[i]:
                    spacedWord = spacedWord[:-2]
                    spacedWord += word[x].upper() + ' '
        elif word[x] == ' ':
            spacedWord += ' '
    return spacedWord
            

def buttonHit(x, y):
    for i in range(len(buttons)):
        if x < buttons[i][1] + 20 and x > buttons[i][1] - 20:
            if y < buttons[i][2] + 20 and y > buttons[i][2] - 20:
                return buttons[i][5]
    return None


def difficulty():
    win.fill(GREEN)
    global difficulty_level
    global word

    choose_difficulty = difficulty_font.render("Choose a difficulty level:",1, BLACK)
    difficulty_text_easy = difficulty_font.render("Easy", 1, BLACK)
    difficulty_text_medium = difficulty_font.render("Medium", 1, BLACK)
    difficulty_text_hard = difficulty_font.render("Hard", 1, BLACK)

    win.blit(choose_difficulty, (winWidth/2 - choose_difficulty.get_width()/2, 95))
    win.blit(difficulty_text_easy, (winWidth/2 - difficulty_text_easy.get_width()/2, 170))
    win.blit(difficulty_text_medium, (winWidth/2 - difficulty_text_medium.get_width()/2, 220))
    win.blit(difficulty_text_hard, (winWidth/2 - difficulty_text_hard.get_width()/2, 270))

    pygame.draw.circle(win, BLACK, (302,195), 10, 0)
    pygame.draw.circle(win, BLACK, (280,245), 10, 0)
    pygame.draw.circle(win, BLACK, (300,295), 10, 0)

    pygame.display.update()

    keepPlaying = True
    while keepPlaying:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepPlaying = False
                quit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                easy_check = math.sqrt((302 - m_x)**2 + (195 - m_y)**2)
                medium_check = math.sqrt((280 - m_x)**2 + (245 - m_y)**2)
                hard_check = math.sqrt((300 - m_x)**2 + (295 - m_y)**2)
                if easy_check < 10:
                    pygame.draw.circle(win, RED, (302,195), 10, 0)
                    pygame.draw.circle(win, BLACK, (280,245), 10, 0)
                    pygame.draw.circle(win, BLACK, (300,295), 10, 0)
                    pygame.display.update()
                    pygame.time.delay(1000)
                    difficulty_level = "Easy"
                    word = randomWord(difficulty_level)
                    keepPlaying = False
                elif medium_check < 10:
                    pygame.draw.circle(win, BLACK, (302,195), 10, 0)
                    pygame.draw.circle(win, RED, (280,245), 10, 0)
                    pygame.draw.circle(win, BLACK, (300,295), 10, 0)
                    pygame.display.update()
                    pygame.time.delay(1000)
                    difficulty_level = "Medium"
                    word = randomWord(difficulty_level)
                    keepPlaying = False
                elif hard_check < 10:
                    pygame.draw.circle(win, BLACK, (302,195), 10, 0)
                    pygame.draw.circle(win, BLACK, (280,245), 10, 0)
                    pygame.draw.circle(win, RED, (300,295), 10, 0)
                    pygame.display.update()
                    pygame.time.delay(1000)
                    difficulty_level = "Hard"
                    word = randomWord(difficulty_level)
                    keepPlaying = False


def end(winner=False):
    global limbs
    lostTxt = 'You Lost, press any key to play again...'
    winTxt = 'WINNER!, press any key to play again...'
    redraw_game_window()
    pygame.time.delay(1000)
    win.fill(GREEN)

    if winner == True:
        label = lost_font.render(winTxt, 1, BLACK)
    else:
        label = lost_font.render(lostTxt, 1, BLACK)

    wordTxt = lost_font.render(word.upper(), 1, BLACK)
    wordWas = lost_font.render('The phrase was: ', 1, BLACK)

    win.blit(wordTxt, (winWidth/2 - wordTxt.get_width()/2, 295))
    win.blit(wordWas, (winWidth/2 - wordWas.get_width()/2, 245))
    win.blit(label, (winWidth / 2 - label.get_width() / 2, 140))
    pygame.display.update()
    again = True
    while again:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                again = False
    reset()


def reset():
    global limbs
    global guessed
    global buttons
    global word
    for i in range(len(buttons)):
        buttons[i][4] = True

    limbs = 0
    guessed = []
    difficulty_level = ""

    difficulty()

#MAINLINE


# Setup buttons

def quit_game():
    pygame.quit()

difficulty()

increase = round(winWidth / 13)
for i in range(26):
    if i < 13:
        y = 40
        x = 25 + (increase * i)
    else:
        x = 25 + (increase * (i - 13))
        y = 85
    buttons.append([LIGHT_BLUE, x, y, 20, True, 65 + i])
    # buttons.append([color, x_pos, y_pos, radius, visible, char])

inPlay = True

while inPlay:
    redraw_game_window()
    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            inPlay = False
            quit_game()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                inPlay = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clickPos = pygame.mouse.get_pos()
            letter = buttonHit(clickPos[0], clickPos[1])
            if letter != None:
                guessed.append(chr(letter))
                buttons[letter - 65][4] = False
                if hang(chr(letter)):
                    if limbs != 5:
                        limbs += 1
                    else:
                        end()
                else:
                    print(spacedOut(word, guessed))
                    if spacedOut(word, guessed).count('_') == 0:
                        end(True)

# always quit pygame when done!