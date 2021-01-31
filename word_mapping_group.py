import re
from word_mapping import WordMapping
from alphabet_mapping import AlphabetMapping

class WordMappingGroup():
    """ The class to map (almost) every word in a puzzle
        to its plaintext translation candidates """

    def __init__(self, puzzle, like_exclusion):
        """ Build the group of word mappings from a puzzle. """
        self._word_dictionary = {}
        # Note that we're temporarily keeping the parentheses
        # to determine whether to include a one-letter word.
        ciphertextWordList = re.compile('[^A-Z\s\'\(\)]')\
                .sub('', puzzle.upper()).split()
        inParentheses = False
        for ciphertextWord in ciphertextWordList:
            if "(" in ciphertextWord:
                inParentheses = True
            ciphertextWordWithoutParentheses = \
                    ciphertextWord.replace('(','').replace(')','')
            if (len(ciphertextWordWithoutParentheses) > 1 or not inParentheses) \
                    and not ciphertextWordWithoutParentheses \
                    in self._word_dictionary.keys():
                word_mapping = WordMapping(ciphertextWordWithoutParentheses,
                                           like_exclusion)
                if word_mapping.number_of_candidates() > 0:
                    self._word_dictionary[ciphertextWordWithoutParentheses] = \
                            word_mapping.candidates()
            if ")" in ciphertextWord:
                inParentheses = False

        # Also, keep an alphabet map.
        self._alphabet_map = AlphabetMapping(like_exclusion)

        # If we can't find a candidate translation for
        # any word, we can't make any guess, so quit.
        if len(self._word_dictionary) == 0:
            return

        # Find our starting point.
        word_to_guess = self._most_promising_word()

        # Now keep paring down the possibilities
        # while we're making good progress.
        while True:
            self._pare_down(word_to_guess)

            # Now determine if this paring down seems to have done
            # sufficient good that another iteration might be worth it.
            # How much good is "sufficient good"? Well, that's debatable.

            # First of all, if all the words are solved (or eliminated because
            # we couldn't find a good translation for them) we've done all we
            # can; how much good we did in this last paring is irrelevant!
            if len(self._word_dictionary) == 0:
                break

            # Second of all, if the best word to guess is different from
            # the one before the paring down, we probably did some good.
            new_word_to_guess = self._most_promising_word()
            if new_word_to_guess != word_to_guess:
                # (And for the next paring down, we
                # now know the most promising word.)
                word_to_guess = new_word_to_guess
                continue

            # Now... if the best word is the same, we might
            # theoretically do more with it in the future, but
            # not using this algorithm. So let's trash it...
            del self._word_dictionary[word_to_guess]
            # ...and unless the word list ran dry...
            if len(self._word_dictionary) == 0:
                break
            # ...pick the next-best word and try again.
            word_to_guess = self._most_promising_word()

    def _most_promising_word(self):
        """ Look through all the words in this mapping and find one that shows
            more promise than (or at least as much promise as) any other
            word for the purpose of narrowing down the possibilities. """
        # First of all, get a list of all the ciphertext words in the mapping.
        # This method assumes that there's at least one entry in the mapping.
        ciphertext_words = list(self._word_dictionary)
        temp = ciphertext_words[0]
        for word in ciphertext_words[1:]:
            temp = self._more_promising_word(temp, word)
        return temp

    def _more_promising_word(self, word_1, word_2):
        """ Given two ciphertext words in the mapping,
            which one is officially more promising? """
        # This method assumes they're not the same
        # word and that they're both in the mapping.

        # The first criterion is the number of candidate
        # plaintext words - the fewer the better.
        if len(self._word_dictionary[word_1]) < \
           len(self._word_dictionary[word_2]):
            return word_1
        if len(self._word_dictionary[word_1]) > \
           len(self._word_dictionary[word_2]):
            return word_2

        # If the plaintext list is the same length for both, the second
        # criterion is the length of the word itself; the longer the better.
        if len(word_1) < len(word_2):
            return word_2
        if len(word_1) > len(word_2):
            return word_1

        # If those two criteria are tied then it's a tossup, but for
        # consistency, let's take the one that comes first alphabetically.
        if word_1 < word_2:
            return word_1
        return word_2

    def _pare_down(self, word_to_guess):
        """ Based on the premise that one word in the puzzle
            is one of the plaintext values in our word map,
            narrow down that word's letters' translations. """
        for index in range(len(word_to_guess)):
            if word_to_guess[index] != '\'':
                plaintext_values = ""
                for plaintext in self._word_dictionary[word_to_guess]:
                    plaintext_values += plaintext[index]
                self._alphabet_map.narrow_down_translations(
                        word_to_guess[index], plaintext_values)

        # Now if the word we guessed has only one translation...
        if len(self._word_dictionary[word_to_guess]) == 1:
            # ...then we did all the good we can with it, so delete it.
            del self._word_dictionary[word_to_guess]

        # Now that the alphabet map is pared down, we can
        # pare down the word translations accordingly.
        # Start by looping through the ciphertext words.
        all_entries = list(self._word_dictionary.keys())
        for entry in all_entries:
            # And for each ciphertext word, loop
            # through the plaintext candidates.
            index = 0
            while index < len(self._word_dictionary[entry]):
                # If a translation doesn't conform, delete it.
                if self._alphabet_map.conforms(entry,
                        self._word_dictionary[entry][index]):
                    index += 1
                else:
                    del self._word_dictionary[entry][index]
            # Furthermore, after deleting some translations, if
            # we find there are no translations left, delete
            # the whole ciphertext entry from the dictionary!
            if len(self._word_dictionary[entry]) == 0:
                del self._word_dictionary[entry]

    def translate(self, ciphertext):
        """ Given a ciphertext letter, return all translations. """
        return self._alphabet_map.translate(ciphertext)
