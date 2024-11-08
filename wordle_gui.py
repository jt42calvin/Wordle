"""
CS 108 Final Project

This program sets up a GUI to play a Wordle game. Made with guizero.

@author: Jacob Tocila (jt42)
@author: Kenny Howes (kmh67)
@date: Fall, 2022
"""

from wordle_engine import *
from guizero import App, Text, Box
from wordle_keyboard import Keyboard, QWERTY_LAYOUT

# Colors
GREEN = "#1ef967"
YELLOW = "#f3db0f"
WHITE = "#fafafa"
DARK_GREY = "#787878"

# Gradient hex values provided by https://hexcolorblender.vercel.app/. Red and yellow bounds set by Calvin University's brand identity standards: https://calvin.edu/dotAsset/f784aa74-291f-45b1-b45c-d6455663bcb4
GRADIENT = ['#481d52', '#4c1e54', '#4f1f56', '#532057', '#562159', '#5a235b', '#5e245c', '#62255e', '#652660', '#692761', '#6d2863', '#712964', '#742a66', '#782c67', '#7c2d68', '#802e6a', '#842f6b', '#88306c', '#8c326d', '#8f336f', '#933470', '#973571', '#9b3772', '#9f3873', '#a33974', '#a73b75', '#ab3c76', '#af3e77', '#b33f77', '#b74178', '#ba4279', '#be447a', '#c2457a', '#c6477b', '#ca487c', '#ce4a7c', '#d24c7d', '#d54d7d', '#d94f7e', '#dd517e', '#df527c', '#e0527a', '#e15378', '#e35476', '#e45574', '#e55672', '#e65770', '#e7586e', '#e8596c', '#e95b6a', '#ea5c68', '#eb5d66', '#ec5f64', '#ec6062', '#ed6261', '#ed635f', '#ee655d', '#ee665b', '#ee6859', '#ef6a57', '#ef6c55', '#ef6d53', '#ef6f51', '#ef714f', '#ef734d', '#ee754b', '#ee7749', '#ee7848', '#ed7a46', '#ed7c44', '#ec7e42', '#ec8040', '#eb823f', '#ea843d', '#ea863b', '#e9883a', '#e88a38', '#e78c37', '#e68e35', '#e98a39', '#eb863d', '#ee8241', '#f07f45', '#f17b49', '#f3774e', '#f47352', '#f57057', '#f56d5c', '#f56961', '#f56666', '#f4646a', '#f3616f', '#f25f74', '#f05d79', '#ee5b7e', '#ec5a83', '#e95888', '#e6588d', '#e25792', '#de5797', '#da579b', '#d658a0', '#d158a4', '#cb59a8', '#c55aac', '#bf5cb0', '#b95db4', '#b25eb7', '#ab60ba', '#a361bd', '#9b63bf', '#9364c2', '#8a66c4', '#8167c5', '#7768c7', '#6d6ac8', '#616bc9', '#556cc9', '#566dca', '#576ecb', '#586fcc', '#5970cd', '#5a72ce', '#5b73cf', '#5b74d0', '#5c75d1', '#5d76d2', '#5e77d3', '#5f78d3', '#6079d4', '#617ad5', '#627cd6', '#637dd7', '#647ed8', '#657fd9', '#6680da', '#6781db', '#6882dc', '#6983dd', '#6a85de', '#6a86df', '#6b87e0', '#6c88e1', '#6d89e2', '#6e8ae3', '#6f8be4', '#708de5', '#718ee6', '#728fe6', '#7390e7', '#7491e8', '#7592e9', '#7693ea', '#7795eb', '#7896ec', '#7997ed', '#7a98ee']
GRADIENT_FORWARD = 1
GRADIENT_REVERSE = -1

