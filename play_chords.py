#!/usr/bin/env python3

#
# play a set of notes/chords/etc from the command line - *** in the order given ***
#

#
# The following may be used multiple times... each time they're seen they change the bpm/ts/etc.
#
#   bpm=N     set BPM to whatever. Defaults to 120
#   ts=N      set Time Signature to whatever. Defaults to 4/4
#
# Notes start with an underscore; else are in the usual A-G, plus modifiers (#, etc.)
#
# Rests start with an X
#
# Chords use the usual A-G plus modifiers (#, etc.) This uses music21's harmony.ChordSymbol
# function to try and determine if it's a valid chord
#
# The duration of the music object defaults to a quarter note, but may be changed by adding a "."
# followed by a desired length... valid values are 'whole', 'half', 'quarter', 'eighth', '16th', 
# '32nd', '64th', '128th', '256th' '512th',, '1024th', '2048th', 'zero'
#
# The octave of the music object defaults to 4 (e.g. C-4), but may be changed by adding a "_"
# followed by a desired octave (1-N)
#
# Example -
#
#   $0   C  D  E                     play C-4, D-4, and E-4 chords @ 120 BPM
#
#   $0   ts=3/4  bpm=80  C D B       set to 3/4 time, 80bpm
#

import os
import re
import sys

usage = "%s chords-notes-or-directives [ bpm=N  ts=N  A-G/X[#b[0-9] etc ]  ...]" % sys.argv[0]

# silly pygame thing... has to come before music21, which uses pygame
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

from music21 import *


VERBOSE = False

def vprint(stringy):
    if VERBOSE:
        print(stringy)

# the flow of notes+
# scorey  = stream.Score(id='on-da-fly')
# part1   = stream.Part(id='part-one')
# streamy = stream.Measure(number=1)

streamy = stream.Stream()

fraction2duration = {
    "1":    "whole",
    "1/2":  "half",
    "1/4":  "quarter",
    "1/8":  "eighth",
    "1/16": "16th",
    "1/32": "32nd",
    "1/64": "64th",
    "1/128": "128th",
    "1/256": "256th",
    "1/512": "512th",
    "1/1024": "1024th",
    "1/2048": "2048th",
    "1/zero": "zero",
}

base_notes = ["A", "B", "C", "D", "E", "F", "G"]

#
# defaults if not specified
#
DEFAULT_DURATION  = "quarter"
DEFAULT_TIME_SIG  = "4/4"
DEFAULT_BPM       = 120

# any sound?
PLAY_MUSAK        = False
PLAY_MUSAK        = True

# remove the temporary-ish midi file
REMOVE_MIDI       = True

# use music-score to tell us the score
# PRINT_SCORE       = True
PRINT_SCORE       = False

# bpm = tempo.MetronomeMark(number=DEFAULT_BPM)
# bpm.setQuarterBPM(DEFAULT_BPM)
# streamy.append(bpm)



#
# does a string look like a note?
#
def is_note(notey):

    print("Note: %s" % notey)

    # Regular expression pattern for matching valid notes
    note_pattern = r'^([A-Ga-g])(#|b|##|bb)?(\d+)?$'
    
    # re.fullmatch() to ensure the entire string matches the pattern
    try:
        return bool(re.fullmatch(note_pattern, notey, re.IGNORECASE))

    except re.error:
        return False


#
# given a string, return a note/chord string along with duration
#
def get_duration(notey):

    duration = DEFAULT_DURATION

    if "." in notey:
        notey, duration = notey.split(".")

        # if used a shorthand
        if duration in fraction2duration:
            duration = fraction2duration[duration]

    return(notey, duration)

#
# given a note string and duration, return a note object
#
def str2note(notey, duration):
    notey               = note.Note(notey)
    notey.duration.type = duration
    return(notey)

#
# do the rest thang
#
def str2rest(resty, duration):
    # print(resty)
    # print(duration)
    try:
        resty               = note.Rest()
        resty.duration.type = duration
        return(resty)
    except:
        import pdb
        pdb.set_trace()
