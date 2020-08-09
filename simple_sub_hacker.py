""" This file was adapted from "Cracking Codes with Python" by Al Sweigart.
    You can download the source code from https://nostarch.com/crackingcodes .
    This work is licensed under the Creative Commons
    Attribution-NonCommercial-ShareAlike 3.0 United States License.
    To view a copy of this license, visit
    https://creativecommons.org/licenses/by-nc-sa/3.0/us .
"""

from one_word_solver import OneWordSolver
from cryp_constants import CrypConstants
import word_patterns
import re, copy

class SimpleSubHacker():
    """ Come up with a starting solution to a complete puzzle. """

    @staticmethod
    def getBlankCipherletterMapping():
        """ Returns a dictionary value that is a blank cipherletter mapping """
        return {'A': [], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [],
                'H': [], 'I': [], 'J': [], 'K': [], 'L': [], 'M': [], 'N': [],
                'O': [], 'P': [], 'Q': [], 'R': [], 'S': [], 'T': [], 'U': [],
                'V': [], 'W': [], 'X': [], 'Y': [], 'Z': []}

    @staticmethod
    def hackSimpleSub(message, like_exclusion):
        """ Generate an intersected map with possible plaintext
            translations for each ciphertext letter. """
        
        nonLettersOrSpacePattern = re.compile('[^A-Z\s\']')
        # (Note that despite the variable name, Aaron Bitman
        # modified the expression to include apostrophes as well.)
    
        intersectedMap = SimpleSubHacker.getBlankCipherletterMapping()
        cipherwordList = nonLettersOrSpacePattern.sub(
                '', message.upper()).split()

        for cipherword in cipherwordList:
            # Get a new cipherletter mapping for each ciphertext word:
            candidateMap = SimpleSubHacker.getBlankCipherletterMapping()

            wordPattern = OneWordSolver.get_word_pattern(cipherword)
            if wordPattern not in word_patterns.allPatterns:
                continue # This word was not in our dictionary, so continue.

            # Add the letters of each candidate to the mapping:
            for candidate in word_patterns.allPatterns[wordPattern]:
                if like_exclusion:
                    if SimpleSubHacker.conforms_to_like_exclusion(
                            cipherword, candidate):
                        SimpleSubHacker.addLettersToMapping(
                            candidateMap, cipherword, candidate)
                else:
                    SimpleSubHacker.addLettersToMapping(
                        candidateMap, cipherword, candidate)

            # Intersect the new mapping with the existing intersected mapping:
            intersectedMap = SimpleSubHacker.intersectMappings(
                intersectedMap, candidateMap)

        # Remove any solved letters from the other lists:
        return SimpleSubHacker.removeSolvedLettersFromMapping(intersectedMap)

    @staticmethod
    def addLettersToMapping(letterMapping, cipherword, candidate):
        """ The `letterMapping` parameter is a "cipherletter mapping"
            dictionary value of which the return value of this function
            starts as a copy. The `cipherword` parameter is a string value
            of the ciphertext word. The `candidate` parameter is a
            possible English word to which the cipherword could decrypt.

            This function adds the letters of the candidate
            as potential decryption letters for the
            cipherletters in the cipherletter mapping. """

        for i in range(len(cipherword)):
            if candidate[i] != '\'':
                if candidate[i] not in letterMapping[cipherword[i]]:
                    letterMapping[cipherword[i]].append(candidate[i])

    @staticmethod
    def conforms_to_like_exclusion(cipherword, plainword):
        """ Determine if a plaintext candidate conforms to
            like-exclusion for a ciphertext word. This method
            assumes the two arguments are strings of the same length
            with the apostrophe, if any, in the same position. """
        for index in range(len(cipherword)):
            if cipherword[index] != '\'':
                if cipherword[index] == plainword[index]:
                    return False
        return True

    def intersectMappings(mapA, mapB):
        # To intersect two maps, create a blank map, and then add only the
        # potential decryption letters if they exist in BOTH maps.
        intersectedMapping = SimpleSubHacker.getBlankCipherletterMapping()
        
        for letter in CrypConstants.LETTERS:

            # An empty list means "any letter is possible".
            # In this case just copy the other map entirely.
            if mapA[letter] == []:
                intersectedMapping[letter] = copy.deepcopy(mapB[letter])
            elif mapB[letter] == []:
                intersectedMapping[letter] = copy.deepcopy(mapA[letter])
            else:
                # If a letter in mapA[letter] exists in mapB[letter], add
                # that letter to intersectedMapping[letter].
                for mappedLetter in mapA[letter]:
                    if mappedLetter in mapB[letter]:
                        intersectedMapping[letter].append(mappedLetter)

        return intersectedMapping

    def removeSolvedLettersFromMapping(letterMapping):
        """ Cipherletters in the mapping that map to only one letter
            are "solved" and can be removed from the other letters. For
            example, if 'A' maps to potential letters ['M', 'N'], and
            'B' maps to ['N'], then we know that 'B' must map to 'N',
            so we can remove 'N' from the list of the plaintext letters
            to which 'A' could map. So 'A' then maps to ['M']. Note
            that now that 'A' maps to only one letter, we can remove
            'M' from the list of letters for every other letter. (This
            is why there is a loop that keeps reducing the map.) """

        loopAgain = True
        while loopAgain:
            # First assume that we will not loop again:
            loopAgain = False

            # `solvedLetters` will be a list of uppercase letters that
            # have one and only one possible mapping in `letterMapping`:
            solvedLetters = []
            for cipherletter in CrypConstants.LETTERS:
                if len(letterMapping[cipherletter]) == 1:
                    solvedLetters.append(letterMapping[cipherletter][0])

            # If a letter is solved, than it cannot possibly be a potential
            # decryption letter for a different ciphertext letter, so we
            # should remove it from those other lists:
            for cipherletter in CrypConstants.LETTERS:
                for s in solvedLetters:
                    if len(letterMapping[cipherletter]) != 1 and \
                       s in letterMapping[cipherletter]:
                        letterMapping[cipherletter].remove(s)
                        if len(letterMapping[cipherletter]) == 1:
                            # A new letter is now solved, so loop again.
                            loopAgain = True
        return letterMapping

# The following lines were used to test this class.
# cryptogram = "AT JTSJFNYF NUFEI NI FVDNPECEANSZ, QRA NA NI TSPO IEXF GDFS OTR JTSJFNYF IT WESO ADEA OTR EIJCNQF ST RSURF JTSIFLRFSJF AT ADFW ESU JES AEBF ADFW XTC GDEA ADFO ECF GTCAD. KFTKPF GDT JTSJFNYF XFG XNSU NA YFCO UNXXNJRPA STA AT CFZECU ADFW GNAD NSTCUNSEAF CFIKFJA. (G. ITWFCIFA WERZDEW)"
# cryptogram = "VA VGBZ ZR JCUA CB ZIA YKAQABZ, GBT ZIA RBJD ICQZRKD ZIGZ CQ VRKZI G ZCBWAK'Q TGP CQ ZIA ICQZRKD VA PGWA ZRTGD. (IABKD LRKT)"
# print(SimpleSubHacker.hackSimpleSub(cryptogram))
