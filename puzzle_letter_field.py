import tkinter as tk

class PuzzleLetterField(tk.Entry):
    """ A tkinter Entry widget with functionality
        to allow just one letter """
    def __init__(self, master, row, column, **kw):
        """ Initialize the Entry widget. """
        tk.Entry.__init__(self, master, kw)
        self.master = master
        self.bind('<Key>', self.enter_char)
        self.bind('<KeyRelease>', self.finish_char)
        self.bind('<FocusIn>', self.indicate_focus)
        self.row = row
        self.column = column
        self.original_value = ""

    def enter_char(self, key):
        """ Enter the character the user entered
            at the exclusion of all else. """
        entry = key.keysym

        if entry == 'BackSpace':
            self.delete(0, tk.END) # Throw out everything in the field.
            self.master.translate_across_the_board(self.row, self.column)
            self.master.reverse_tab(self.row, self.column)
        elif entry == 'Delete':
            self.delete(0, tk.END) # Throw out everything in the field.
            self.master.translate_across_the_board(self.row, self.column)
            self.master.tab(self.row, self.column)
        elif entry == 'Left':
            self.master.reverse_tab(self.row, self.column)
        elif entry == 'Right':
            self.master.tab(self.row, self.column)
        elif entry == 'Up':
            self.master.change_row(self.row, self.column, -1)
        elif entry == 'Down':
            self.master.change_row(self.row, self.column, 1)
        elif entry == 'Tab':
            pass # Don't throw out the value.
        elif entry == 'Home':
            self.master.home(self.row)
        elif entry == 'End':
            self.master.end(self.row)
        elif PuzzleLetterField.is_acceptable(entry):
            entry = entry.upper()
            self.delete(0, tk.END) # Throw out everything in the field.
            self.insert(0, entry)
        else:
            # If the character is unacceptable, remember
            # the current value for future reference.
            self.original_value = self.get()

    def finish_char(self, key):
        """ Enter the character the user entered
            at the exclusion of all else. """
        entry = key.keysym
        if PuzzleLetterField.is_acceptable(entry):
            if entry == 'space':
                self.delete(0, tk.END) # Throw out everything in the field.
                self.master.tab(self.row, self.column)
            elif entry != 'BackSpace' and entry != 'Delete' and entry != 'Left' \
               and entry != 'Right' and entry != 'Up' and entry != 'Down' \
               and entry != 'Tab' and entry != 'Home' and entry != 'End':
 
                entry = entry.upper()
                self.delete(0, tk.END) # Throw out everything in the field.
                self.insert(0, entry)
                self.master.tab(self.row, self.column)
        elif entry == 'Shift_L' or entry == 'Shift_R':
            pass
        elif len(self.get()) > 0:
            # Get the existing character; it's presumably acceptable.
            self.delete(0, tk.END) # Throw out everything in the field.
            self.insert(0, self.original_value)
        self.master.translate_across_the_board(self.row, self.column)

    def indicate_focus(self, event):
        """ Indicate that this is the letter field that last got focus. """
        self.master.indicate_focus(self.row, self.column)

    @staticmethod
    def is_acceptable(entry):
        """ Determine if a character is allowed in the field. """
        if entry == 'BackSpace' or entry == 'Delete' \
            or entry == 'Left' or entry == 'Right' \
            or entry == 'Up' or entry == 'Down' or entry == 'Tab' \
            or entry == 'Home' or entry == 'End' or entry == 'space':
            return True
        if len(entry) != 1:
            return False
        return entry.isalpha()
