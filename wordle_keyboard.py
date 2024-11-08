"""
CS 108 Final Project

This program creates a keyboard used to type in characters and execute commands. Made with guizero.

@author: Jacob Tocila (jt42)
@author: Kenny Howes (kmh67)
@date: Fall, 2022
"""

from guizero import Box, PushButton

# The code for the keyboard was modeled after a sample phone dialer program from the GUI unit in class
# The concept is similar but upscaled for A-Z letters instead of 0-9 numbers

KEY_WIDTH = 1
BUTTON_WIDTH = 4
# Letter rows 1-3 are for Q-P, A-L, Z-M respectively. Command row is for Show Stats, Hide Stats, Clear, Backspace, and Enter buttons
        
QWERTY_LAYOUT = ["Q","W","E","R","T","Y","U","I","O","P","A","S","D","F","G","H","J","K","L","Z","X","C","V","B","N","M"]

class Keyboard:
    def __init__(self, master, when_key_pressed = None, when_back_pressed = None, when_enter_pressed = None, when_clear_pressed = None, when_cheat_pressed = None):
        self.when_key_pressed = when_key_pressed
        self.when_back_pressed = when_back_pressed
        self.when_enter_pressed = when_enter_pressed
        self.when_clear_pressed = when_clear_pressed
        self.when_cheat_pressed = when_cheat_pressed
        # Boxes are constructed in reverse order from code
        # A separate box is used for command buttons for keeping things cleaner looking
        self.command_buttons = Box(master, layout = "grid", align="bottom")
        self.letter_buttons_row_three = Box(master, layout = "grid", align="bottom")
        self.letter_buttons_row_two = Box(master, layout = "grid", align="bottom")
        self.letter_buttons_row_one = Box(master, layout = "grid", align="bottom")
        self.widgets = [self.command_buttons, self.letter_buttons_row_one, self.letter_buttons_row_two, self.letter_buttons_row_three]

        self.key_color = "#c9c9c9"
        self.keys = []

        # Different boxes help keep each row of buttons nice and tidy.
        for i in range(len(QWERTY_LAYOUT[0:10])):
            pb = PushButton(self.letter_buttons_row_one, args = QWERTY_LAYOUT[i], text = QWERTY_LAYOUT[i], grid = [i, 0], command=self.press, width=KEY_WIDTH)
            pb.font = "Times New Roman"
            self.keys.append(pb)

        for i in range(len(QWERTY_LAYOUT[10:19])):
            pb = PushButton(self.letter_buttons_row_two, args = QWERTY_LAYOUT[i + 10], text = QWERTY_LAYOUT[i + 10], grid = [i, 1], command=self.press, width=KEY_WIDTH)
            pb.font = "Times New Roman"
            self.keys.append(pb)

        for i in range(len(QWERTY_LAYOUT[19:26])):
            pb = PushButton(self.letter_buttons_row_three, args = QWERTY_LAYOUT[i + 19], text = QWERTY_LAYOUT[i + 19], grid = [i, 2], command=self.press, width=KEY_WIDTH)
            pb.font = "Times New Roman"
            self.keys.append(pb)

        # Having a separate row for command buttons keeps the GUI clean
        cheat_button = PushButton (self.command_buttons, text = "Cheat", grid = [i, 3], command = self.cheat, width=BUTTON_WIDTH)
        cheat_button.font = "Times New Roman"
        clear_button = PushButton(self.command_buttons, text = "Clear", grid = [i + 1, 3], command = self.clear, width=BUTTON_WIDTH)
        clear_button.font = "Times New Roman"
        back_space_button = PushButton(self.command_buttons, text = "Back", grid = [i + 2, 3], command = self.back, width=BUTTON_WIDTH)
        back_space_button.font = "Times New Roman"
        enter_button = PushButton(self.command_buttons, text = "Enter", grid = [i + 3, 3], command = self.enter, width=BUTTON_WIDTH)
        enter_button.font = "Times New Roman"
            
    def cheat(self):
        # This method tells the user what the answer is. Helpful for developers/professors while debugging/grading code!
        if self.when_cheat_pressed != None: self.when_cheat_pressed()
    
    def press(self, key):
        if self.when_key_pressed != None: self.when_key_pressed(key)
    
    def clear(self):
        if self.when_clear_pressed != None: self.when_clear_pressed()
    
    def back(self):
        if self.when_back_pressed != None: self.when_back_pressed()
        
    def enter(self):
        if self.when_enter_pressed != None: self.when_enter_pressed()
    
    def disable_keyboard(self):
        for box in self.widgets:
            box.disable()
    
    def enable_keyboard(self):
        for box in self.widgets:
            box.enable()