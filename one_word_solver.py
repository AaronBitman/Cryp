""" This file was adapted from "Cracking Codes with Python" by Al Sweigart.
    You can download the source code from https://nostarch.com/crackingcodes .
    This work is licensed under the Creative Commons
    Attribution-NonCommercial-ShareAlike 3.0 United States License.
    To view a copy of this license, visit
    https://creativecommons.org/licenses/by-nc-sa/3.0/us .
"""

import word_patterns

class OneWordSolver():
    """ Solve a one-word cryptogram. """

    @staticmethod
    def solve_word(word):
        """ Prints all plaintext translations for a ciphertext word """
        word_pattern = OneWordSolver.get_word_pattern(word)
        try:
            answers = word_patterns.allPatterns[word_pattern][:]
        except:
            answers = []
        return answers
    
    @staticmethod
    def get_word_pattern(word):
        """ Returns a string of the pattern form of the given
            word, e.g. '0.1.2.3.4.1.2.3.5.6' for 'DUSTBUSTER' """
        word = word.upper()
        nextNum = 0
        letterNums = {}
        wordPattern = []

        for letter in word:
            if letter == '\'':
                letterNums[letter] = '\''
            elif letter not in letterNums:
                letterNums[letter] = str(nextNum)
                nextNum += 1
            wordPattern.append(letterNums[letter])
        return '.'.join(wordPattern)
