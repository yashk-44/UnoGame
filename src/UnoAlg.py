from __future__ import annotations
from random import randint
from typing import Union, Optional

# ALL COLOR CONSTANTS
RED = '#D50000'
YELLOW = '#FFD500'
GREEN = '#3E9A3F'
BLUE = '#005BAA'
WHITE = '#FFFFFF'

# ALL VALUES AND COLORS
POSSIBLE_COLORS = [("red", RED, 0), ("green", GREEN, 1), ("blue", BLUE, 2),
                   ("yellow", YELLOW, 3)]
POSSIBLE_VALUES = {0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8",
                   9: "9", 10: "skip", 11: "rev.", 12: "+2",
                   13: "wild", 14: "+4"}
POSSIBLE_VALUES_INVERTED = {}
for val in POSSIBLE_VALUES:
    POSSIBLE_VALUES_INVERTED[POSSIBLE_VALUES[val]] = val


def create_player_link(lop: list[Player]):
    for i in range(len(lop)):
        if i == 0:
            lop[i].prev_player = lop[-1]
            lop[i].next_player = lop[i + 1]
        elif i == len(lop) - 1:
            lop[i].prev_player = lop[i - 1]
            lop[i].next_player = lop[0]
        else:
            lop[i].next_player = lop[i + 1]
            lop[i].prev_player = lop[i - 1]


def generate_random_card(num_times: int = 1) -> list[Card]:
    """
    Generates random cards.
    """

    cards_given = []  # The cards that will be generated.
    for i in range(num_times):  # generates cars num_times times
        colour_chosen = POSSIBLE_COLORS[randint(0, 3)]  # Chosen colour
        key_of_value = randint(0, 14)  # Chooses random key for dictionary
        value_chosen = POSSIBLE_VALUES[key_of_value]  # Picks the selected value

        if value_chosen in ["wild", "+4"]:  # Assigns the appropriate display colors
            cards_given.append(Card(value_chosen, ("white", WHITE, 4)))
        else:
            cards_given.append(Card(value_chosen, colour_chosen))
    return cards_given  # Returns the final card option


def sort_cards(cards: list[Card]) -> list[Card]:  # THIS CODE WAS SUGGESTED BY CHATGPT
    """
    Sorts a provided list of cards, grouping them by colours, then by values.
    :return: a list of sorted card objects.
    """
    return sorted(cards, key=lambda card: (card.colour_code, POSSIBLE_VALUES_INVERTED[card.value]))

# def sort_cards(cards: list[Card]) -> list[Card]:
#     """
#     Returns the sorted version of the cards.
#     :return: the sorted list of cards
#     """
#     cvd = {}
#     for card in cards:
#         cv = (card.colour_code, card.value)
#         cvd.setdefault(cv, []).append(card)
#     sorted_cvd = {}
#     final_cards = []
#     while not len(cvd) == 0:
#         minimum_key, minimum_val = cvd.popitem()
#         cvd[minimum_key] = minimum_val
#         for k in cvd:
#             if k[0] < minimum_key[0]:
#                 minimum_key, minimum_val = k, cvd[k]
#         cvd.pop(minimum_key)
#         sorted_cvd[minimum_key] = minimum_val
#
#     while len(sorted_cvd) > 0:
#         cards_key, cards_list = sorted_cvd.popitem()
#         sorted_by_value = []
#         while len(cards_list) > 0:
#             minimum = cards_list[0]
#             for card in cards_list:
#                 if POSSIBLE_VALUES_INVERTED[card.value] < POSSIBLE_VALUES_INVERTED[minimum.value]:
#                     minimum = card
#             cards_list.remove(minimum)
#             sorted_by_value.append(minimum)
#         final_cards.extend(sorted_by_value)
#     return final_cards[::-1]


