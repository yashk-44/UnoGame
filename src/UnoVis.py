import math
import os
from time import sleep

import pygame
import UnoAlg as Uno
from typing import *

# IMPORTANT CONSTANTS FOR COLOURS
RED = '#D50000'
YELLOW = '#FFD500'
GREEN = '#3E9A3F'
BLUE = '#005BAA'
WHITE = '#FFFFFF'
BLACK = '#000000'
LIGHT_GRAY = '#C9C9C9'
SCARLET_RED = '#D20103'
HONEY_YELLOW = '#FFDE59'
LEADER_YELLOW = '#FDEA16'
COLORS = [BLUE, GREEN, YELLOW, RED, BLACK]

# CONSTANTS FOR THE CARDS TO BE DISPLAYED FOR EACH PLAYER
CARD_WIDTH, CARD_HEIGHT = 80, 120

# CONSTANTS FOR MAXIMUM AND MINIMUM NUMBER OF PLAYERS
MIN_PLAYERS, MAX_PLAYERS = 2, 10

# Initialize the pygame
pygame.init()

# GLOBAL VARIABLES FOR BUTTONS
button_width, button_height = 220, 50
button_rect = pygame.Rect(0, 0, button_width, button_height)
button_color = BLACK
font_color = BLACK

# GLOBAL VARIABLES FOR PLAYER COUNT AND PLAYER COUNT DISPLAY MESSAGE
number_of_players = MIN_PLAYERS
player_count_message = "2 (minimum)"

# CONSTANTS FOR CARD DISPLAY FONTS
game_font = pygame.font.SysFont("segoeui", 35, True)
draw_card_font = pygame.font.SysFont("segoeui", 30, True)
card_font = pygame.font.SysFont("sequeui", 40, False)
alert_font = pygame.font.SysFont("segoeui", 40, True)
top_card_font = pygame.font.SysFont("segoeui", 45, True)

# GLOBAL VARIABLES FOR THE WIDTH AND HEIGHT OF THE WINDOW
screen_width, screen_height = 600, 600

# GLOBAL VARIABLE FOR THE PAGE NUMBER OF THIS PLAYERS CARDS
page_number = 1

# GLOBAL VARIABLE FOR THE TOP CARD RECTANGLE
top_card_rect: Optional[pygame.Rect] = None

# GLOBAL VARIABLE TO STORE THE BUTTON BEING HOVERED OVER
to_highlight: Optional[int] = None
hovered_card: Optional[Uno.Card] = None

# GLOBAL VARIABLE TO STORE WHICH COLOR THE PLAYER IS HOVERING OVER AFTER SELECTING +4 OR WILD CARD
hovered_color: Optional[pygame.Rect] = None

# GLOBAL VARIABLE TO STORE WHETHER PLAYER IS HOVERING OVER THE UNO OR DRAW CARD BUTTON
uno_hover = False
draw_hover = False

# Creates the screen
screen = pygame.display.set_mode((screen_width, screen_height))

# Sets the title and icon
pygame.display.set_caption("UNO!")
dir_to_image = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "resources", "unologo_2.png")
icon = pygame.image.load(dir_to_image)
pygame.display.set_icon(icon)

