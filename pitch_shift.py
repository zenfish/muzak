#!/usr/bin/env python3

#
# shift the pitch of a set of chord(s)/note(s) up or down N semitones
#
# Usage: $0 N-semitones chord/note-1 [chord/note-2 [chord/note-3 [...] ]]   # (use minus-N for going down)
#

import re
import sys

from mingus.containers.note import *
from mingus.core.notes      import *

DEFAULT_OCTAVE = "4"

def shifty(name, semitones):

    try:

        # if doesn't have an octave, assume 4th and add... also convert to mingus note class
        trans     = name

        trans     = Note(trans)

        octave    = trans.octave
        semitones = int(semitones)

        tmp = trans

        #
        # check to see if it creeps up to the the next octave -
        # e.g. going from B->C or vice-versa
        #

        # if positive, go up, one at a time
        if semitones >= 0:
            for _ in range(semitones):
                tmp = notes.augment(tmp.name)
                if reduce_accidentals(Note(tmp).name) == "C":
                    octave = octave + 1
                tmp = Note(tmp + "-" + str(octave))
            trans = tmp
        # if negative, go down, one at a time
        else:
#           print(tmp)
            for _ in range(abs(semitones)):
#               print("pre: %s" % octave)
                tmp = notes.diminish(tmp.name)
                if reduce_accidentals(Note(tmp).name) == "B":
                    octave = octave - 1
                tmp = Note(tmp + "-" + str(octave))
            trans = tmp

        trans = Note(trans)
        base  = reduce_accidentals(trans.name)
        trans = Note(base + "-" + str(octave))

    except Exception as e:
        print(e)
        print("line number: " + str(e.__traceback__.tb_lineno))
        print(usage)
        sys.exit(4)

    # return a string w no quotes
    return str(trans)[1:-1]

#
# use the command line or stdin
#
usage = "Usage: %s N-semitones chord/note-1 [chord/note-2 [chord/note-3 [...] ]]   # (use minus-N for going down)" % sys.argv[0]

try:
    # stdin.. but need to read the pitch shift amount
    if len(sys.argv) == 2:
        semi = sys.argv[1]
        argz = sys.stdin.readline().split()
    elif len(sys.argv) > 2:
        semi = sys.argv[1]
        argz = sys.argv[2:]
    else:
        print(usage)
        sys.exit(1)

except Exception as e:
    print(e)
    print("Usage: %s N-semitones chord/note-1 [chord/note-2 [chord/note-3 [...] ]]   # (use minus-N for going down)" % sys.argv[0])
    sys.exit(1)

for music in argz:
    transed = shifty(music, semi)
    print("%s" % transed, end=" ")

print("")