class GameControls:
    """
    A class for a game.
    === ATTRIBUTES ===
    lop: list of players in this game.
    current_player: the player who has to make their move.
    pile_of_cards: the cards the players have placed for this game.
    """

    def __init__(self, lon: list[str]) -> None:
        """
        Initializes a game.
        :param lon: the list of player names
        :return: None
        """
        self.list_of_players = []
        for name in lon:
            new_player = Player(self, name)
            self.list_of_players.append(new_player)
        create_player_link(self.list_of_players)
        self.current_player = self.list_of_players[randint(0, len(self.list_of_players) - 1)]
        self.pile_of_cards = Pile()
        self._top_card = self.pile_of_cards.top_card
        self._player_wins = False
        self._reverse_order = False
        self._winner = None

    def update_pile(self, card: Card, new_color: str = "white"):
        """
        Places a card at the top of the game's pile.
        """
        self.pile_of_cards.place_card(card)
        self._top_card = self.pile_of_cards.top_card
        if card.value in ["wild", "+4"]:
            self.change_colour(new_color)
        if self.current_player.get_num_cards() == 0:
            self._player_wins, self._winner = True, self.current_player

    def update_game(self, card: Card, new_color: str = "white") -> None:
        """
        A function to update the players cards.
        :param card: the card being placed.
        :param new_color: the new color.
        :return: None
        """
        if card.value in ["rev.", "skip", "wild", "+2", "+4"]:
            if card.value == "skip":
                self.skip_player()
            elif card.value == "rev.":
                self.reverse()
            elif card.value == "+2":
                self.next_player()
                self.add_cards_to_player(2)
            elif card.value == "wild":
                self.change_colour(new_color)
                self.next_player()
            else:
                self.change_colour(new_color)
                self.next_player()
                self.add_cards_to_player(4)
        else:
            self.next_player()

    def check_card_validity(self, card: Card) -> bool:
        """
        Checks if <card> is valid or not.
        :param card: the card to be checked.
        :return: True if card is valid, False otherwise.
        """
        return (self._top_card.colour in ["white", card.colour] or
                card.value == self._top_card.value)

    def next_player(self):
        """
        Moves to the next player.
        """
        if not self._reverse_order:
            self.current_player = self.current_player.next_player
        else:
            self.current_player = self.current_player.prev_player

    def reverse(self):
        """
        Reverses the order of the game.
        """
        self._reverse_order = not self._reverse_order
        self.next_player()

    def skip_player(self):
        """Skips the next player's turn."""
        self.next_player()
        self.next_player()

    def add_cards_to_player(self, num_cards: int = 1):
        """
        Gives cards to the next player.
        """
        self.current_player.draw_card(num_cards)
        self.next_player()

    def change_colour(self, new_colour: str):
        """
        Changes the colour of the game. This is used for wildcards and +4 cards.
        :param new_colour: the new color for the cards following this card.
        """
        self._top_card.colour = new_colour
        for item in POSSIBLE_COLORS:
            if item[0] == new_colour:
                self.pile_of_cards.top_card.display_colour = item[1]

    def get_game_status(self) -> tuple[bool, Optional[Player]]:
        """
        Returns whether any player has won.
        :return: True if a player has won, False otherwise.
        """
        return self._player_wins, self._winner

    def get_leader(self) -> Player:
        """
        Gets the leader of the game.
        :return: the Player leading.
        """
        leader = self.list_of_players[0]
        for player in self.list_of_players:
            if player.get_num_cards() < leader.get_num_cards():
                leader = player
        return leader

    def is_reversed(self) -> bool:
        """
        Returns whether the game is being played in reverse order or not.
        :return: True if reverse, false otherwise.
        """
        return self._reverse_order

    def get_next_player(self, card: Optional[Card]) -> Player:
        """
        Gets the next player.
        :param card: the type of this card determines who is the next player.
        :return: the next player based on the direction of the game.
        """
        if isinstance(card, Card):
            if card.value in ["+2", "+4", "skip"]:
                if self._reverse_order:
                    return self.current_player.prev_player.prev_player
                return self.current_player.next_player.next_player
            elif card.value == "rev.":
                if self._reverse_order:
                    return self.current_player.next_player
                return self.current_player.prev_player
        if self._reverse_order:
            return self.current_player.prev_player
        return self.current_player.next_player