# Sets up the homescreen logo
home_icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "resources", "unologo.png")
icon = pygame.image.load(home_icon_path).convert_alpha()
icon = pygame.transform.scale(icon, (icon.get_width() // 12.5, icon.get_height() // 12.5))
icon_rect = icon.get_rect(center=(screen_width // 2, screen_height // 3))

# BUTTONS TO DISPLAY THE COLORS WHEN A USER SELECTS A +4 OR WILDCARD
COLOUR_RECTS: dict[tuple[str, str], pygame.Rect] = \
    {(RED, "red"): pygame.Rect((screen_width // 2) - 90, (screen_height // 2) - 90, 85, 85)
        , (GREEN, "green"): pygame.Rect((screen_width // 2) + 5, (screen_height // 2) - 90, 85, 85)
        , (BLUE, "blue"): pygame.Rect((screen_width // 2) - 90, (screen_height // 2) + 5, 85, 85)
        , (YELLOW, "yellow"): pygame.Rect((screen_width // 2) + 5, (screen_height // 2) + 5, 85, 85)}


# A function to "animate" a loading screen
def intro_screen() -> None:
    """
    Starts an animation for the opening screen of this game.
    :return: None
    """
    for i in range(len(COLORS)):
        screen.fill(COLORS[i])
        pygame.display.update()
        sleep(0.75 + (0.15 * i))
    screen.blit(icon, icon_rect)
    pygame.display.update()
    sleep(1)


# A function to display the home screen
def home_screen() -> bool:
    """
    A function to display the home screen of the game.
    :return: False upon user pressing start button.
    """
    global button_rect, button_color, font_color, game_font
    screen.fill(BLACK)
    screen.blit(icon, icon_rect)

    start_text = game_font.render("click here to start", False, font_color)
    button_rect.width = start_text.get_rect().width + 20
    button_rect.height = start_text.get_rect().height + 10
    pygame.draw.rect(screen, button_color, button_rect)
    button_rect.center = (screen_width // 2, 3.5 * (screen_height // 5))
    start_rect = start_text.get_rect(center=button_rect.center)

    screen.blit(start_text, start_rect)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)
        elif event.type == pygame.MOUSEBUTTONDOWN and button_rect.collidepoint(pygame.mouse.get_pos()):
            return False
    if button_rect.collidepoint(pygame.mouse.get_pos()):
        button_color = YELLOW
        font_color = RED
    else:
        button_color = RED
        font_color = YELLOW
    return True


# A function to display the setup screen
def config_screen() -> bool:
    """
    A function to display the player-configuration screen
    :return: False if user presses the start button, True otherwise.
    """
    global number_of_players, player_count_message, font_color, button_color

    screen.fill(LIGHT_GRAY)

    instruction_font = pygame.font.SysFont("segoeui", 35, True)
    instruction_text = instruction_font.render("number of players", True, HONEY_YELLOW)
    instruction_rect = instruction_text.get_rect(center=button_rect.center)
    instruction_rect = pygame.Rect(0, 0, instruction_rect.width + 6, instruction_rect.height + 6)
    instruction_rect.center = (screen_width // 2, screen_height // 4)
    pygame.draw.rect(screen, SCARLET_RED, instruction_rect)
    screen.blit(instruction_text, (instruction_rect.x + 3, instruction_rect.y + 3))

    player_count_font = pygame.font.SysFont("calibri", 33, False)
    player_count_text = player_count_font.render(player_count_message, True, BLACK)
    player_count_rect = pygame.Rect(0, 0, screen_width, screen_height)
    player_count_rect.center = (screen_width // 2, screen_height // 2.35)
    screen.blit(player_count_text, player_count_text.get_rect(center=player_count_rect.center))

    pm_font = pygame.font.SysFont('impact', 40, True)
    button_rect.center = (screen_width // 3), (screen_height // 4) * 3
    minus_text = pm_font.render("-", True, WHITE)
    minus_rect = minus_text.get_rect(center=button_rect.center)

    button_rect.center = button_rect.center[0] * 2, button_rect.center[1]
    plus_text = pm_font.render("+", True, WHITE)
    plus_rect = plus_text.get_rect(center=button_rect.center)
    plus_rect.width, minus_rect.width = plus_rect.height, minus_rect.height
    minus_rect.center, plus_rect.center = ((screen_width // 3, math.floor((screen_height // 3) * 1.75)),
                                           (2 * (screen_width // 3), math.floor((screen_height // 3) * 1.75)))

    start_game_font = pygame.font.SysFont("segoeui", 35, True)
    start_game_text = start_game_font.render("start game!", True, font_color)
    start_game_rect = start_game_text.get_rect(center=button_rect.center)
    start_game_rect = pygame.Rect(0, 0, start_game_rect.width + 4, start_game_rect.height + 4)
    start_game_rect.center = (screen_width // 2, 3.675 * (screen_height // 5))

    pygame.draw.rect(screen, button_color, start_game_rect)
    pygame.draw.rect(screen, RED, minus_rect)
    pygame.draw.rect(screen, GREEN, plus_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if minus_rect.collidepoint(pygame.mouse.get_pos()):
                number_of_players = max(number_of_players - 1, MIN_PLAYERS)
                if number_of_players == MIN_PLAYERS:
                    player_count_message = "2 (minimum)"
                else:
                    player_count_message = str(number_of_players)
            elif plus_rect.collidepoint(pygame.mouse.get_pos()):
                number_of_players = min(number_of_players + 1, MAX_PLAYERS)
                if number_of_players == MAX_PLAYERS:
                    player_count_message = "10 (maximum)"
                else:
                    player_count_message = str(number_of_players)

            elif start_game_rect.collidepoint(pygame.mouse.get_pos()):
                return False
        elif start_game_rect.collidepoint(pygame.mouse.get_pos()):
            if not (button_color == GREEN or font_color == WHITE):
                button_color, font_color = GREEN, WHITE
        else:
            if not (button_color == YELLOW or font_color == BLUE):
                button_color, font_color = YELLOW, BLUE
    screen.blit(minus_text, minus_text.get_rect(center=minus_rect.center))
    screen.blit(plus_text, plus_text.get_rect(center=plus_rect.center))
    screen.blit(start_game_text, start_game_text.get_rect(center=start_game_rect.center))
    pygame.display.update()
    return True


def select_color() -> Optional[str]:
    """
    A function to display and prompt the user to select a color
    :return: A selected colour if user clicks on a button, None otherwise to indicate the user cancelled it.
    """
    global hovered_color
    # INSTRUCTION TEXT TO SELECT A COLOR
    while True:
        screen.fill(BLACK)
        color_choose_text_1 = (pygame.font.SysFont("seqoeui", 45, False).
                               render("CHOOSE A COLOUR or", True, WHITE))
        cct_rect_1 = color_choose_text_1.get_rect()
        cct_rect_1.center = screen_width // 2, screen_height // 4
        screen.blit(color_choose_text_1, color_choose_text_1.get_rect(center=cct_rect_1.center))

        color_choose_text_2 = (pygame.font.SysFont("seqoeui", 45, False).
                               render("PRESS ANYWHERE ELSE TO CANCEL", True, WHITE))
        cct_rect_2 = color_choose_text_2.get_rect()
        cct_rect_2.center = screen_width // 2, (screen_height // 4) + cct_rect_1.height
        screen.blit(color_choose_text_2, color_choose_text_2.get_rect(center=cct_rect_2.center))
        # END OF INSTRUCTION TEXT RENDERING

        for colour_rect in COLOUR_RECTS:
            pygame.draw.rect(screen, colour_rect[0], COLOUR_RECTS[colour_rect], 3 * (COLOUR_RECTS[colour_rect] !=
                                                                                     hovered_color), 3, 5, 5, 5, 5)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                if event.button == 1:
                    for rect in COLOUR_RECTS:
                        if COLOUR_RECTS[rect].collidepoint(position):
                            hovered_color = None
                            return rect[1]
                    hovered_color = None
                    return None
            else:
                position = pygame.mouse.get_pos()
                for rect in COLOUR_RECTS:
                    if COLOUR_RECTS[rect].collidepoint(position):
                        hovered_color = COLOUR_RECTS[rect]
                        break
                    else:
                        hovered_color = None
        pygame.display.update()


def uno_function(game_played: Uno.GameControls) -> bool:
    """
    A function that deals with the event of the current player pressing the UNO! button.
    :param game_played: the game being played
    :return: None
    """
    safe_call = False
    players = game_played.list_of_players
    current_player = game_played.current_player
    if not current_player.has_called_uno() and current_player.get_num_cards() == 1:
        current_player.call_uno()
        safe_call = True

    for player in players:
        if player != current_player and player.get_num_cards() == 1 and not player.has_called_uno():
            safe_call = True
            player.draw_card(2)
    return safe_call


def buffer_action(game_played: Uno.GameControls) -> None:
    """
    This function handles events after a player has placed a card.
    :return:
    """
    global page_number, to_highlight, hovered_card, hovered_color, uno_hover, draw_hover, top_card_rect

    start_time = pygame.time.get_ticks()
    timer_duration = 3000  # milliseconds (3 seconds)
    running = True

    while running:
        screen.fill(BLACK)
        card_count_font = pygame.font.SysFont("segoeui", 22, False)

        # THIS SECTION TAKES CARE OF PRINTING THE PLAYER STATS ON THE TOP-LEFT OF THE SCREEN
        leader = game_played.get_leader()
        players = game_played.list_of_players

        for i in range(len(players)):
            curr_card_count = players[i].get_num_cards()
            message = f"{players[i].name}"
            if players[i] == game_played.current_player:
                card_count_font.bold = True
                message += " (you)"
                message += f": {players[i].get_num_cards()} card"
            else:
                if game_played.get_next_player(hovered_card) == players[i]:
                    message += " (next)"
                    if isinstance(hovered_card, Uno.Card):
                        if hovered_card.value == "+4":
                            curr_card_count += 4
                        elif hovered_card.value == "+2":
                            curr_card_count += 2
                message += f": {players[i].get_num_cards()} card"
                card_count_font.bold = False
            if curr_card_count > 1:
                message += "s"
            if players[i] == leader:
                player_count_color = LEADER_YELLOW
            else:
                player_count_color = WHITE

            card_count_text = card_count_font.render(message, True, player_count_color)
            temp = card_count_text.get_rect()
            temp.topleft = 5, i * card_count_font.get_height()  # SHIFTS THE TEXT DOWN
            screen.blit(card_count_text, temp)
        # END OF PLAYER-STAT SECTION

        if hovered_card is not None:
            if hovered_card.value == "rev.":
                if game_played.is_reversed():
                    arrow = "direction: \u2193"
                else:
                    arrow = "direction: \u2191"
            else:
                if game_played.is_reversed():
                    arrow = "direction: \u2191"
                else:
                    arrow = "direction: \u2193"
        else:
            if game_played.is_reversed():
                arrow = "direction: \u2191"
            else:
                arrow = "direction: \u2193"

        arrow_rendered = pygame.font.SysFont("segoeui", 35, True).render(arrow, True, WHITE)
        arrow_rect = arrow_rendered.get_rect()
        arrow_rect.topright = screen_width - 10, 0
        screen.blit(arrow_rendered, arrow_rect)

        # DISPLAYS THE TOP CARD IN THE PILE
        top_card = game_played.pile_of_cards.top_card
        top_card_rect = pygame.Rect(0, 0, 100, 150)
        top_card_rect.center = screen_width // 2, (screen_height // 2) - 20
        top_card_color = top_card.display_colour
        pygame.draw.rect(screen, top_card_color, top_card_rect, 0, 5, 5, 5, 5)
        top_card_font_color = WHITE
        if top_card_color in [WHITE, YELLOW]:
            top_card_font_color = BLACK
        top_card_text = top_card_font.render(top_card.value, True, top_card_font_color)
        screen.blit(top_card_text, top_card_text.get_rect(center=top_card_rect.center))
        # END OF RENDERING TOP CARD

        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time

        # TODO: START OF DISPLAYING
        card_buttons: list[tuple[pygame.Rect, Uno.Card]] = []

        # CREATES A BUTTON TO DRAW ANOTHER CARD
        draw_text_col = WHITE
        if draw_hover:
            draw_text_col = BLACK
        draw_card_text = draw_card_font.render("draw", True, draw_text_col)
        draw_card_button = draw_card_text.get_rect()
        draw_card_button.width += 20
        draw_card_button.height = draw_card_button.width
        draw_card_button.center = (screen_width // 3) * 2.20, 0
        draw_card_button.top = top_card_rect.center[1] + 5
        pygame.draw.rect(screen, SCARLET_RED, draw_card_button, 4 * int(not draw_hover), 4, 4, 4, 4)
        screen.blit(draw_card_text, draw_card_text.get_rect(center=draw_card_button.center))
        # END OF RENDERING THE DRAW CARD BUTTON

        # CREATES A "UNO!" BUTTON
        uno_text_col = WHITE
        if uno_hover:
            uno_text_col = BLACK
        uno_text = draw_card_font.render("UNO!", True, uno_text_col)
        uno_button = uno_text.get_rect()
        uno_button.width = draw_card_button.width
        uno_button.height = uno_button.width
        uno_button.center = (screen_width // 3) * 2.20, 0
        uno_button.bottom = top_card_rect.center[1] - 5
        pygame.draw.rect(screen, LEADER_YELLOW, uno_button, 4 * int(not uno_hover), 4, 4, 4, 4)
        screen.blit(uno_text, uno_text.get_rect(center=uno_button.center))
        # END OF RENDERING THE UNO! BUTTON

        # START OF CODE TO DISPLAY THE PAGE THIS PERSON WANTS
        card_pages = game_played.current_player.get_card_pages()
        cards = card_pages[page_number]

        total_width = (len(cards) * CARD_WIDTH) + ((len(cards) - 1) * 4)
        midpoint = total_width // 2
        start_x = (screen_width // 2) - midpoint  # THE START OF DISPLAYING ALL THE CARDS
        start_y = 460
        for i in range(len(cards)):
            card_button = pygame.Rect(start_x + (i * (4 + CARD_WIDTH)), start_y, CARD_WIDTH, CARD_HEIGHT)
            card_color = WHITE
            if cards[i].display_colour in [WHITE, YELLOW]:
                card_color = BLACK
            if to_highlight == i:
                pygame.draw.rect(screen, cards[i].display_colour, card_button, 0, 3, 3, 3, 3)
                card_label = card_font.render(cards[i].value, True, card_color)
            else:
                pygame.draw.rect(screen, cards[i].display_colour, card_button, 6, 3, 3, 3, 3)
                card_label = card_font.render(cards[i].value, True, WHITE)
            screen.blit(card_label, card_label.get_rect(center=card_button.center))
            card_buttons.append((card_button, cards[i]))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            elif event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    page_number = min(page_number + 1, len(card_pages))
                else:
                    page_number = max(page_number - 1, 1)
                continue
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    position = pygame.mouse.get_pos()
                    if uno_button.collidepoint(position):
                        if not uno_function(game_played):
                            screen.fill(SCARLET_RED)
                            false_call_text = alert_font.render("False call!", True, WHITE)
                            false_call_rect = false_call_text.get_rect()
                            false_call_rect.center = screen_width // 2, screen_height // 2
                            screen.blit(false_call_text, false_call_text.get_rect(center=false_call_rect.center))
                            pygame.display.update()
                            sleep(3)
                        pygame.display.update()
                    else:
                        running = False
                    break

            else:
                position = pygame.mouse.get_pos()
                for button in card_buttons:
                    if button[0].collidepoint(position):
                        to_highlight = card_buttons.index(button)
                        hovered_card = button[1]
                        break
                    else:
                        to_highlight = hovered_card = None
                if draw_card_button.collidepoint(position):
                    uno_hover = False
                    draw_hover = True
                elif uno_button.collidepoint(position):
                    uno_hover = True
                    draw_hover = False
                else:
                    uno_hover = draw_hover = False

        # Update display
        pygame.display.update()

        # End condition
        if elapsed_time >= timer_duration:
            running = False

        # pygame.time.delay(100)  # Optional to reduce CPU usage

    display_next_player_screen(game_played)


def display_first_player_screen(game_played: Uno.GameControls) -> None:
    """
    Displays a screen, urging the next player to make their move.
    :param game_played: the game being played.
    :return: None
    """
    global to_highlight
    screen.fill(YELLOW)

    pass_font = pygame.font.SysFont("consolas", 30, True)
    pass_text_top = pass_font.render(f"{game.current_player.name.capitalize()} starts.", True, BLACK)
    pass_text_upper_mid = pass_font.render(f" Pass device to {game.current_player.name.capitalize()}.", True, BLACK)
    pass_text_lower_mid = pass_font.render("click anywhere on the screen", True, BLACK)
    pass_text_bottom = pass_font.render(f"when {game.current_player.name.capitalize()} is ready.", True, BLACK)

    pass_text_top_rect = pass_text_top.get_rect()
    pass_text_top_rect.center = (screen_width // 2, (screen_height // 2) - pass_text_upper_mid.get_height() -
                                 pass_text_top.get_height())

    pass_text_upper_mid_rect = pass_text_upper_mid.get_rect()
    pass_text_upper_mid_rect.center = screen_width // 2, screen_height // 2 - pass_text_upper_mid.get_height()

    pass_text_lower_mid_rect = pass_text_lower_mid.get_rect()
    pass_text_lower_mid_rect.center = screen_width // 2, screen_height // 2 + pass_text_lower_mid.get_height()

    pass_text_bottom_rect = pass_text_bottom.get_rect()
    pass_text_bottom_rect.center = (screen_width // 2, (screen_height // 2) + pass_text_bottom.get_height() +
                                    pass_text_lower_mid.get_height())

    screen.blit(pass_text_top, pass_text_top.get_rect(center=pass_text_top_rect.center))
    screen.blit(pass_text_upper_mid, pass_text_upper_mid.get_rect(center=pass_text_upper_mid_rect.center))
    screen.blit(pass_text_lower_mid, pass_text_lower_mid.get_rect(center=pass_text_lower_mid_rect.center))
    screen.blit(pass_text_bottom, pass_text_bottom.get_rect(center=pass_text_bottom_rect.center))

    pygame.display.update()

    keep = True
    while keep:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                keep = False
                break
    to_highlight = None


def display_next_player_screen(game_played: Uno.GameControls) -> None:
    """
    Displays a screen, urging the next player to make their move.
    :param game_played: the game being played.
    :return: None
    """
    global to_highlight
    if not game_played.is_reversed():
        screen.fill(GREEN)
    else:
        screen.fill(SCARLET_RED)

    pass_font = pygame.font.SysFont("consolas", 30, True)
    pass_text_top = pass_font.render(f"Pass device to {game.get_next_player(hovered_card).name.capitalize()}.",
                                     True, WHITE)
    pass_text_middle = pass_font.render("Click anywhere on the screen", True, WHITE)
    pass_text_bottom = pass_font.render(f"when {game.get_next_player(hovered_card).name.capitalize()} is ready.",
                                        True, WHITE)

    pass_text_top_rect = pass_text_top.get_rect()
    pass_text_top_rect.center = screen_width // 2, (screen_height // 2) - pass_text_top.get_height() - 3

    pass_text_middle_rect = pass_text_middle.get_rect()
    pass_text_middle_rect.center = screen_width // 2, screen_height // 2

    pass_text_bottom_rect = pass_text_bottom.get_rect()
    pass_text_bottom_rect.center = screen_width // 2, (screen_height // 2) + pass_text_bottom.get_height() + 3

    screen.blit(pass_text_top, pass_text_top.get_rect(center=pass_text_top_rect.center))
    screen.blit(pass_text_middle, pass_text_middle.get_rect(center=pass_text_middle_rect.center))
    screen.blit(pass_text_bottom, pass_text_bottom.get_rect(center=pass_text_bottom_rect.center))

    pygame.display.update()

    keep = True
    while keep:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                keep = False
                break
    to_highlight = None


def play_screen_fixed(game_played: Uno.GameControls) -> None:
    """
    A function to set up the concrete, non-interactive sections of the
    stage for card-placement.
    :param game_played: the game being played.
    :return: None
    """
    global top_card_rect

    screen.fill(BLACK)
    card_count_font = pygame.font.SysFont("segoeui", 22, False)

    # THIS SECTION TAKES CARE OF PRINTING THE PLAYER STATS ON THE TOP-LEFT OF THE SCREEN
    leader = game_played.get_leader()
    players = game_played.list_of_players

    for i in range(len(players)):
        curr_card_count = players[i].get_num_cards()
        message = f"{players[i].name}"
        if players[i] == game_played.current_player:
            card_count_font.bold = True
            message += " (you)"
            if game_played.get_next_player(hovered_card) == players[i]:
                message += " (next)"
            message += f": {curr_card_count} card"
        else:
            if game_played.get_next_player(hovered_card).prev_player == players[i]:
                if isinstance(hovered_card, Uno.Card):
                    if hovered_card.value == "+4":
                        curr_card_count += 4
                    elif hovered_card.value == "+2":
                        curr_card_count += 2
            elif game_played.get_next_player(hovered_card) == players[i]:
                message += " (next)"
            message += f": {curr_card_count} card"
            card_count_font.bold = False
        if curr_card_count > 1:
            message += "s"
        if players[i] == leader:
            player_count_color = LEADER_YELLOW
        else:
            player_count_color = WHITE

        card_count_text = card_count_font.render(message, True, player_count_color)
        temp = card_count_text.get_rect()
        temp.topleft = 5, i * card_count_font.get_height()  # SHIFTS THE TEXT DOWN
        screen.blit(card_count_text, temp)

    if hovered_card is not None:
        if hovered_card.value == "rev.":
            if game_played.is_reversed():
                arrow = "direction: \u2193"
            else:
                arrow = "direction: \u2191"
        else:
            if game_played.is_reversed():
                arrow = "direction: \u2191"
            else:
                arrow = "direction: \u2193"
    else:
        if game_played.is_reversed():
            arrow = "direction: \u2191"
        else:
            arrow = "direction: \u2193"

    arrow_rendered = pygame.font.SysFont("segoeui", 35, True).render(arrow, True, WHITE)
    arrow_rect = arrow_rendered.get_rect()
    arrow_rect.topright = screen_width - 10, 0
    screen.blit(arrow_rendered, arrow_rect)

    # DISPLAYS THE TOP CARD IN THE PILE
    top_card = game_played.pile_of_cards.top_card
    top_card_rect = pygame.Rect(0, 0, 100, 150)
    top_card_rect.center = screen_width // 2, (screen_height // 2) - 20
    top_card_color = top_card.display_colour
    pygame.draw.rect(screen, top_card_color, top_card_rect, 0, 5, 5, 5, 5)
    top_card_font_color = WHITE
    if top_card_color in [WHITE, YELLOW]:
        top_card_font_color = BLACK
    top_card_text = top_card_font.render(top_card.value, True, top_card_font_color)
    screen.blit(top_card_text, top_card_text.get_rect(center=top_card_rect.center))
    # END OF RENDERING TOP CARD


def play_screen_interactive(game_played: Uno.GameControls) -> None:
    """
    A function to just update the screen to display the current card
    :param game_played: the game being played and controlled
    :return: True upon game ending
    """
    global page_number, to_highlight, hovered_card, hovered_color, uno_hover, draw_hover

    card_buttons: list[tuple[pygame.Rect, Uno.Card]] = []

    # CREATES A BUTTON TO DRAW ANOTHER CARD
    draw_text_col = WHITE
    if draw_hover:
        draw_text_col = BLACK
    draw_card_text = draw_card_font.render("draw", True, draw_text_col)
    draw_card_button = draw_card_text.get_rect()
    draw_card_button.width += 20
    draw_card_button.height = draw_card_button.width
    draw_card_button.center = (screen_width // 3) * 2.20, 0
    draw_card_button.top = top_card_rect.center[1] + 5
    pygame.draw.rect(screen, SCARLET_RED, draw_card_button, 4 * int(not draw_hover), 4, 4, 4, 4)
    screen.blit(draw_card_text, draw_card_text.get_rect(center=draw_card_button.center))
    # END OF RENDERING THE DRAW CARD BUTTON

    # CREATES A "UNO!" BUTTON
    uno_text_col = WHITE
    if uno_hover:
        uno_text_col = BLACK
    uno_text = draw_card_font.render("UNO!", True, uno_text_col)
    uno_button = uno_text.get_rect()
    uno_button.width = draw_card_button.width
    uno_button.height = uno_button.width
    uno_button.center = (screen_width // 3) * 2.20, 0
    uno_button.bottom = top_card_rect.center[1] - 5
    pygame.draw.rect(screen, LEADER_YELLOW, uno_button, 4 * int(not uno_hover), 4, 4, 4, 4)
    screen.blit(uno_text, uno_text.get_rect(center=uno_button.center))
    # END OF RENDERING THE UNO! BUTTON

    # START OF CODE TO DISPLAY THE PAGE THIS PERSON WANTS
    card_pages = game_played.current_player.get_card_pages()
    cards = card_pages[page_number]

    total_width = (len(cards) * CARD_WIDTH) + ((len(cards) - 1) * 4)
    midpoint = total_width // 2
    start_x = (screen_width // 2) - midpoint  # THE START OF DISPLAYING ALL THE CARDS
    start_y = 460
    for i in range(len(cards)):
        card_button = pygame.Rect(start_x + (i * (4 + CARD_WIDTH)), start_y, CARD_WIDTH, CARD_HEIGHT)
        card_color = WHITE
        if cards[i].display_colour in [WHITE, YELLOW]:
            card_color = BLACK
        if to_highlight == i:
            pygame.draw.rect(screen, cards[i].display_colour, card_button, 0, 3, 3, 3, 3)
            card_label = card_font.render(cards[i].value, True, card_color)
        else:
            pygame.draw.rect(screen, cards[i].display_colour, card_button, 6, 3, 3, 3, 3)
            card_label = card_font.render(cards[i].value, True, WHITE)
        screen.blit(card_label, card_label.get_rect(center=card_button.center))
        card_buttons.append((card_button, cards[i]))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)
        elif event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                page_number = min(page_number + 1, len(card_pages))
            else:
                page_number = max(page_number - 1, 1)
            continue
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                position = pygame.mouse.get_pos()
                for button in card_buttons:
                    if button[0].collidepoint(position):
                        if button[1].colour == "white":
                            # START OF CODE TO DISPLAY THE FOUR COLORS AS OPTIONS
                            selected_color = select_color()
                            if selected_color is None:
                                break
                            else:
                                to_highlight = hovered_card = None
                                game_played.current_player.place_card(button[1], selected_color)
                                if game_played.get_game_status()[0]:
                                    return
                                buffer_action(game_played)
                                game_played.update_game(button[1], selected_color)
                            to_highlight = hovered_card = None
                            break
                        elif game_played.check_card_validity(button[1]):
                            game_played.current_player.place_card(button[1])
                            if game_played.get_game_status()[0]:
                                return
                            buffer_action(game_played)
                            game_played.update_game(button[1])
                            card_pages = game_played.current_player.get_card_pages()
                            page_number = 1
                            pygame.display.update()
                            break
                        else:
                            screen.fill(SCARLET_RED)
                            alert_text_middle = alert_font.render("TRY ANOTHER CARD, or", True, WHITE)
                            middle_rect = alert_text_middle.get_rect(center=(screen_width // 2, screen_height // 2))

                            alert_text_top = alert_font.render("CANNOT PLACE THIS CARD!", True, WHITE)
                            top_rect = alert_text_top.get_rect(
                                center=(screen_width // 2, (screen_height // 2) - alert_font.get_height()))

                            alert_text_bottom = alert_font.render("DRAW A CARD", True, WHITE)
                            bottom_rect = alert_text_bottom.get_rect(
                                center=(screen_width // 2, (screen_height // 2) + alert_font.get_height()))

                            screen.blit(alert_text_top, top_rect)
                            screen.blit(alert_text_middle, middle_rect)
                            screen.blit(alert_text_bottom, bottom_rect)
                            pygame.display.update()
                            sleep(2)
                            break
                if draw_card_button.collidepoint(position):
                    game_played.current_player.draw_card()
                    game_played.next_player()
                    page_number = 1
                    break
                elif uno_button.collidepoint(position):
                    if not uno_function(game_played):
                        screen.fill(SCARLET_RED)
                        false_call_text = alert_font.render("False call!", True, WHITE)
                        false_call_rect = false_call_text.get_rect()
                        false_call_rect.center = screen_width // 2, screen_height // 2
                        screen.blit(false_call_text, false_call_text.get_rect(center=false_call_rect.center))
                        pygame.display.update()
                        sleep(3)
                    pygame.display.update()
                    break

        else:
            position = pygame.mouse.get_pos()
            for button in card_buttons:
                if button[0].collidepoint(position):
                    to_highlight = card_buttons.index(button)
                    hovered_card = button[1]
                    break
                else:
                    to_highlight = hovered_card = None
            if draw_card_button.collidepoint(position):
                uno_hover = False
                draw_hover = True
            elif uno_button.collidepoint(position):
                uno_hover = True
                draw_hover = False
            else:
                uno_hover = draw_hover = False
    pygame.display.update()


def display_winner(game_played: Uno.GameControls) -> bool:
    """
    Displays the winner, and asks if user wants to play again or not
    :param game_played: the game being played
    :return: True if the player wants to play again, False otherwise.
    """
    yes_hovered, no_hovered = False, False
    # ANNOUNCES WINNER
    screen.fill(BLUE)
    winner_font = pygame.font.SysFont("segoui", 60, False)
    winner_text = winner_font.render(f"{game_played.get_game_status()[1].name} wins!", True, LEADER_YELLOW)
    winner_rect = winner_text.get_rect()
    winner_rect.center = screen_width // 2, screen_height // 2.1
    screen.blit(winner_text, winner_text.get_rect(center=winner_rect.center))
    pygame.display.update()
    sleep(3)
    # END OF WINNER ANNOUNCEMENT

    # CREATES THE TEXT PROMPTING USER TO PLAY AGAIN OR NOT
    again_font = pygame.font.SysFont("seqoeui", 50, False)
    again_text = again_font.render("play again?", True, WHITE)
    again_rect = again_text.get_rect()
    again_rect.center = screen_width // 2, screen_height // 1.75
    screen.blit(again_text, again_text.get_rect(center=again_rect.center))
    # END OF TEXT PROMPT

    # CREATES THE TWO BUTTONS NEEDED
    yes_no_font = pygame.font.SysFont("segoeui", 40, True)

    yes_text = yes_no_font.render("Yes", True, WHITE)
    yes_rect = yes_text.get_rect()
    yes_rect.width += 10
    yes_rect.height += 10
    yes_rect.center = screen_width // 2, screen_height // 1.50
    yes_rect.right = (screen_width // 2) - 5

    no_text = yes_no_font.render("No", True, WHITE)
    no_rect = no_text.get_rect()
    no_rect.width += 10
    no_rect.height += 10
    no_rect.center = screen_width // 2, screen_height // 1.50
    no_rect.left = (screen_width // 2) + 5

    if yes_hovered and not no_hovered:
        pygame.draw.rect(screen, GREEN, yes_rect, 3)
        pygame.draw.rect(screen, RED, no_rect, 0)
    elif no_hovered and not yes_hovered:
        pygame.draw.rect(screen, GREEN, yes_rect, 0)
        pygame.draw.rect(screen, RED, no_rect, 3)
    else:
        pygame.draw.rect(screen, GREEN, yes_rect, 0)
        pygame.draw.rect(screen, RED, no_rect, 0)

    screen.blit(yes_text, yes_text.get_rect(center=yes_rect.center))
    screen.blit(no_text, no_text.get_rect(center=no_rect.center))
    pygame.display.update()

    while True:
        screen.fill(BLUE)

        screen.blit(winner_text, winner_text.get_rect(center=winner_rect.center))
        screen.blit(again_text, again_text.get_rect(center=again_rect.center))

        if yes_hovered and not no_hovered:
            pygame.draw.rect(screen, GREEN, yes_rect, 0)
            pygame.draw.rect(screen, RED, no_rect, 3)
        elif no_hovered and not yes_hovered:
            pygame.draw.rect(screen, GREEN, yes_rect, 3)
            pygame.draw.rect(screen, RED, no_rect, 0)
        else:
            pygame.draw.rect(screen, GREEN, yes_rect, 3)
            pygame.draw.rect(screen, RED, no_rect, 3)
        screen.blit(yes_text, yes_text.get_rect(center=yes_rect.center))
        screen.blit(no_text, no_text.get_rect(center=no_rect.center))
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                position = pygame.mouse.get_pos()
                if yes_rect.collidepoint(position):
                    return True
                elif no_rect.collidepoint(position):
                    return False
            else:
                position = pygame.mouse.get_pos()
                if yes_rect.collidepoint(position):
                    yes_hovered = True
                    no_hovered = False
                elif no_rect.collidepoint(position):
                    yes_hovered = False
                    no_hovered = True
                else:
                    yes_hovered = no_hovered = False
        pygame.display.update()


def play_screen(game_played: Uno.GameControls) -> bool:
    """
    A function that displays the full screen for the player
    :param game_played: the game being played.
    :return: False upon game completion
    """
    while not game_played.get_game_status()[0]:
        play_screen_fixed(game_played)
        play_screen_interactive(game_played)
    return False


def exit_screen() -> None:
    """
    A function that displays an exiting screen.
    :return:
    """
    screen.fill(BLACK)
    final_text = pygame.font.SysFont("segoeui", 50, True).render("Thanks for playing", True, WHITE)
    final_rect = final_text.get_rect()
    final_rect.center = screen_width // 2, (screen_height // 2) - (icon_rect.height // 2) - 50
    icon_rect.center = screen_width // 2, screen_height // 2
    screen.blit(final_text, final_text.get_rect(center=final_rect.center))
    screen.blit(icon, icon_rect)
    pygame.display.update()
    sleep(5)


if __name__ == "__main__":
    # a boolean to indicate whether the current stage of game is done or not
    runs = True

    # FIRST LOOP FOR THE HOME SCREEN ANIMATION AND SETUP
    intro_screen()

    while runs:
        runs = home_screen()

    plays = True
    while plays:
        runs = True
        font_color, button_color = BLUE, YELLOW
        while runs:
            runs = config_screen()

        game = Uno.GameControls([f"player {i}" for i in range(1, number_of_players + 1)])
        # Generates the game accordingly
        display_first_player_screen(game)

        play_screen(game)

        plays = display_winner(game)

    exit_screen()
