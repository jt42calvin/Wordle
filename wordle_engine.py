"""
CS 108 Final Project

This program contains the class used for playing a Wordle game.

@author: Jacob Tocila (jt42)
@author: Kenny Howes (kmh67)
@date: Fall, 2022
"""

import random

# These constants are meant to are used in the method to determine if the letter is in the correct space
WRONG_LETTER_WRONG_SPACE = 0
CORRECT_LETTER_WRONG_SPACE = 1
CORRECT_LETTER_CORRECT_SPACE = 2
# These constants are used when checking if a submitted guess is valid
WRONG_AMOUNT_OF_LETTERS = 30
ALREADY_GUESSED = 31
NOT_RECOGNIZED = 32
# These constants are used after submitting a word. Checks if the win/lose condition is met
WIN = 40
LOSS = 41

class Wordle:
    def __init__(self):
        self._possible_word_list = []
        self._guessed_words = []
        self.attempt_count = 0
        self.solution_word = ''
        for line in open("possible_words.txt", "r"):
            self._possible_word_list.append(line.strip())
        self.start_new_game()

    def start_new_game(self):
        """Restart round specific variables. Clears the guessed word list, assigns a new solution word, and sets the turn count back to 0."""
        self._guessed_words = []
        self.solution_word = random.choice(self._possible_word_list)
        self.attempt_count = 0

    def is_attempt_word_good(self, word_to_check):
        """Checks if the submitted guess word is 5 letters long, in the attempt word list, or in the list of already guessed words."""
        if len(word_to_check) != 5:
            return WRONG_AMOUNT_OF_LETTERS
        if word_to_check not in self._possible_word_list:
            return NOT_RECOGNIZED
        if word_to_check in self._guessed_words:
            return ALREADY_GUESSED
        return True

    def grade_attempt(self, attempt_word):
        """If the submitted guessed word is a valid word:
        increase turn count by 1 add to guessed word list"""
        attempt_word = attempt_word.lower()
        attempt_accepted = self.is_attempt_word_good(attempt_word)
        if attempt_accepted == True:
            # Set up the attempt and specific variables
            self.attempt_count += 1
            self._guessed_words.append(attempt_word)
            not_yet_checked_character_positions = [0,1,2,3,4]
            not_yet_checked_characters = []
            # For ever character in the attempt word
            for char in self.solution_word:
                not_yet_checked_characters.append(char)
            # Algorithm to check given attempt
            # Returns the grading for each letter as a list of integers (numbers to return are defined above this class)
            graded_data = [0] * 5
            for i in range(5):
                if attempt_word[i] == self.solution_word[i]:
                    graded_data[i] = CORRECT_LETTER_CORRECT_SPACE
                    not_yet_checked_character_positions.remove(i)
                    not_yet_checked_characters.remove(attempt_word[i])
            
            for i in not_yet_checked_character_positions:
                if attempt_word[i] in not_yet_checked_characters:
                    graded_data[i] = CORRECT_LETTER_WRONG_SPACE
                    not_yet_checked_characters.remove(attempt_word[i])
                else:
                    graded_data[i] = WRONG_LETTER_WRONG_SPACE
            return graded_data

        # If the attempt is not acceptable
        return attempt_accepted
        
    def check_game_over(self, attempt_word):
        """Returns if the game is won, lost, or ongoing."""
        attempt_word = attempt_word.lower()
        if attempt_word == self.solution_word:
            return(WIN)
        elif self.attempt_count == 6:
            return(LOSS)

if __name__ == "__main__":
    test_engine = Wordle()
    print("Solution word: ", test_engine.solution_word)
    
    # Tests if input is an exact match to solution word
    for letter in test_engine.grade_attempt(test_engine.solution_word):
        assert letter == CORRECT_LETTER_CORRECT_SPACE
    
    # Removes last attempt for manual testing below
    test_engine.attempt_count -= 1

    # Tests if input is not 5 letters
    assert test_engine.grade_attempt("asd") == WRONG_AMOUNT_OF_LETTERS

    # Tests if input has already been guessed
    assert test_engine.grade_attempt(test_engine.solution_word) == ALREADY_GUESSED

    # Tests if input is not a real word. (Or atleast recognized in possible_words.txt)
    assert test_engine.grade_attempt("sasdf") == NOT_RECOGNIZED

    # Allows user to enter attempts to confirm engine runs properly
    done = False
    while not done:
        attempt_word = input(f"Attempt {test_engine.attempt_count + 1}: ")
        feedback = test_engine.grade_attempt(attempt_word)
        if  isinstance(feedback, list):
            for letter_grade in feedback:
                print(letter_grade, end=" ")
            print("- Code meanings are found at the start of this program.")
        else: print(feedback, "- Code meanings are found at the start of this program.")

        ask_if_done = input("Are you done (y/n): ")
        if len(ask_if_done) > 0 and ask_if_done.lower()[0] == "y":
            done = True