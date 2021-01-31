from one_word_solver import OneWordSolver

class WordMapping():
    """ The class to map one ciphertext word to
        its plaintext translation candidates """

    def __init__(self, ciphertext, like_exclusion):
        """ Build an initial list of candidate plaintext
            translations for the given ciphertext word. """
        self._translations = OneWordSolver.solve_word(ciphertext)
        if like_exclusion:
            index = 0
            while index < len(self._translations):
                if WordMapping.violates_like_exclusion\
                        (ciphertext, self._translations[index]):
                    del self._translations[index]
                else:
                    index += 1

    def number_of_candidates(self):
        """ Return the number of candidate words to which
            we're considering translating the ciphertext. """
        return len(self._translations)

    def candidates(self):
        """ Return a list of candidate words to which
            we're considering translating the ciphertext. """
        return self._translations

    @staticmethod
    def violates_like_exclusion(word1, word2):
        """ Determine if a translation of a ciphertext word violates
            like-exclusion. Note that it makes no difference which argument
            is the ciphertext and which the plaintext. This method assumes
            that the two arguments are strings of the same length, that
            they're all the same case, that the only non-alphabetic
            character that might be in them is an apostrophe, and that any
            such apostrophes are in the same position in both strings. """
        for index in range(len(word1)):
            if word1[index] != '\'':
                if word1[index] == word2[index]:
                    return True
        return False
