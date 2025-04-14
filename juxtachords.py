#!/usr/bin/env python3

#
# juxtachords - command line tool to put notes in a grid of sorts to see how they (don't?) share notes
#
#   Usage: juxtachords chord1 [chord2 [chord3 [... chord-N]]]
#
# So using it with:
#
#   Dm7 G7 Cmaj7
#
# Gives -
#
#               C       C#      D       D#      E       F       F#      G       G#      A       A#      B
#
#       Dm7     C               D                       F                               A
#       G7                      D                       F               G                               B
#       Cmaj7   C                               E                       G                               B
#
#
# The interesting Mingus package - https://github.com/bspaans/python-mingus - does all the heavy lifting.
# Gives an error if Mingus doesn't recognize the chord in question.
# 
# Date: Mar 27th 2024
# Version: .01
# Author: zen
#

#
# Requires python3 and the mingus and colorama packages - e.g. "pip3 install mingus colorama"
#

#
# simple package checking
#
import importlib.util
import sys

failzor = False
for pkg in ["mingus", "colorama"]:
    _pkg = importlib.util.find_spec(pkg)
    if _pkg is None:
        print("*** Requires the '%s' package to run" % pkg)
        failzor = True

if failzor:
    print("\nbailin' out - install the required packages before running...\n")
    sys.exit(2)

from   colorama           import *
from   mingus.core.chords import from_shorthand 
import mingus.core.notes as notes

#
# simple usage sanity check
#
chordz = sys.argv[1:]

if not chordz:
    print("Usage: %s chord1 [c2 [c3 [... cN]]]" % sys.argv[0])
    sys.exit(1)

# 0=C, etc.
all_notez = [0,1,2,3,4,5,6,7,8,9,10,11]

#
# print notes at top... let's assume something works, or this is rather silly, but hey
#
print("        ", end="")
for n in all_notez:
    # print(Fore.LIGHTBLUE_EX + "{:>7s}".format(notes.int_to_note(n)), end="")
    print(Fore.LIGHTBLUE_EX + "%-8s" % notes.int_to_note(n), end="")

print(Style.RESET_ALL)

print("")

for chord in chordz:

    # skip blanks
    if chord.isspace():
        continue

    # ensure the first letter is capitalized
    chord = ' '.join(chord[0].upper() + c[1:] for c in chord.split())

    try:
        notez = from_shorthand(chord)

        print(Fore.LIGHTMAGENTA_EX + "%-8s" % chord + Style.RESET_ALL, end="")

        n_in_chord = [notes.note_to_int(note) for note in notez]

        for n in all_notez:
            if n in n_in_chord:
                print("%-8s" % (notes.int_to_note(n)), end="")
            else:
                print('%8s' % " ", end="")

        print("")

    except Exception as e:
        print(e)
        sys.stderr.write("... grr, couldn't get notes from chord....\n")

print("")

