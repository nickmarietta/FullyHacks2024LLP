import os, pygame, sys, tempfile
import random
from button import Button
from gtts import gTTS 

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("El Aprendizaje")

BG = pygame.image.load("neon2.jpg")
PLAYBG = pygame.image.load("PLAY.jpg")
LISTENBG = pygame.image.load("neoncity.jpg")
MATCHBG = pygame.image.load("neonrain2.jpg")

def get_font(size):
    return pygame.font.Font(None, size)

def spec_font(size):
    return pygame.font.Font('blippo.ttf', size)

current_game_state = "play"
def start_matching_game():
    # Game setup
    global current_game_state

    running = True

    word_pairs = [("Hello", "Hola"), ("Goodbye", "Adiós"), ("Thank you", "Gracias")]
    english_words = [pair[0] for pair in word_pairs]
    spanish_words = [pair[1] for pair in word_pairs]
    all_words = english_words + spanish_words
    random.shuffle(all_words)

    word_boxes = []
    font = get_font(50)
    box_color = (0, 0, 0, 0)
    text_color = "white"
    padding = 0 
    outline_width = 0

    for index, word in enumerate(all_words):
        x = 100 + (index % 3) * 400
        y = 100 + (index // 3) * 100
        text_surface = font.render(word, True, text_color)
        text_rect = text_surface.get_rect(center=(x, y))
        
        box_rect = text_rect.inflate(padding * 2, padding * 2)

        word_boxes.append((word, text_rect, box_rect))

    selected_words = []

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for word, text_rect, box_rect in word_boxes:
                    if box_rect.collidepoint(event.pos):
                        selected_words.append(word)
                        if len(selected_words) == 2:
                            match_found = False
                            if selected_words[0] in english_words and selected_words[1] in spanish_words:
                                if english_words.index(selected_words[0]) == spanish_words.index(selected_words[1]):
                                    match_found = True
                            elif selected_words[0] in spanish_words and selected_words[1] in english_words:
                                if spanish_words.index(selected_words[0]) == english_words.index(selected_words[1]):
                                    match_found = True
                            
                            if match_found:
                                all_words.remove(selected_words[0])
                                all_words.remove(selected_words[1])
                            
                            selected_words = []
                            word_boxes = [(word, text_rect, box_rect) for word, text_rect, box_rect in word_boxes if word in all_words]

        SCREEN.blit(MATCHBG, (0, 0))
        for word, text_rect, box_rect in word_boxes:
            pygame.draw.rect(SCREEN, box_color, box_rect, outline_width)
            text_surface = font.render(word, True, text_color)
            SCREEN.blit(text_surface, text_rect)
        
        if not all_words:
            current_game_state = "play"
            running = False
        
        pygame.display.update()

def listen_game():
    # Game setup
    PLAY_MOUSE_POS = pygame.mouse.get_pos()
    #SCREEN.fill("black")
    running = True

    playaudio_button = Button(image=None, pos=(635, 110), 
                            text_input="Play Audio", font=spec_font(50), base_color="White", hovering_color="Green")
    playaudio_button.changeColor(PLAY_MOUSE_POS)
    playaudio_button.update(SCREEN)
    spanish_eng_words = [("Hola", "Hello"), ("Buenos días", "Good morning"), ("Buenas tardes", "Good afternoon"), ("Buenas noches", "Good night"), ("¿Cómo estás?", "How are you?"), ("¿Qué tal?", "How's it going?"), 
                     ("Por favor", "Please"), ("Gracias", "Thank you"), ("De nada", "You're welcome"), ("Lo siento", "I'm sorry"), ("Perdón", "Excuse me/pardon"), ("¿Cómo te llamas?", "What's your name?"), ("Me llamo", "My name is"), 
                     ("¿Cuántos años tienes?", "How old are you?"), ("Tengo [Número] años", "I am [Number] years old"), ("Uno", "One"), ("Dos", "Two"), ("Tres", "Three"), ("Cuatro", "Four"), ("Cinco", "Five"), ("Seis", "Six"), ("Siete", "Seven"), 
                     ("Ocho", "Eight"), ("Nueve", "Nine"), ("Diez", "Ten"), ("Hablar", "To speak"), ("Comer", "To eat"), ("Beber", "To drink"), ("Dormir", "To sleep"), ("Estudiar", "To study"), ("Trabajar", "To work"), ("Vivir", "To live"), ("Gustar", "To like"), 
                     ("Tener", "To have"), ("Ser", "To be (permanent)"), ("Feliz", "Happy"), ("Triste", "Sad"), ("Grande", "Big"), ("Pequeño", "Small"), ("Nuevo", "New"), ("Viejo", "Old"), ("Bonito", "Beautiful"), ("Feo", "Ugly"), ("Rápido", "Fast"), 
                     ("Lento", "Slow"), ("Desayunar", "To have breakfast"), ("Almorzar", "To have lunch"), ("Cenar", "To have dinner"), ("Ir", "To go"), ("Venir", "To come"), ("Comprar", "To buy"), ("Vender", "To sell"), ("Mirar", "To watch/look at"), 
                     ("Escuchar", "To listen"), ("Leer", "To read"), ("Casa", "House/Home"), ("Trabajo", "Work/Job"), ("Escuela", "School"), ("Tienda", "Store"), ("Restaurante", "Restaurant"), ("Parque", "Park"), ("Playa", "Beach"), ("Hospital", "Hospital"), 
                     ("Banco", "Bank"), ("Iglesia", "Church"), ("Ahora", "Now"), ("Hoy", "Today"), ("Mañana", "Tomorrow"), ("Ayer", "Yesterday"), ("Semana", "Week"), ("Mes", "Month"), ("Año", "Year"), ("Hora", "Hour"), ("Minuto", "Minute"), ("Segundo", "Second")]
    spanish_words = [pair[0] for pair in spanish_eng_words]
    english_words = [pair[1] for pair in spanish_eng_words]
    current_index = 0
    user_text = ""
    active = False

    input_rect = pygame.Rect(550, 600, 140, 32)
    color = pygame.Color("lightskyblue3")
    color_passive = pygame.Color("gray15")
    color = color_passive

    while running:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.blit(LISTENBG, (0, 0))
        playaudio_button.changeColor(PLAY_MOUSE_POS)
        playaudio_button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if playaudio_button.checkForInput(PLAY_MOUSE_POS):
                    mytext = spanish_words[current_index]
                    language = 'es'
                    try:
                        # use tempfile so file is not saved
                        with tempfile.NamedTemporaryFile(delete=True) as fp:
                            tts = gTTS(text=mytext, lang=language, slow=False)
                            tts.save(f"{fp.name}.mp3")
                            pygame.mixer.init()
                            pygame.mixer.music.load(f"{fp.name}.mp3")
                            pygame.mixer.music.play()
                    except Exception as e:
                        print(f"Error playing audio: {e}")
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False
                color = pygame.Color("lightskyblue3") if active else color_passive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        if user_text.lower() == english_words[current_index].lower():
                            print("Correct!")
                            current_index = (current_index + 1) % len(spanish_words)
                            user_text = "" 
                        else:
                            print("Incorrect.")
                            user_text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        user_text += event.unicode

        pygame.draw.rect(SCREEN, color, input_rect, 2)
        text_surface = pygame.font.Font(None, 32).render(user_text, True, (255, 255, 255))
        SCREEN.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

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
                elif LISTEN_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    listen_game()

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