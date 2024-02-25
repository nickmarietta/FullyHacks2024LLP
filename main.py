import pygame, sys
import random
from button import Button

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("El Aprendizaje")

BG = pygame.image.load("neon2.jpg")
PLAYBG = pygame.image.load("PLAY.jpg")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font(None, size)

def spec_font(size):
    return pygame.font.Font('blippo.ttf', size)

def start_matching_game():
    # Game setup
    SCREEN.fill("White")
    running = True

    # Example word pairs
    word_pairs = [("Hello", "Hola"), ("Goodbye", "Adiós"), ("Thank you", "Gracias")]
    english_words = [pair[0] for pair in word_pairs]
    spanish_words = [pair[1] for pair in word_pairs]
    all_words = english_words + spanish_words
    random.shuffle(all_words)

    # Positions and sizes for words
    word_boxes = []
    font = get_font(30)
    for index, word in enumerate(all_words):
        x = 100 + (index % 3) * 400  # Three columns of words
        y = 100 + (index // 3) * 100  # Row based on the word index
        text_surface = font.render(word, True, "Black")
        rect = text_surface.get_rect(center=(x, y))
        word_boxes.append((word, rect))

    selected_words = []

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for word, rect in word_boxes:
                    if rect.collidepoint(event.pos):
                        selected_words.append(word)
                        if len(selected_words) == 2:
                            # Check for match
                            if selected_words[0] in english_words and selected_words[1] in spanish_words and english_words.index(selected_words[0]) == spanish_words.index(selected_words[1]):
                                # Match found, remove words
                                all_words.remove(selected_words[0])
                                all_words.remove(selected_words[1])
                            selected_words = []
                            # Recreate word_boxes without matched words
                            word_boxes = [(word, rect) for word, rect in word_boxes if word in all_words]

        SCREEN.fill("white")
        for word, rect in word_boxes:
            text_surface = font.render(word, True, "Black")
            SCREEN.blit(text_surface, rect)

        pygame.display.update()

def play():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(PLAYBG, (0, 0))

        PLAY_TEXT = pygame.image.load("gamemodelogo.png")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 60))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        # matching button
        MATCH_BUTTON = Button(image=None, pos=(213, 630), 
                            text_input="Matching", font=spec_font(70), base_color="White", hovering_color="Green")

        MATCH_BUTTON.changeColor(PLAY_MOUSE_POS)
        MATCH_BUTTON.update(SCREEN)

        # listen button
        LISTEN_BUTTON = Button(image=None, pos=(639, 630), 
                            text_input="Listen", font=spec_font(70), base_color="White", hovering_color="Green")

        LISTEN_BUTTON.changeColor(PLAY_MOUSE_POS)
        LISTEN_BUTTON.update(SCREEN)

        # back button
        PLAY_BACK = Button(image=None, pos=(1065, 630), 
                            text_input="Back", font=spec_font(70), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()
                elif MATCH_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    start_matching_game()

        pygame.display.update()
    
def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MAIN_MENU = Button(image=pygame.image.load("titlelogo.png"), pos=(640, 100), 
                            text_input="", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        PLAY_BUTTON = Button(image=pygame.image.load("playlogo.png"), pos=(640, 250), 
                            text_input="", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("optionsnew.png"), pos=(640, 400), 
                            text_input="", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("exit.png"), pos=(640, 550), 
                            text_input="", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        # SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [MAIN_MENU,PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()