#
#
# given a chord string and duration, return a chord object
#
def chord2note(chordy, duration):

    # Create a ChordSymbol object from the chord symbol string
    try:
        symbol              = harmony.ChordSymbol(chordy)
    except:
        print("Don't understand the chord: %s" % chordy)
        sys.exit(33)
    
    # Extract the pitches from the ChordSymbol object
    pitches             = symbol.pitches
    
    # Create and return the Chord object using the extracted pitches
    chordy              = chord.Chord([p for p in pitches])

    chordy.duration.type = duration

    return(chordy)


#
#
# the fun begins
#
#

if len(sys.argv[1:]) < 1:
    print("Error: " + usage)
    sys.exit(1)

#
# suck in data from the command line
#
for arg in sys.argv[1:]:

#   print("Next token: %s - " % arg, end="")

    firstup  = arg[0].upper()

    duration = ""

    #
    # maybe a note?
    #
    if arg[0] == "_":

        notey           = arg[1:]

        notey, duration = get_duration(notey)

        if not is_note(notey):
            print("... not a note...")
        else:
            vprint("\tNote")
            notey = str2note(notey, duration)
            streamy.append(notey)

    #
    # a rest?
    #
    elif arg[0].lower() == "x":

        resty           = arg

        resty, duration = get_duration(resty)

        vprint("\tRest")
        resty = str2rest(resty, duration)
        streamy.append(resty)

    #
    # time signature?
    #
    elif arg[0:3] == "ts=":
        _, siggy = arg.split("=")
        ts = meter.TimeSignature(siggy)

        streamy.append(ts)

        print("Setting Time Signature to %s" % siggy)

    #
    # BPM
    #
    elif arg[0:4] == "bpm=":
        _, bpm = arg.split("=")

        speedy = tempo.MetronomeMark(number=int(bpm)) 
        speedy.setQuarterBPM(int(bpm))

        streamy.append(speedy)

        print("Setting BPM to %s" % bpm)

    #
    # Clef
    #
    elif arg[0:5] == "clef=":
        _, cleffy = arg.split("=")


        #
        # apparently music21 supports.... 
        #
        # AltoClef Bass8vaClef Bass8vbClef BassClef CBaritoneClef CClef FBaritoneClef FClef FrenchViolinClef 
        # GClef GSopranoClef JianpuClef MezzoSopranoClef NoClef PercussionClef PitchClef SopranoClef SubBassClef 
        # TabClef TenorClef Treble8vaClef Treble8vbClef TrebleClef
        #
        # rollin' the dice...
        #

        cleffy = cleffy[0].upper() + cleffy[1:] + "Clef"

        cleffun = getattr(clef, cleffy)()
        print("trying to add... %s" % cleffy)
        streamy.append(cleffun)

    #
    # maybe a chord?
    #
    # ... always starts with A-G
    elif firstup.startswith(tuple(base_notes)):

        # print("maybe a chord....?")

        chordy = arg

        # get the chord duration
        chordy, duration = get_duration(chordy)

        # actually change chordy => to a music21 chord
        chordy = chord2note(chordy, duration)

        if not chordy:
            print("... not a chord...")
        else:
            vprint("\tChord")
            # print(qq)

            try:
                streamy.append(chordy)
            except Exception as e:
                print(e)
                print("chordy, duration => %s / %s" % (chordy, duration))
                import pdb
                pdb.set_trace()


    else:
        print("woah, I'm lost!")
        sys.exit(99)


# divide the Stream into Measures
# streamy.makeMeasures()
streamy.makeMeasures(inPlace=True)


print("sketchy overview of what we've seen so far -\n")

print(streamy.show('text'))

print("")

# print("Beats for the various notes++:")
# for m in streamy:
#     for n in m:
#         print("\t" + str(n) + ": " + str(n.beat))
# 
# print("")

if PLAY_MUSAK:
    vprint('playing....')
    midi_file = streamy.write('mid')
    midi.realtime.StreamPlayer(streamy).play()

    vprint(midi_file)

    # remove midi file
    if REMOVE_MIDI:
        vprint("removing midi file... " + str(midi_file))
        os.remove(midi_file)
    else:
        vprint("Midi file kept: %" % str(midi_file))

# goes to external program
if PRINT_SCORE:
    print(streamy.show())

# streamy.write(fmt='lili.png')
# streamy.write('/Users/zen/src/me/music/tmp/lili.png')

print("finito")

