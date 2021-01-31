import tkinter as tk
from one_word_interface import OneWordWindow
from puzzle_letter_field import PuzzleLetterField
from enter_ciphertext_window import EnterCiphertextWindow
from word_mapping_group import WordMappingGroup
from cryp_constants import CrypConstants

class Cryp(tk.Tk):
    """ The class for a window for solving a whole cryptogram puzzle """

    def __init__(self, *args, **kwargs):
        """ Initialize the window. """
        tk.Tk.__init__(self, *args, **kwargs)
        # Set the title of the main window.
        self.title('Cryp')
        # Set the size of the main window.
        self.geometry('900x350')

        self.NUMBER_OF_ROWS = 7
        self.CHARACTERS_PER_ROW = 50
        self.row_focus = None
        self.column_focus = None

        # Widgets
        grid_row_index = 1
        self.solution_field = []
        self.letter_field = []
        for row_index in range(self.NUMBER_OF_ROWS):
            self.solution_field.append([])
            self.letter_field.append([])
            for column_index in range(self.CHARACTERS_PER_ROW):
                self.solution_field[row_index].append(PuzzleLetterField(
                    self, row_index, column_index, width=2))
                self.solution_field[row_index][column_index].config(
                    state=tk.DISABLED, justify=tk.CENTER)
                self.letter_field[row_index].append(tk.Label(self))
                self.solution_field[row_index][column_index].grid(
                    row=grid_row_index, column=column_index+1)
                self.letter_field[row_index][column_index].grid(
                    row=grid_row_index+1, column=column_index+1)
            grid_row_index = grid_row_index + 2

        button_populate = tk.Button(self, text = 'Populate',
            command=lambda : self.populate())
        button_solve_word = tk.Button(self, text = 'Solve Word',
            command=lambda : self.solve_word())
        button_clear = tk.Button(self, text = 'Clear',
            command=lambda : self.clear())
        button_populate.grid(row=grid_row_index, column=1, columnspan=5)
        button_solve_word.grid(row=grid_row_index, column=6, columnspan=5)
        button_clear.grid(row=grid_row_index, column = 11, columnspan=5)

        self.freq_by_alpha = tk.Label(self)
        self.freq_by_freq = tk.Label(self)
        grid_row_index = grid_row_index + 1
        self.freq_by_alpha.grid(row=grid_row_index,
            column=1, columnspan=self.CHARACTERS_PER_ROW)
        grid_row_index = grid_row_index + 1
        self.freq_by_freq.grid(row=grid_row_index,
            column=1, columnspan=self.CHARACTERS_PER_ROW)

    def indicate_focus(self, row, column):
        """ Set the row and column of the plaintext field that
            currently has focus, in case we want to know later. """
        self.row_focus = row
        self.column_focus = column

    def populate(self):
        """ Allow the user to fill in the ciphertext. """
        # Note that this function assumes no word will exceed the
        # line length; make sure the validation guarantees that.

        # Open a dialog window to get the ciphertext.
        ciphertext_window = EnterCiphertextWindow(self, title='Enter puzzle')
        # If the user hit Cancel or the "X" button then forget it.
        if ciphertext_window.result == None:
            return
        ciphertext_message, like_exclusion = ciphertext_window.result

        row_index = column_index = 0

        # Break up the message into words.
        ciphertext_words = ciphertext_message.split(' ')
        for word in ciphertext_words:
            if len(word) > 0:
                # If the number of chars left in the line
                # are less than the size of the next word...
                if len(word) > self.CHARACTERS_PER_ROW - column_index:
                    # There aren't enough spaces left in the line
                    # for the word. So fill up the rest of the
                    # row with blanks and start the next row.
                    while column_index < self.CHARACTERS_PER_ROW:
                        self.set_character(row_index, column_index, ' ')
                        column_index = column_index + 1
                    row_index = row_index + 1
                    if row_index >= self.NUMBER_OF_ROWS:
                        # We've run out of space; just quit.
                        break
                    column_index = 0

                # Now that we know the line has sufficient room
                # for the word, enter the word into the puzzle.
                for letter in range(0, len(word)):
                    self.set_character(row_index, column_index, word[letter])
                    column_index = column_index + 1
                # If there's room in the line for a space, add one.
                if column_index < self.CHARACTERS_PER_ROW:
                    self.set_character(row_index, column_index, ' ')
                    column_index = column_index + 1

        # Now that all the words are filled in, fill up
        # the rest of the puzzle with uneditable blanks.
        while row_index < self.NUMBER_OF_ROWS:
            while column_index < self.CHARACTERS_PER_ROW:
                self.set_character(row_index, column_index, ' ')
                column_index = column_index + 1
            row_index = row_index + 1
            column_index = 0

        # Now take a guess at some of the solution by assuming
        # that some of the words are in our dictionary.
        initial_mapping = WordMappingGroup(ciphertext_message, like_exclusion)
        for ciphertext_letter in CrypConstants.LETTERS:
            plaintext_letter = initial_mapping.translate(ciphertext_letter)
            if len(plaintext_letter) == 1:
                self.map(ciphertext_letter, plaintext_letter)

        # Fill in the frequency reports.
        freq_by_alpha, freq_by_freq = self.freq(ciphertext_message)
        self.freq_by_alpha.config(text=freq_by_alpha)
        self.freq_by_freq.config(text=freq_by_freq)

        # Set the focus on the first available space. Users
        # might want that, and it makes it easier to determine
        # focus if the user should want to solve a word.
        self.home(0)

    def freq(self, message):
        """ Given a ciphertext message, return a user-friendly string with
            an alphabetical frequency survey and another user-friendly
            string with the survey in order of frequency. """
        # First run the survey.
        freq_dict = {}
        for letter in CrypConstants.LETTERS:
            freq_dict[letter] = 0
        for letter in message:
            if letter.isalpha():
                freq_dict[letter] = freq_dict[letter] + 1

        # Now generate an alphabetical report.
        alpha_report = 'A:'
        for letter in CrypConstants.LETTERS:
            if letter != 'A':
                alpha_report = alpha_report + ", " + letter + ":"
            alpha_report = alpha_report + str(freq_dict[letter])

        # Now generate a freq-order report.
        freq_by_freq = sorted(freq_dict.items(),
            key=lambda x: x[1], reverse=True)
        letter, current_freq = freq_by_freq[0]
        freq_report = str(current_freq) + ':'
        for item in freq_by_freq:
            letter, new_freq = item
            if new_freq < current_freq:
                freq_report = freq_report + ', ' + str(new_freq) + ':'
                current_freq = new_freq
            freq_report = freq_report + letter

        return alpha_report, freq_report

    def set_character(self, row, column, char_value):
        """ Set a ciphertext character. And if it's not alphabetic, also
            set and disable the corresponding plaintext character. """
        self.solution_field[row][column].delete(0, tk.END)
        if char_value.isalpha():
            self.solution_field[row][column].config(state=tk.NORMAL)
            self.letter_field[row][column].config(text=char_value)
        else:
            self.letter_field[row][column].config(text=char_value)
            # (We need to enable the field first to change the
            # value because we can't change it when it's disabled.)
            self.solution_field[row][column].config(state=tk.NORMAL)
            self.solution_field[row][column].delete(0, tk.END)
            self.solution_field[row][column].insert(0, char_value)
            self.solution_field[row][column].config(state=tk.DISABLED)

    def tab(self, row, column):
        """ Assuming that the focus is on the plaintext space of the given
            row and column, move the focus to the next appropriate space. """
        while True:
            # If it's the end of the row, go to the beginning of the next row.
            if column >= self.CHARACTERS_PER_ROW - 1:
                column = 0
                # If it's the last row, go back to the first row.
                if row >= self.NUMBER_OF_ROWS - 1:
                    row = 0
                else:
                    row = row + 1
            else:
                column = column + 1
            if tk.NORMAL in self.solution_field[row][column].config()['state']:
                # We found the next control.
                self.solution_field[row][column].focus_set()
                return

    def reverse_tab(self, row, column):
        """ Assuming that the focus is on the plaintext space of the given row
            and column, move the focus to the previous appropriate space. """
        while True:
            # If it's the beginning of the row,
            # go to the end of the previous row.
            if column == 0:
                column = self.CHARACTERS_PER_ROW - 1
                # If it's the first row, go to the last row.
                if row == 0:
                    row = self.NUMBER_OF_ROWS - 1
                else:
                    row = row - 1
            else:
                column = column - 1
            if tk.NORMAL in self.solution_field[row][column].config()['state']:
                # We found the next control.
                self.solution_field[row][column].focus_set()
                return

    def change_row(self, row, column, increment):
        """ Assuming that the focus is on the plaintext space of the
            given row and column, move the focus to the next or previous
            row in which the space at that column is enabled. An increment
            of +1 means go down. An increment of -1 means go up. """
        while True:
            row = row + increment
            if row < 0:
                row = self.NUMBER_OF_ROWS - 1
            elif row >= self.NUMBER_OF_ROWS:
                row = 0
            if tk.NORMAL in self.solution_field[row][column].config()['state']:
                # We found the correct control.
                self.solution_field[row][column].focus_set()
                return

    def home(self, row):
        """ Go to the beginning of the given row. """
        column = 0
        while True:
            if tk.NORMAL in self.solution_field[row][column].config()['state']:
                # We found the correct control.
                self.solution_field[row][column].focus_set()
                return
            column = column + 1
            if column >= self.CHARACTERS_PER_ROW:
                # There are no clickable fields in this
                # row. (This should never happen.)
                return
    
    def end(self, row):
        """ Go to the end of the given row, assuming
            it has at least one permitted space. """
        column = self.CHARACTERS_PER_ROW - 1
        while True:
            if tk.NORMAL in self.solution_field[row][column].config()['state']:
                # We found the correct control.
                self.solution_field[row][column].focus_set()
                return
            column = column - 1
            if column <= 0:
                # There are no clickable fields in this
                # row. (This should never happen.)
                return

    def translate_across_the_board(self, row, column):
        """ Given the row and column of one ciphertext character, translate
            it to a plaintext character throughout the puzzle. """
        ciphertext = self.letter_field[row][column].config()['text'][4]
        plaintext = self.solution_field[row][column].get()
        self.map(ciphertext, plaintext)

    def map(self, ciphertext, plaintext):
        """ Translate the given ciphertext letter to the
            given plaintext letter throughout the puzzle. """
        for row_index in range(self.NUMBER_OF_ROWS):
            for column_index in range(self.CHARACTERS_PER_ROW):
                if self.letter_field[row_index][column_index].\
                   config()['text'][4] == ciphertext:
                    self.solution_field[row_index][column_index].\
                        delete(0, tk.END)
                    self.solution_field[row_index][column_index].\
                        insert(0, plaintext)

    def solve_word(self):
        """ Open the window to solve one word. """
        OneWordWindow(self)

    def current_word_location(self):
        """ Determine the starting and ending columns of the
            word in which one character has focus and the
            ciphertext word and its known plaintext. """
        # If there's no focus then forget it.
        if self.row_focus == None or self.column_focus == None:
            return None, None, None, None
        
        start_column_index = self.column_focus
        ciphertext_word = self.letter_field\
            [self.row_focus][start_column_index].config('text')[4]
        plaintext_word = self.plaintext_representation(
            self.row_focus, start_column_index)
        while self.column_is_part_of_word(start_column_index-1):
            start_column_index = start_column_index - 1
            ciphertext_word = self.letter_field[self.row_focus]\
                [start_column_index].config('text')[4] + ciphertext_word
            plaintext_word = self.plaintext_representation(
                self.row_focus, start_column_index) + plaintext_word
        end_column_index = self.column_focus
        while self.column_is_part_of_word(end_column_index+1):
            end_column_index = end_column_index + 1
            ciphertext_word = ciphertext_word + self.letter_field\
                [self.row_focus][end_column_index].config('text')[4]
            plaintext_word = plaintext_word + self.plaintext_representation(
                self.row_focus, end_column_index)
        return self.row_focus, start_column_index, \
                ciphertext_word, plaintext_word

    def plaintext_representation(self, row, column):
        """ Give a representation of the plaintext at a given
            row and column. A letter or apostrophe is acceptable; 
            represent anything else with an underscore. """
        temp = self.solution_field[row][column].get()
        if temp.isalpha() or temp == '\'':
            return temp
        return '_'

    def column_is_part_of_word(self, column):
        """ Assuming one row has focus, determine if a
            given plaintext character is part of a word. """
        if column < 0:
            return False
        if column >= self.CHARACTERS_PER_ROW:
            return False
        ciphertext = self.letter_field[self.row_focus][column].\
                     config()['text'][4]
        if ciphertext.isalpha():
            return True
        if ciphertext == '\'':
            return True
        return False

    def assign_one_word_plaintext(self, row, column, cipherword, plainword):
        """ The user has decided (or guessed) that one ciphertext
            word is a certain plaintext word. Fill in the plaintext
            word and translate accordingly across the board. """
        # But first validate it. That is to say make sure the
        # ciphertext word is still where it was when the one-word
        # interface was opened. After all, the user might have
        # populated the window with a different puzzle by now.
        if self.ciphertext_is_where_it_was(row, column, cipherword):
            for index in range(len(cipherword)):
                self.map(cipherword[index], plainword[index])

    def ciphertext_is_where_it_was(self, row, start_column, cipherword):
        """ Make sure a ciphertext word is where we expect it to be. """
        index = start_column
        for cipherletter in cipherword:
            if cipherletter != self.letter_field[row][index].config('text')[4]:
                return False
            index = index + 1
        return True

    def known_plaintext(self, ciphertext_exceptions):
        """ Get a non-repeating set of all plaintext letters in the puzzle
            that are solved in the interface, except for those letters
            whose ciphertext is in the "ciphertext_exceptions" argument. """
        temp = ""
        for row_index in range(self.NUMBER_OF_ROWS):
            for column_index in range(self.CHARACTERS_PER_ROW):
                temp += self.addition_to_known_plaintext(row_index,
                        column_index, temp, ciphertext_exceptions)
        return temp

    def addition_to_known_plaintext(self, row_num,
            column_num, plaintext_so_far, ciphertext_exceptions):
        """ Determine what to add to the known plaintext list
            based on the data at the given row and column. """
        plaintext_at_this_point = self.solution_field[row_num][column_num].get()
        if plaintext_at_this_point is None:
            return ""
        plaintext_at_this_point = plaintext_at_this_point.strip()
        if len(plaintext_at_this_point) < 1:
            return ""
        plaintext_at_this_point = plaintext_at_this_point[0]
        if plaintext_at_this_point < 'A' or plaintext_at_this_point > 'Z':
            return ""
        if plaintext_at_this_point in plaintext_so_far:
            return ""
        ciphertext_at_this_point = self.letter_field\
                [row_num][column_num].config()['text'][4]
        # If the plaintext at this point is alphabetic,
        # presumably the ciphertext is too.
        if ciphertext_at_this_point in ciphertext_exceptions:
            return ""
        return plaintext_at_this_point
        

    def clear(self):
        """ Clear all the editable fields. """
        for row_index in range(self.NUMBER_OF_ROWS):
            for column_index in range(self.CHARACTERS_PER_ROW):
                if tk.NORMAL in self.solution_field[row_index][column_index]\
                       .config()['state']:
                    self.solution_field[row_index][column_index].delete(
                        0, tk.END)

    def confirm_word(self, row, column, ciphertext):
        """ Confirm that a given ciphertext word is where it was.
            (It might not be if the user changed the puzzle.
            Return True if the word is there, False otherwise. """
        column_index = column
        for cipherchar in ciphertext:
            if column_index >= self.CHARACTERS_PER_ROW:
                return False
            if self.letter_field[row][column_index].config('text')[4] \
                    != cipherchar:
                return False
            column_index += 1
        return True

if __name__ == '__main__':
    app = Cryp()
