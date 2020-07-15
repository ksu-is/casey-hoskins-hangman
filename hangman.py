import pygame
import random
import math


#Set the initial game window settings
pygame.init()
winHeight = 650
winWidth = 700
win=pygame.display.set_mode((winWidth,winHeight))


#Set the color variables for easier reference
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0, 0)
GREY = (224,224,224)
BLUE = (0,0,255)
DARK_GREY = (128,128,128)
GREEN = (0,255,0)

#Set fonts for easier reference
btn_font = pygame.font.SysFont("comicsansms", 20)
guess_font = pygame.font.SysFont("monospace", 24)
lost_font = pygame.font.SysFont('arial', 45)
difficulty_font = pygame.font.SysFont('comicsansms', 32)


#Set initial variables required for gameplay
word = ''
buttons = []
guessed = []
hangmanPics = [pygame.image.load('hangman0.png'), pygame.image.load('hangman1.png'), pygame.image.load('hangman2.png'), pygame.image.load('hangman3.png'), pygame.image.load('hangman4.png'), pygame.image.load('hangman5.png'), pygame.image.load('hangman6.png')]
limbs = 0
hint = False
word_count = 1



#Sets the initial game board with hangman art and button placement
def redraw_game_window():
    global guessed
    global hangmanPics
    global limbs
    win.fill(GREY)
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


    if hint == True:
        hint_text = difficulty_font.render("Hint", 1, BLACK)
        win.blit(hint_text, (winWidth/2 - hint_text.get_width()/2, 470))
        pygame.draw.circle(win, GREEN, (305,493), 10, 0)
        give_hint = difficulty_font.render(hint_str, 1, BLACK)
        win.blit(give_hint, (winWidth/2 - give_hint.get_width()/2, 520))
    else:
        hint_text = difficulty_font.render("Hint", 1, BLACK)
        win.blit(hint_text, (winWidth/2 - hint_text.get_width()/2, 470))
        pygame.draw.circle(win, BLACK, (305,493), 10, 0)

    pygame.display.update()

#Selects a random word based on the difficulty level the user selected
def randomWord(difficulty_level):
    global word
    global hint_str
    global unending_word
    global unending_list
    global word_count

    if difficulty_level == "Easy":
        file = open('words-easy.txt')
        f = file.readlines()
        i = random.randrange(0, len(f) - 1)
        file = open('words_easy_hint.txt')
        h = file.readlines()
        hint_str = h[i][:-1]
        return f[i][:-1]
    elif difficulty_level == "Medium":
        file = open('words-medium.txt')
        f = file.readlines()
        i = random.randrange(0, len(f) - 1)
        file = open('words-medium-hint.txt')
        h = file.readlines()
        hint_str = h[i][:-1]
        return f[i][:-1]
    elif difficulty_level == "Hard":
        file = open('words-hard.txt')
        f = file.readlines()
        i = random.randrange(0, len(f) - 1)
        file = open('words-hard-hint.txt')
        h = file.readlines()
        hint_str = h[i][:-1]
        return f[i][:-1]
    elif difficulty_level == "unending" and word_count == 1:
        file = open('words-hard.txt')
        f = file.readlines()
        unending_list = list(f)
        i = random.randrange(0, len(unending_list) - 1)
        word_count = 2
        return unending_list[i][:-1]
    elif difficulty_level == "unending" and word_count == 2:
        unending_list.remove(unending_word + "\n")
        i = random.randrange(0, len(unending_list) - 1)
        return unending_list[i][:-1]


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
            
#Registers the letter selection
def buttonHit(x, y):
    for i in range(len(buttons)):
        if x < buttons[i][1] + 20 and x > buttons[i][1] - 20:
            if y < buttons[i][2] + 20 and y > buttons[i][2] - 20:
                return buttons[i][5]
    return None

