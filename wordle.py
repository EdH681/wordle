import pygame
import copy
from random import choice

dimensions = width, height = 1000, 700

pygame.init()
win = pygame.display.set_mode((width, height))

file = open('words.dat', 'r+')
words = []

for word in file:
    word = word.replace('\n','')
    words.append(word)

ans = open('answers.dat', 'r+')
accepted = []
for word in ans:
    word = word.replace('\n', '')
    accepted.append(word)
    accepted = (accepted[0].split())


size = 50
running = True
string = ''
characters = []
attempts = []
performance = []
used = [*'00000000000000000000000000']
line = 0
typable = True
font = pygame.font.SysFont('arial', round(0.9*size), True)
endFont = pygame.font.SysFont('arial', round(height/15), True)
url = 'https://www.thefreedictionary.com/hello'
alphabet = [*'qwertyuiopasdfghjklzxcvbnm']
passed = False
done = False
colours = [(64, 64, 64), (255, 214, 75), (0, 172, 23)]
x = 0
y = 0

word = choice(accepted).lower()


def text_display(blank, layer, size):
    letters = blank
    for i in range(len(letters)):
        text = font.render(letters[i].upper(), True, 'white')
        textRect = text.get_rect()
        textRect.center = ((width/2-(size*2.5))+(i*size)+(size/2), (height/25)+(layer*size)+(size/2))
        win.blit(text, textRect)


def history(previous, size):
    if len(previous) >= 1:
        for y in range(len(previous)):
            for x in range(len(previous[y])):
                text = font.render(previous[y][x].upper(), True, 'white')
                textRect = text.get_rect()
                textRect.center = ((width/2-(size*2.5))+(x*size)+(size/2), (height/25)+(y*size)+(size/2))
                win.blit(text, textRect)


def draw_empty(x, y, size, width):
    colour = (64, 64, 64)
    pygame.draw.rect(win, colour, ((width/2-(size*2.5))+x+1, (height/25)+y+1, size-2, size-2), 2)


def letter_check(result, target):
    positions = []
    target = [*target]
    global used, alphabet

    for r in range(len(result)):
        temp = []
        to_find = copy.deepcopy(target)
        for i in range(5):
            target = target
            found = False
            if result[r][i] in target:

                # green
                if target[i] == result[r][i] and target[i] in to_find and not found:
                    temp.append(2)
                    to_find.remove(result[r][i])
                    found = True
                    alphabet_position = alphabet.index(result[r][i])
                    used[alphabet_position] = 3

                # yellow
                if target[i] != result[r][i] and result[r][i] in to_find and not found:
                    temp.append(1)
                    to_find.remove(result[r][i])
                    found = True
                    alphabet_position = alphabet.index(result[r][i])
                    used[alphabet_position] = 2

                # grey (already found)
                if result[r][i] not in to_find and not found:
                    temp.append(0)

            # grey (not in word)
            else:
                temp.append(0)
                alphabet_position = alphabet.index(result[r][i])
                used[alphabet_position] = 1

        positions.append(temp)
    return positions


def fill_results(structure, colour_select):
    for y in range(len(structure)):
        for x in range(5):

            colour = colour_select[structure[y][x]]
            pygame.draw.rect(win, colour, ((width/2-(size*2.5))+(x*size)+1, (height/25)+(y*size)+1, size-2, size-2))


def combine(expanded):
    combined = ''
    for i in expanded:
        combined += i
    return combined


def availability(x, y, colour_value, size, words, position):
    global characters
    clickable = True

    colour = int(colour_value[position])
    box = pygame.draw.rect(win, 'black', (0, 0, 0, 0))

    if colour == 0:
        box = pygame.draw.rect(win, (64, 64, 64), (x, y, size, size), 2)
    if colour == 1:
        box = pygame.draw.rect(win, (64, 64, 64), (x, y, size, size))
    if colour == 2:
        box = pygame.draw.rect(win, (255, 214, 75), (x, y, size, size))
    if colour == 3:
        box = pygame.draw.rect(win, (0, 172, 23), (x, y, size, size))

    text = font.render(words.upper(), True, 'white')
    textRect = text.get_rect()
    textRect.center = (x + (size/2), y + (size/2))
    win.blit(text, textRect)




while running:

    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:
            keyNum = event.key

            # letters
            if 97 <= keyNum <= 122 and typable:
                if len(characters) < 5:
                    characters.append(chr(keyNum))

            # enter
            if (keyNum == 13 or keyNum == 1073741912) and len(characters) == 5:
                entire_word = combine(characters)
                if entire_word in words:
                    if line <= 4:
                        line += 1
                    else:
                        typable = False
                        done = True

                    attempts.append(characters)
                    characters = []
                    performance = letter_check(attempts, word)
            # backspace
            if keyNum == 8 and len(characters) >= 1:
                characters.pop(len(characters)-1)

            # reveal
            if keyNum == 1073742048:
                print(word)

        win.fill('black')

        for x in range(5):
            for y in range(6):
                draw_empty(x * size, y * size, size, width)

        fill_results(performance, colours)

        history(attempts, size)

        text_display(characters, line, size)

        for i in range(26):
            if i < 10:
                y = 0.6*height
                x = (width/2) - (size*5) + (i*size)
            if 10 <= i < 19:
                y = (0.6*height) + size + 1
                x = (width / 2) - (size * 4.5) + ((i-10) * size)
            if i >= 19:
                y = (0.6*height) + (size*2) + 2
                x = (width / 2) - (size * 3.5) + ((i-19) * size)
            availability(x, y, used, size, alphabet[i], i)

        if len(performance) >= 1 and performance[-1] == [2, 2, 2, 2, 2]:
            typable = False
            passed = True

        if passed:
            text = endFont.render('CORRECT', True, 'green')
            textRect = text.get_rect()
            textRect.center = (width/2, height*0.53)
            win.blit(text, textRect)

        if done and not passed:
            text = endFont.render(f'THE WORD IS: {word.upper()}', True, 'red')
            textRect = text.get_rect()
            textRect.center = (width / 2, height * 0.53)
            win.blit(text, textRect)

        pygame.display.update()
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
