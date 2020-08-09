import tkinter as tk

class LetterField(tk.Entry):
    """ A tkinter Entry widget with functionality
        to allow just one letter """
    def __init__(self, master, letter_field_type, letter_field_index, **kw):
        """ Initialize the Entry widget. """
        tk.Entry.__init__(self, master, kw)
        self.master = master
        self.bind('<Key>', self.enter_char)
        self.bind('<KeyRelease>', self.finish_char)
        self.letter_field_type = letter_field_type # "Cipher" or "Plain"
        self.letter_field_index = letter_field_index

    def enter_char(self, key):
        """ Enter the character the user entered
            at the exclusion of all else. """
        entry = key.keysym
        if entry == 'BackSpace':
            self.delete(0, tk.END) # Throw out everything in the field.
            self.master.reverse_tab(self.letter_field_type,
                                    self.letter_field_index)
        elif entry == 'Delete':
            self.delete(0, tk.END) # Throw out everything in the field.
            self.master.tab(self.letter_field_type, self.letter_field_index)            
        elif entry == 'Left':
            self.master.reverse_tab(self.letter_field_type,
                                    self.letter_field_index)
        elif entry == 'Right':
            self.master.tab(self.letter_field_type, self.letter_field_index)
        elif entry == 'Up' or entry == 'Down':
            self.master.switch_line(self.letter_field_type,
                                    self.letter_field_index)
        elif entry == 'Tab':
            pass # Don't throw out the value.
        elif entry == 'Home':
            self.master.home(self.letter_field_type)
        elif entry == 'End':
            self.master.end(self.letter_field_type)
        elif LetterField.is_acceptable(entry):
            if entry == 'quoteright':
                entry = '\''
            else:
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
        if LetterField.is_acceptable(entry):
            if entry == 'space':
                self.delete(0, tk.END) # Throw out everything in the field.
                self.master.tab(self.letter_field_type, self.letter_field_index)
            elif entry != 'BackSpace' and entry != 'Delete' and entry != 'Left' \
               and entry != 'Right' and entry != 'Up' and entry != 'Down' \
               and entry != 'Tab' and entry != 'Home' and entry != 'End':
                if entry == 'quoteright':
                    entry = '\''
                else:
                    entry = entry.upper()
                self.delete(0, tk.END) # Throw out everything in the field.
                self.insert(0, entry)
                self.master.tab(self.letter_field_type, self.letter_field_index)
        elif entry == 'Shift_L' or entry== 'Shift_R':
            pass
        elif len(self.get()) > 0:
            # Get the existing character; it's presumably acceptable.
            self.delete(0, tk.END) # Throw out everything in the field.
            self.insert(0, self.original_value)
        self.master.fill_in_search_field()

    @staticmethod
    def is_acceptable(entry):
        """ Determine if a character is allowed in the field. """
        if entry == '\'' or entry == 'quoteright' or entry == 'BackSpace' \
           or entry == 'Delete' or entry == 'Left' or entry == 'Right' \
           or entry == 'Up' or entry == 'Down' or entry == 'Tab' \
           or entry == 'Home' or entry == 'End' or entry == 'space':
            return True
        if len(entry) != 1:
            return False
        return entry.isalpha()
