import tkSimpleDialog
import tkinter as tk
from tkinter import messagebox
from cryp_constants import CrypConstants

class EnterCiphertextWindow(tkSimpleDialog.Dialog):
    """ A Class for the window to enter a puzzle. """

    def body(self, master):
        """ Create the Text object in which to enter the ciphertext. """

        # Widgets
        self.puzzle = tk.Text(self)
        self.like_exclusion = tk.BooleanVar()
        self.like_exclusion_control = tk.Checkbutton(self,
            text='Like-exclusion', variable=self.like_exclusion)
        self.puzzle.pack()
        self.like_exclusion_control.pack()
        return self.puzzle # initial focus

    def apply(self):
        """ Close the window and return the ciphertext
            puzzle and the "like-exclusion" setting. """
        self.result = self.puzzle.get(1.0, tk.END).upper()\
            .replace('\n', ' ').replace('\t', ' '), self.like_exclusion.get()

    def validate(self):
        """ Prohibit a word that's too long. """
        ciphertext_words = self.puzzle.get(1.0, tk.END)\
            .replace('\n', ' ').replace('\t', ' ').split(' ')
        for word in ciphertext_words:
            if len(word.strip()) > CrypConstants.MAXIMUM_WORD_SIZE + 3:
                # We allow the longest word plus three characters
                # for two quotes and one punctuation mark.
                messagebox.showerror("Validation error", "The word " + word +
                    " is too long. The maximum size allowed is " +
                    str(CrypConstants.MAXIMUM_WORD_SIZE + 3))
                return False
        return True

