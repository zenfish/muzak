#!/usr/bin/env python3

#
# XXX I obviously don't understand intervals yet! Hopefully my code does :)
# I need to actually do some reading/investigation... could probably could use 
# some tests somewhere also:)
#

from mingus.core.intervals import from_shorthand
import sys

#
# Takes either command line or stdin as input
#
#   $0 [note1 shortcut [note2 shortcut [...] [noteN shortcut]]]
#
# *** Note - it won't be happy if you don't have an even number of arguments!  Note/shortcut pairs, keep it in mind ***
#
#   So:
#
#      C M3     should print the major third of a C
#      D# A4    should print the tritone of D#
#
# You can also use integers instead of the name, which correspond to the number of half steps.
# A negative sign in front of an interval means go down that many steps, not up - so this is legal:
#
#   A -M3
#   B -6
#
#
# https://musictheory.pugetsound.edu/mt21c/HowToIdentifyIntervals.html
#  Half Steps     Interval Name     (shortcut)
#   1               Minor Second    (m2)
#   2               Major Second    (M2)
#   3               Minor Third     (m3)
#   4               Major Third     (M3)
#   5               Perfect Fourth  (P4)
#   6               Tritone or Augmented Fourth/Diminished Fifth (A4/d5)
#   7               Perfect Fifth   (P5)
#   8               Minor Sixth     (m6)
#   9               Major Sixth     (M6)
#   10              Minor Seventh   (m7)
#   11              Major Seventh   (M7)
# hmm... going to keep this out for now... maybe later: 12 Perfect Octave (P8)
#
# google "Search Labs | AI Overview" claims -
#
# shortcuts and... also allowing just flat numbers if you don't know the above
valid_intervals = {
        "m2": 1,
        "M2": 2,
        "m3": 3,
        "M3": 4,
        "P4": 5,
        "A4": 6,
        "d5": 6,
        "tri": 6,
        "P5": 7,
        "m6": 8,
        "M6": 9,
        "m7": 10,
        "M7": 11,
        # "P8": 12,
        "1":  1,
        "2":  2,
        "3":  3,
        "4":  4,
        "5":  5,
        "6":  6,
        "7":  7,
        "8":  8,
        "9":  9,
        "10": 10,
        "11": 11
        # "12": 12
}

# lookup table from short-long form
shortcut_to_interval = {
        "m2": "Minor Second",
        "M2": "Major Second",
        "m3": "Minor Third",
        "M3": "Major Third",
        "P4": "Perfect Fourth",
        "A4": "Tritone ",
        "d5": "Augmented Fourth",
        "tri": "Diminished Fifth",
        "P5": "Perfect Fifth",
        "m6": "Minor Sixth",
        "M6": "Major Sixth",
        "m7": "Minor Seventh",
        "M7": "Major Seventh"
}

#
# mingus doesn't like just numbers tho, so a simpole lookuap
# going from numbers to the shortcut
#
# making "6" to be A4 (apparently could be d5/tritone as well)
#
n_to_shortcut = {
        "1": "m2",
        "2": "M2",
        "3": "m3",
        "4": "M3",
        "5": "P4",
        "6": "A4",
        "7": "P5",
        "8": "m6",
        "9": "M6",
        "10": "m7",
        "11": "M7"
        # "12": "P8"
}

#
# sort of a weird tool, so pump out some help
#
usage   = f"\n{sys.argv[0]} [reads-from-stdin-or] [note1-shortcut [note2-shortcut [...] [noteN-shortcut]]]\n" + \
"""\nValid shortcuts are either the amount of half steps or the shortcut below (in parenthesis)

    Half Steps   Interval Name                                  Shortcut
         1       Minor Second                                      m2
         2       Major Second                                      M2
         3       Minor Third                                       m3
         4       Major Third                                       M3
         5       Perfect Fourth                                    P4
         6       Tritone/Augmented Fourth/Diminished Fifth     tri/A4/d5
         7       Perfect Fifth                                     P5
         8       Minor Sixth                                       m6
         9       Major Sixth                                       M6
         10      Minor Seventh                                     m7
         11      Major Seventh                                     M7
"""

# VERBOSE = True
VERBOSE = False

if "--help" in str(sys.argv) or "-h" in str(sys.argv):
    print(usage)
    sys.exit(0)

#
# read a file or stdin
#
try:
    # notes = sys.argv[1:]
    objects = sys.argv[1:]
except Exception as e:
    print(e)
    print(usage)
    sys.exit(1)

if not objects:
    try:
        if VERBOSE:
            sys.stderr.write("reading from stdin...\n")
        objects = sys.stdin.read().strip().split()
    except Exception as e:
        print(e)
        print(usage)
        sys.exit(1)

# print("OB: ")
# print(objects)
olen = len(objects)

# for token in objects:

# twofer per loopy
for n in range(0, olen, 2):

    # print("T1")
    # print(token)

    note     = objects[n].upper()
    shortcut = objects[n+1]

    # if the number starts with a minus sign, remove it and set the flag for going down rather than up
    DOWN = False
    if shortcut[0] == "-":
        shortcut = shortcut[1:]
        DOWN  = True

    # convert #'s to actual shotcutds
    if shortcut[0].isdigit():
        try:
            shortcut = n_to_shortcut[shortcut]
        except:
            print(f"something suss about {shortcut}, skipping....")
            continue

    # print(f"TOK: {token}")
    # print(f"Note/Short: {note} / {shortcut}")

    try:
        if shortcut not in valid_intervals:
            sys.stderr.write(f"Don't recognize \"{shortcut}\" as a shortcut, skipping\n")
            continue
    except Exception as e:
        print(e)
        sys.stderr.write("bailin' on this one, not sure what's going on....")
        continue

    # go down
    if DOWN:

        interval = from_shorthand(note, shortcut, False)

        # if VERBOSE:
        sys.stderr.write(f"going down - the {shortcut_to_interval[shortcut]} below {note} is ")
        sys.stderr.flush()

    else:

        interval = from_shorthand(note, shortcut)

        # if VERBOSE:
        sys.stderr.write(f"The {shortcut_to_interval[shortcut]} of {note} is ")
        sys.stderr.flush()

    print(f"{interval}")


