# UNO (Developed in PYGAME)
Welcome to Pygame UNO! This program was developed using python. The game is played
locally on one device.
<h2>Setup</h2>
1. Clone this repository from github.
2. Ensure you have Python 3.11 (or newer) installed
3. Make sure the following libraries are installed:
   - typing
   - random
   - __future__
   - math
   - os
   - time
4. To start the game, simply run "UnoVis.py"

<h2> Starting the game </h2>
The players start by pressing the "start" button when they are ready to set up
the game. On the next screen the players can toggle the number of players, ranging from 2 to 10 players inclusive.
Once the number of players have been decided, the "start" button must be pressed. 

Once the start button is pressed, the game begins. A screen is displayed, asking for the device to be passed to the
starting player, which is picked at random. Once the device is given to the first player and they are ready, they press
anywhere in the window to see their playing hand.

<h2> Screen layout </h2>
Every player sees the following on their screen when playing: 
* **Top-left**: the players and the number of cards they have. 
  * The leader is displayed in yellow, and the current player is displayed in bold text.
  * The "next" player in the current direction is indicated with a "(next)" after their name.
    * The next player and the card count is reflected by the card the cursor is hovering over. 
      * A "skip" card will show the player who plays after the skip card is placed. 
      * A "+2" or "+4" card will display the number of cards the original "next" player will have after the card is placed, and highlight the "next" player to play after the card is placed.
      * A "reverse" card will show the next player if that card is placed.
* **Top-right**: the current direction of gameplay.
  * If the cursor is hovering over a reverse card, the arrow points in the opposite direction to indicate the direction of gameplay if card is placed.
* **Middle**: The top card, the "UNO!" button, and the "draw card" button.
  * "draw card": if this button is pressed, the player picks up a card and their turn is skipped.
  * "uno!": if a player presses this card, it calls UNO! for that player, and draws 2 cards for any players who have not called uno with 1 card left in their hand. If the call is illegal, a "false call" screen is displayed.
* **Bottom**: The playing hand for that player.
  * The cards are sorted by colour then by value. Every player sees segments of up to 7 cards. If they want to see their remaining cards, they scroll up to see the next page, and scroll down to see the previous page. 

<h2>Rules and steps on gameplay</h2>
Refer to: https://www.unorules.com/

<h2>Future updates ️🔮</h2>
1. Allow players to "stack" +2 and +4 cards.

2. Create a timer for each player.