class Pile:
    """
    A class for a pile of cards
    """

    def __init__(self):
        self._pile = []

        colour_chosen = POSSIBLE_COLORS[randint(0, 3)]
        key_of_value = randint(0, 9)
        value_chosen = POSSIBLE_VALUES[key_of_value]
        self.top_card = Card(value_chosen, colour_chosen)

    def place_card(self, card: Card):
        """
        Places a card at the top of the game's pile.
        """
        self._pile.append(card)
        self.top_card = card


class Player:
    """
    A class to represent a player "Node" in a game.
    ===INSTANCE ATTRIBUTES===
    game: the game this player is playing.
    name: the name of this player.
    cards: the cards this player currently holds.
    total_cards: the number of cards this player has remaining.
    === Representation Invariants ===
    len(self.name) > 0
    next_player in game.players
    """
    # Private attributes
    # _cards: the list of cards the player holds.
    # _card_pages: the page of cards
    # _called_uno: whether this player has called uno or not
    name: str
    game: GameControls
    total_cards: int
    next_player: Optional[Player]
    prev_player: Optional[Player]

    def __init__(self, game: GameControls, name: str) -> None:
        """
        Creates a new player object.
        :param game: the game this player is registered to.
        :param name: the name of the player.
        """
        self.name = name
        self._cards = sort_cards(generate_random_card(7))
        self.game = game
        self.next_player = None
        self.prev_player = None
        self._card_pages = {1: self._cards}
        self._called_uno = False

    def place_card(self, next_card: Card, new_color: Optional[str] = None) -> None:
        """
        Sends a command to the registered game to place the card onto the game.
        :param next_card: the card the player wishes to place
        :param new_color: the color of the new card, this is an optional parameter.
        :return: Nothing
        """
        self._cards.remove(next_card)
        self._cards = sort_cards(self._cards)
        if next_card.value not in ["+4", "wild"]:
            self.game.update_pile(next_card, next_card.colour)
        else:
            self.game.update_pile(next_card, new_color)
        self._card_pages = {}
        j = 1
        for i in range(0, len(self._cards), 7):
            self._card_pages[j] = self._cards[i: i + 7]
            j += 1

    def draw_card(self, num_cards: int = 1) -> None:
        """
        The current player picks up a new card. The player's pile of cards are also returned sorted.
        """
        new_card = generate_random_card(num_cards)
        self._cards.extend(new_card)
        self._cards = sort_cards(self._cards)
        self._card_pages = {}
        j = 1
        for i in range(0, len(self._cards), 7):
            self._card_pages[j] = self._cards[i: i + 7]
            j += 1
        if self._called_uno:
            self._called_uno = False

    def call_uno(self) -> None:
        """
        Calls uno for the player.
        :return: Nothing
        """
        self._called_uno = True

    def has_called_uno(self) -> bool:
        """
        Checks whether the player has called uno or not.
        :return: True if called, false otherwise.
        """
        return self._called_uno

    def get_cards(self) -> list[Card]:
        """
        Gets the list of cards.
        :return: the list of cards the player currently has.
        """
        return self._cards

    def get_num_cards(self) -> int:
        """
        Gets the number of cards this player has.
        :return: the number of cards this player has.
        """
        return len(self._cards)

    def get_card_pages(self) -> dict[int, list[Card]]:
        """
        Gets the "pages" of cards for each player
        :return: the card pages.
        """
        return self._card_pages


class Card:
    """
    A class to represent any generic card.
    """

    def __init__(self, value: str, colour: tuple[str, str, int]):
        """
        Initializes the attributes for a card.
        """
        self.value = value
        self.colour = colour[0]
        self.display_colour = colour[1]
        self.colour_code = colour[2]