#Gives the user three difficulty options to choose from
def difficulty():
    win.fill(GREY)
    global difficulty_level
    global word

    choose_difficulty = difficulty_font.render("Choose a difficulty level:",1, BLACK)
    difficulty_text_easy = difficulty_font.render("Easy", 1, BLACK)
    difficulty_text_medium = difficulty_font.render("Medium", 1, BLACK)
    difficulty_text_hard = difficulty_font.render("Hard", 1, BLACK)
    difficulty_text_unending = difficulty_font.render("Unending", 1, BLACK)

    win.blit(choose_difficulty, (winWidth/2 - choose_difficulty.get_width()/2, 95))
    win.blit(difficulty_text_easy, (winWidth/2 - difficulty_text_easy.get_width()/2, 170))
    win.blit(difficulty_text_medium, (winWidth/2 - difficulty_text_medium.get_width()/2, 220))
    win.blit(difficulty_text_hard, (winWidth/2 - difficulty_text_hard.get_width()/2, 270))
    win.blit(difficulty_text_unending, (winWidth/2 - difficulty_text_unending.get_width()/2, 310))

    pygame.draw.circle(win, BLACK, (302,195), 10, 0)
    pygame.draw.circle(win, BLACK, (280,245), 10, 0)
    pygame.draw.circle(win, BLACK, (300,295), 10, 0)
    pygame.draw.circle(win, BLACK, (270,335), 10, 0)

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
                unending_check = math.sqrt((270 - m_x)**2 + (335 - m_y)**2)

                if easy_check < 10:
                    pygame.draw.circle(win, GREEN, (302,195), 10, 0)
                    pygame.draw.circle(win, BLACK, (280,245), 10, 0)
                    pygame.draw.circle(win, BLACK, (300,295), 10, 0)
                    pygame.draw.circle(win, BLACK, (270,335), 10, 0)
                    pygame.display.update()
                    pygame.time.delay(1000)
                    difficulty_level = "Easy"
                    word = randomWord(difficulty_level)
                    keepPlaying = False
                    play_game()
                elif medium_check < 10:
                    pygame.draw.circle(win, BLACK, (302,195), 10, 0)
                    pygame.draw.circle(win, GREEN, (280,245), 10, 0)
                    pygame.draw.circle(win, BLACK, (300,295), 10, 0)
                    pygame.draw.circle(win, BLACK, (270,335), 10, 0)
                    pygame.display.update()
                    pygame.time.delay(1000)
                    difficulty_level = "Medium"
                    word = randomWord(difficulty_level)
                    keepPlaying = False
                    play_game()
                elif hard_check < 10:
                    pygame.draw.circle(win, BLACK, (302,195), 10, 0)
                    pygame.draw.circle(win, BLACK, (280,245), 10, 0)
                    pygame.draw.circle(win, GREEN, (300,295), 10, 0)
                    pygame.draw.circle(win, BLACK, (270,335), 10, 0)
                    pygame.display.update()
                    pygame.time.delay(1000)
                    difficulty_level = "Hard"
                    word = randomWord(difficulty_level)
                    keepPlaying = False
                    play_game()
                elif unending_check < 10:
                    pygame.draw.circle(win, BLACK, (302,195), 10, 0)
                    pygame.draw.circle(win, BLACK, (280,245), 10, 0)
                    pygame.draw.circle(win, BLACK, (300,295), 10, 0)
                    pygame.draw.circle(win, GREEN, (270,335), 10, 0)
                    pygame.display.update()
                    pygame.time.delay(1000)
                    difficulty_level = "unending"
                    word = randomWord(difficulty_level)
                    keepPlaying = False
                    play_game()

def difficulty_level_unending():
    reset()

#End game screen that tells the user if they won or lost and gives the correct word
def end(winner=False):
    global limbs
    global wordWas
    global unending_word
    lostTxt = 'You Lost, press any key to play again...'
    winTxt = 'WINNER!, press any key to play again...'
    unending_word = word
    redraw_game_window()
    pygame.time.delay(1000)
    win.fill(GREY)

    if winner == True and difficulty_level == "unending":
        difficulty_level_unending()
    else:
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

#After the game is over, resets variables for the next game
def reset():
    global limbs
    global guessed
    global buttons
    global word
    global hint
    global difficulty_level
    for i in range(len(buttons)):
        buttons[i][4] = True

    limbs = 0
    guessed = []
    buttons = []
    hint = False
    if difficulty_level == "unending":
        word = randomWord(difficulty_level)
        play_game()
    else:
        difficulty_level = ""
        word = ""

# Setup buttons

def quit_game():
    pygame.quit()

def play_game():
    global limbs
    global hint
    global word

    increase = round(winWidth / 13)
    for i in range(26):
        if i < 13:
            y = 40
            x = 25 + (increase * i)
        else:
            x = 25 + (increase * (i - 13))
            y = 85
        buttons.append([DARK_GREY, x, y, 20, True, 65 + i])
        # buttons.append([color, x_pos, y_pos, radius, visible, char])


    #Registers the mouse events and checks after each guess if the word has been guessed or the user is out of guesses.  
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
                m_x, m_y = pygame.mouse.get_pos()
                hint_check = math.sqrt((305 - m_x)**2 + (493 - m_y)**2)
                if hint_check < 10:
                    hint = True
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

difficulty()