class WordleGUI:
    def __init__(self, app):
        app.width, app.height = 349, 500
        app.icon = "red_yellow_icon_small.png"
        app.title="Super Wordle"
        app.when_key_pressed = self.key_press
        self.window = app

        # Set up keyboard
        self.keyboard_box = Box(app, align="bottom")
        self.keyboard = Keyboard(self.keyboard_box,
                                when_key_pressed=self.add_character_to_attempt, 
                                when_back_pressed=self.remove_character_from_attempt, 
                                when_clear_pressed=self.clear_attempt,
                                when_enter_pressed=self.make_attempt,
                                when_cheat_pressed=self.cheat)
        self.key_color = self.keyboard.key_color
        # Keys that have different colors from previous attempts
        self.graded_keys = {}

        # Set up text object to send messages to the user
        self.message = Text(master=app, width="fill", font="Times New Roman", size=17, align="bottom")

        # Sets up the list to contain the thirty letters between the six attempts with five letters each
        self.letter_grid = []
        # Set the acutal attempt grid
        self.set_up_attempt_rows()
        # Initialize the currect attempt word
        self.attempt_word = ''
        
        # Starting the background gradient animation
        self.background_frame = 0
        self.gradient_direction = GRADIENT_FORWARD
        app.repeat(128, self.animate_background)

    def key_press(self, event):
        if event.key.isalpha():
            self.add_character_to_attempt(event.key)
        # \r relates to return
        elif event.key == "\r":
            self.make_attempt()
        # \b relates to backspace
        elif event.key == "\b":
            self.remove_character_from_attempt()
    
    def add_character_to_attempt(self, char_to_add):
        if len(self.attempt_word) < 5:
            self.attempt_word += char_to_add
            row = wordle.attempt_count
            self.letter_grid[row][len(self.attempt_word) - 1].value = char_to_add.upper()
    
    def remove_character_from_attempt(self):
        self.attempt_word = self.attempt_word[:-1]
        row = wordle.attempt_count
        self.letter_grid[row][len(self.attempt_word)].value = ''

    def clear_attempt(self):
        self.attempt_word = ''
        row = wordle.attempt_count
        for letter in self.letter_grid[row]:
            letter.value = ''
    
    def make_attempt(self):
        self.clear_message()
        self.print_attempt(wordle.grade_attempt(self.attempt_word))
        game_over_value = wordle.check_game_over(self.attempt_word)
        self.attempt_word = ''
        if game_over_value == WIN:
            self.send_message(f"You win! The word was '{wordle.solution_word.upper()}'.", GREEN, clear=False)
            self.keyboard.disable_keyboard()
            self.window.after(5000, self.end_game)
        elif game_over_value == LOSS:
            self.send_message(f"Game over! The word was '{wordle.solution_word.upper()}'.", WHITE, clear=False)
            self.keyboard.disable_keyboard()
            self.window.after(5000, self.end_game)
    
    def print_attempt(self, graded_attempt_data):
        # The first three branches handle invalid attempts
        if graded_attempt_data == WRONG_AMOUNT_OF_LETTERS:
            self.send_message(f"'{self.attempt_word.upper()}' is not five characters!")
            self.clear_attempt()
        elif graded_attempt_data == ALREADY_GUESSED:
            self.send_message(f"'{self.attempt_word.upper()}' has already been guessed!")
            self.clear_attempt()
        elif graded_attempt_data == NOT_RECOGNIZED:
            self.send_message(f"'{self.attempt_word.upper()}' is not recognized!")
            self.clear_attempt()
        # If word is valid
        else:
            # The engine comes first and increases attempt count by 1, so 1 is subtracted here to counteract that increase
            row = wordle.attempt_count - 1
            for i in range(len(graded_attempt_data)):
                # Handles "green" case
                if graded_attempt_data[i] == CORRECT_LETTER_CORRECT_SPACE:
                    self.letter_grid[row][i].text_color = GREEN
                    self.letter_grid[row][i].value = f"{self.attempt_word[i].upper()}"
                    # Set color of key. Dictionary key here is an index to get the actual key object from the keyboard.
                    self.graded_keys[QWERTY_LAYOUT.index(self.attempt_word[i].upper())] = GREEN

                # Handles "yellow" case
                elif graded_attempt_data[i] == CORRECT_LETTER_WRONG_SPACE:
                    self.letter_grid[row][i].text_color = YELLOW
                    self.letter_grid[row][i].value = f"{self.attempt_word[i].upper()}"
                    # Makes sure not to override key color if the current key color is of a higher rank (green > yellow > grey)
                    key_of_graded_letter = QWERTY_LAYOUT.index(self.attempt_word[i].upper())
                    if key_of_graded_letter in self.graded_keys:
                        if self.graded_keys[key_of_graded_letter] != GREEN:
                            # Set color of key. Dictionary key here is an index to get the actual key object from the keyboard.
                            self.graded_keys[key_of_graded_letter] = YELLOW
                    else:
                        # Set color of key. Dictionary key here is an index to get the actual key object from the keyboard.
                        self.graded_keys[key_of_graded_letter] = YELLOW
                
                # Handles "red" case
                elif graded_attempt_data[i] == WRONG_LETTER_WRONG_SPACE:
                    self.letter_grid[row][i].text_color = WHITE
                    self.letter_grid[row][i].value = f"{self.attempt_word[i].upper()}"
                    # Makes sure not to override key color if the current key color is of a higher rank (green > yellow > grey)
                    key_of_graded_letter = QWERTY_LAYOUT.index(self.attempt_word[i].upper())
                    if key_of_graded_letter in self.graded_keys:
                        if self.graded_keys[key_of_graded_letter] != GREEN and self.graded_keys[key_of_graded_letter] != YELLOW:
                            # Set color of key. Dictionary key here is an index to get the actual key object from the keyboard.
                            self.graded_keys[key_of_graded_letter] = DARK_GREY
                    else:
                        # Set color of key. Dictionary key here is an index to get the actual key object from the keyboard.
                        self.graded_keys[key_of_graded_letter] = DARK_GREY

    def set_up_attempt_rows(self):
        for i in range(6):
            attempt_box = Box(master=self.window, align="top", height=40, width=200, layout="grid")
            individual_letter_boxes = []
            self.individual_letter_texts = []
            for i in range(5):
                letter_box = Box(attempt_box, grid=[i,0], height=40, width=40)
                individual_letter_boxes.append(letter_box)
                self.individual_letter_texts.append(Text(letter_box, font="Times New Roman", size=24))
            self.letter_grid.append(self.individual_letter_texts)

    
    def send_message(self, message_to_send, message_color = "white", clear = True, time_to_clear_after = 5000):
        self.message.value = message_to_send
        self.message.text_color = message_color
        self.message.cancel(self.clear_message)
        if clear: self.message.after(time_to_clear_after, self.clear_message)
    
    def clear_message(self):
        # The text value is changed instead of using the hide method to prevent a screen stutter effect
        self.message.value = ""
    
    def animate_background(self):
        if self.background_frame + 1 == len(GRADIENT): self.gradient_direction = GRADIENT_REVERSE
        elif self.background_frame - 1 == -1: self.gradient_direction = GRADIENT_FORWARD
        self.background_frame += self.gradient_direction
        self.window.bg = GRADIENT[self.background_frame]
        for box in self.keyboard.widgets:
            box.bg = self.key_color
        for key_index, value in self.graded_keys.items():
            self.keyboard.keys[key_index].bg = value
    
    def end_game(self):
        new_game_answer = self.window.yesno("Ready for more?", "This is it. Don't get scared now. Play another?")
        if new_game_answer: 
            wordle.start_new_game()
            self.clear_round_specifics()
            self.keyboard.enable_keyboard()
        else: 
            self.window.info("Just wow.", "Coward.")
            self.window.destroy()
    
    def clear_round_specifics(self):
        self.graded_keys.clear()
        for attempt_row in self.letter_grid:
            for letter in attempt_row:
                letter.value = ''
                letter.text_color = "black"
        self.message.value = ("")

    def cheat(self):
        going_to_cheat = self.window.yesno("Seriously...", "Really dude... You really wanna cheat?")
        if going_to_cheat: self.window.info("C'mon bro...", f"The answer is '{wordle.solution_word}'")
        else: self.window.info("Fistbump!", "Good choice!")

if __name__ == "__main__":
    app = App()
    wordle = Wordle()
    game = WordleGUI(app)
    app.display()