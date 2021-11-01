import tkinter as tk
from tkinter import messagebox
from letter_field import LetterField
from one_word_solver import OneWordSolver
from copy import copy
from cryp_constants import CrypConstants

class OneWordWindow(tk.Toplevel):
    """ The class for a window for solving one word """

    def __init__(self, master):
        """ Initialize the window. """
        tk.Toplevel.__init__(self)
        # Set the title of the main window.
        self.title('Solve one word')
        # Set the size of the main window.
        self.geometry('450x350')

        # Keep a reference to the master puzzle window.
        self.master = master

        # See the current word, if there is one.
        self.puzzle_start_row, self.puzzle_start_column, \
                puzzle_cipherword, puzzle_plainword = \
                master.current_word_location()

        # Plaintext Widgets
        plain_label = tk.Label(self, text = 'Plain:')
        self.plaintext_value = []
        self.plaintext_control = []
        for i in range(CrypConstants.MAXIMUM_WORD_SIZE):
            self.plaintext_value.append(tk.StringVar())
            self.plaintext_control.append(LetterField(self,
                letter_field_type = "Plain", letter_field_index = i,
                textvariable=self.plaintext_value[i], width=2))

        # Ciphertext Widgets
        cipher_label = tk.Label(self, text = 'Cipher:')
        self.ciphertext_value = []
        self.ciphertext_control = []
        for i in range(CrypConstants.MAXIMUM_WORD_SIZE):
            self.ciphertext_value.append(tk.StringVar())
            self.ciphertext_control.append(LetterField(self,
                letter_field_type = "Cipher", letter_field_index = i,
                textvariable=self.ciphertext_value[i], width=2))

        # Feedback on how the program will interpret the ciphertext word
        search_for_label = tk.Label(self, text = 'Search for:')
        self.search_for_value = ''
        self.search_for = tk.Label(self)

        # More user controls
        button_solve = tk.Button(self, text = 'Solve',
            command=lambda : self.solve())
        button_clear = tk.Button(self, text = 'Clear',
            command=lambda : self.clear())
        self.like_exclusion = tk.BooleanVar()
        self.like_exclusion_control = tk.Checkbutton(self,
            text='Like-exclusion', variable=self.like_exclusion)
        self.use_puzzle = tk.BooleanVar()
        self.use_puzzle_control = tk.Checkbutton(self,
            text='Use Puzzle', variable=self.use_puzzle)

        # Display for solutions
        scrollbar = tk.Scrollbar(self, orient="vertical")
        self.solutions = tk.Listbox(self, yscrollcommand=scrollbar.set)
        self.solutions.bind('<Button-1>', self.allow_answer_selection)
        self.solutions.bind('<Double-1>', self.select_word)
        scrollbar.config(command=self.solutions.yview)
        self.total = tk.Label(self)

        # Geometry
        plain_label.grid(row=1, column=1)
        for i in range(CrypConstants.MAXIMUM_WORD_SIZE):
            self.plaintext_control[i].grid(row=1, column=i+2)

        cipher_label.grid(row=2, column=1)
        for i in range(CrypConstants.MAXIMUM_WORD_SIZE):
            self.ciphertext_control[i].grid(row=2, column=i+2)

        search_for_label.grid(row=3, column=1, columnspan=2)
        self.search_for.grid(row=3, column=3,
            columnspan=CrypConstants.MAXIMUM_WORD_SIZE - 2, sticky='W')
        
        button_solve.grid(row=4, column=2, columnspan=3)
        button_clear.grid(row=4, column=5, columnspan=3)
        self.like_exclusion_control.grid(row=4, column=8, columnspan=6)
        self.use_puzzle_control.grid(row=4, column=14, columnspan=6)

        self.solutions.grid(row=5, column=1,
            columnspan=CrypConstants.MAXIMUM_WORD_SIZE-1, sticky='EW')
        scrollbar.grid(row=5, column=CrypConstants.MAXIMUM_WORD_SIZE,
                       sticky='NS')
        self.total.grid(row=6, column=1,
                        columnspan = CrypConstants.MAXIMUM_WORD_SIZE)

        # And we may want a "Select Word" button as well.
        self.button_select_word = tk.Button(self, text='Select word',
            command=lambda : self.select_word(None))
        # But don't display it yet.

        # If we're drawing data from the Cryp window...
        self.puzzle_row = master.row_focus
        if self.puzzle_row != None:
            # ...then remember the puzzle's data for the future...
            self.puzzle_cipherword = puzzle_cipherword
            
            # ...and prepopulate this interface.
            for index in range(len(puzzle_cipherword)):
                self.ciphertext_value[index].set(puzzle_cipherword[index])
                if puzzle_plainword[index] != '_':
                    self.plaintext_value[index].set(puzzle_plainword[index])
            self.fill_in_search_field()
            # But because this is the first time, set the puzzle row again;
            # this is still the initial value for the ciphertext.
            self.puzzle_row = master.row_focus

        # Set the focus.
        self.ciphertext_control[0].focus_set()

    def tab(self, letter_field_type, letter_field_index):
        """ Move the focus to the next space. """
        if letter_field_index < CrypConstants.MAXIMUM_WORD_SIZE - 1:
            if letter_field_type == 'Plain':
                self.plaintext_control[letter_field_index+1].focus_set()
            elif letter_field_type == 'Cipher':
                self.ciphertext_control[letter_field_index+1].focus_set()

    def reverse_tab(self, letter_field_type, letter_field_index):
        """ Move the focus to the previous space. """
        if letter_field_index > 0:
            if letter_field_type == 'Plain':
                self.plaintext_control[letter_field_index-1].focus_set()
            elif letter_field_type == 'Cipher':
                self.ciphertext_control[letter_field_index-1].focus_set()

    def switch_line(self, letter_field_type, letter_field_index):
        """ Move the focus from the cipher line
            to the plain line or vice versa. """
        if letter_field_type == 'Plain':
            self.ciphertext_control[letter_field_index].focus_set()
        elif letter_field_type == 'Cipher':
            self.plaintext_control[letter_field_index].focus_set()

    def home(self, letter_field_type):
        """ Move the focus to the beginning of the line. """
        if letter_field_type == 'Plain':
            self.plaintext_control[0].focus_set()
        elif letter_field_type == 'Cipher':
            self.ciphertext_control[0].focus_set()

    def end(self, letter_field_type):
        """ Move the focus to the beginning of the line. """
        if letter_field_type == 'Plain':
            self.plaintext_control[CrypConstants.MAXIMUM_WORD_SIZE - 1].focus_set()
        elif letter_field_type == 'Cipher':
            self.ciphertext_control[CrypConstants.MAXIMUM_WORD_SIZE - 1].focus_set()

    def determine_ciphertext(self):
        """ Determine the ciphertext word. """
        temp = ""
        for i in range(CrypConstants.MAXIMUM_WORD_SIZE):
            possible_char = self.ciphertext_control[i].get()
            if possible_char != '':
                temp = temp + possible_char
            else:
                return temp
        return temp

    def fill_in_search_field(self):
        """ Fill in the search field with the "official" ciphertext. """
        # First determine the new value.
        self.search_for_value = self.determine_ciphertext()
        # If it's different from the old value...
        if self.search_for_value != self.search_for.config()['text'][4]:
            # ...then change it...
            self.search_for.config(text=self.search_for_value)
            # ...and prohibit the user from
            # selecting a word here for the puzzle.
            self.button_select_word.grid_forget()
        
    def solve(self):
        """ Provide all known solutions for a word. """

        # (But first clear the Listbox of any existing content.)
        self.solutions.delete(0, tk.END)
        # (And therefore hide the Select Word button.)
        self.button_select_word.grid_forget()

        solutions = copy(OneWordSolver.solve_word(self.search_for_value))
        
        # Remove all words that conflict with the known plaintext.
        index = 0
        while index < len(solutions):
            if self.conflicts_with_plaintext(
                    solutions[index], self.like_exclusion.get()):
                del(solutions[index])
            else:
                index = index + 1

        # If the user checked the "Use Puzzle" option...
        if self.use_puzzle.get():
            # ...then exclude any words with a character that matches any
            # plaintext character in the puzzle, except for those whose
            # corresponding ciphertext characters appear in THIS window.
            letters_to_exclude = self.master.known_plaintext\
                    (self.search_for_value)
            index = 0
            while index < len(solutions):
                if self.have_common_characters(
                        solutions[index], letters_to_exclude):
                    del(solutions[index])
                else:
                    index = index + 1

        for solution in solutions:
            self.solutions.insert(tk.END, solution)

        if len(solutions) == 1:
            total = '1 solution found'
        else:
            total = str(len(solutions)) + ' solutions found'
        self.total.config(text = total)

    def conflicts_with_plaintext(self, solution, like_exclusion):
        """ If a word (a candidate solution) conflicts with the known
            plaintext, return True; otherwise return False. """
        for index in range(len(solution)):
            if like_exclusion:
                if solution[index] != '\'':
                    if solution[index] == self.ciphertext_value[index].get():
                        return True
            if self.plaintext_value[index].get() != '':
                if solution[index] != self.plaintext_value[index].get():
                    return True
        return False

    def clear(self):
        """ Clear all data. """
        for i in range(CrypConstants.MAXIMUM_WORD_SIZE):
            self.plaintext_control[i].delete(0, tk.END)
            self.ciphertext_control[i].delete(0, tk.END)
        self.search_for.config(text='')
        self.solutions.delete(0, tk.END)
        self.total.config(text='')
        self.ciphertext_control[0].focus_set()
        # (Also hide the Select Word button.)
        self.button_select_word.grid_forget()

    def allow_answer_selection(self, event):
        """ If the user selected a possible answer and conditions allow
            answer selection, reveal the button to select that answer. """
        if self.puzzle_row != None and self.solutions.size() > 0:
            self.button_select_word.grid(row=7, column=1,
                columnspan=CrypConstants.MAXIMUM_WORD_SIZE-1)

    def select_word(self, ignore):
        """ Copy the plaintext word to the Cryp window. """
        # But first double-check that it's allowed.
        if self.puzzle_row == None:
            return
        # Also double-check that the word is still in the puzzle
        # window where it was when this window was opened.
        # (It might not be if the user changed the puzzle.)
        if not self.master.confirm_word(self.puzzle_row,
                self.puzzle_start_column, self.puzzle_cipherword):
            return
        # Also double-check that the selected
        # plaintext fits the ciphertext in the puzzle.
        plaintext_word = self.solutions.get(self.solutions.curselection()[0])
        if plaintext_word not in \
                OneWordSolver.solve_word(self.puzzle_cipherword):
            return
        # After all that validation, we have the word; select it!        
        self.master.assign_one_word_plaintext(self.puzzle_row,
            self.puzzle_start_column, self.puzzle_cipherword, plaintext_word)

    @staticmethod
    def have_common_characters(string1, string2):
        """ Determine whether two strings have
            at least one common character. """
        for char in string1:
            if char in string2:
                return True
        return False

