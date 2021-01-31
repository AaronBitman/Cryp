from cryp_constants import CrypConstants

class AlphabetMapping():
    """ The class to map each ciphertext letter to every
        plaintext letter to which it might possibly translate """

    def __init__(self, like_exclusion):
        """ Build the initial, full (or almost full) mapping. """
        self._letter_dictionary = {}
        for letter in CrypConstants.LETTERS:
            self._letter_dictionary[letter] = CrypConstants.LETTERS
            if like_exclusion:
                self._letter_dictionary[letter] = \
                        self._letter_dictionary[letter].replace(letter, '')

    def delete_translation(self, ciphertext, plaintext):
        """ Note in the mapping that a given ciphertext letter does NOT
            translate to a given plaintext letter, if it's feasible. """
        # (By "feasible" I mean: Don't do it if
        # it reduces the translations to none.)
        if len(self._letter_dictionary[ciphertext]) > 1:
            self._letter_dictionary[ciphertext] = \
                    self._letter_dictionary[ciphertext].replace(plaintext, '')
            # Now... what if that deletion reduced
            # the possible translations to only one?
            if len(self._letter_dictionary[ciphertext]) == 1:
                # That would mean we've determined what translates to
                # the plaintext parameter. So delete that plaintext from
                # the mappings of all the OTHER ciphertext letters.
                # (That's right; this method is potentially recursive.)
                for letter in CrypConstants.LETTERS:
                    if letter != ciphertext:
                        self.delete_translation(letter,
                                self._letter_dictionary[ciphertext])

    def narrow_down_translations(self, ciphertext, plaintext):
        """ Narrow down (potentially) the possible translations of
            of the "ciphertext" argument by asserting that it must
            be one of the letters in the "plaintext" argument. Note
            that this method does NOT assume that the "plaintext"
            argument has no duplicates, or is even in order! """

        # Get the plaintext possibilities we already have.
        current_plaintext = self._letter_dictionary[ciphertext]

        # Note that if we're down to only one possible translation already,
        # there's nothing we can do to narrow it down further so forget it.
        if len(current_plaintext) <= 1:
            return

        # Set the plaintext to the intersection of the
        # current plaintext and the "plaintext" parameter.
        result = ''.join(sorted(set(current_plaintext).
                intersection(plaintext)))
        # There must be at least one translation; otherwise forget it.
        if result == "":
            return

        # Now we can set the translations.
        self._letter_dictionary[ciphertext] = result

        # Now... suppose there's only one translation.
        if len(result) == 1:
            # ...then we've officially determined that's the answer, so we can
            # delete that translation from all the other ciphertext entries.
            for letter in CrypConstants.LETTERS:
                if letter != ciphertext:
                    self.delete_translation(letter, result)

    def conforms(self, ciphertext, plaintext):
        """ If I said that a ciphertext word translates to a
            plaintext word, does that conform to the current alphabet
            mapping? If so, return True; otherwise return False. """
        for index in range(len(ciphertext)):
            if ciphertext[index] != '\'':
                if not plaintext[index] in \
                        self._letter_dictionary[ciphertext[index]]:
                    return False
        return True

    def translate(self, ciphertext):
        """ Given a ciphertext letter, return all translations. """
        return self._letter_dictionary[ciphertext]
