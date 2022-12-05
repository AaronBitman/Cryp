from one_word_solver import OneWordSolver

class WordMapping():
    """ The class to map one ciphertext word to
        its plaintext translation candidates """

    def __init__(self, ciphertext):
        """ Build an initial list of candidate plaintext
            translations for the given ciphertext word. """
        self._translations = OneWordSolver.solve_word(ciphertext)

    def number_of_candidates(self):
        """ Return the number of candidate words to which
            we're considering translating the ciphertext. """
        return len(self._translations)

    def candidates(self):
        """ Return a list of candidate words to which
            we're considering translating the ciphertext. """
        return self._translations
