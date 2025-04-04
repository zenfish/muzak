#!/usr/bin/env python

#
# find the maximum chord length sequences in a song
#
#   Takes a file with chords in it, space sep'd
#

import os
import sys

from collections import defaultdict

MIN_TIMES  = 2
MIN_LENGTH = 6

REPLACEMENT = "~"

# suck in the chords from a file
try:
    chord_file = sys.argv[1]
    with open(chord_file) as filey:
        chords = filey.read()
        chords = chords.split()
        # chords = ''.join(chords)
except:
    print "Usage: %s chord-file" % sys.argv[0]
    sys.exit(1)

print "working with %d chords (%d unique):\n%s\n" % (len(chords), len(set(chords)), ' '.join(chords))

all_chords    = {}
all_index     = {}

#
# might have to rethink this... but that's pretty high up in the ord sequence....
# ... too many chords could blow up
#
# current_index = '!'
current_index = '0'

# since chords can be multiple characters...I'm going to fold them into
# a single character mapping space, do chord distributions on the
# mapped space, and then un-map them at the end. This way I can use
# simple string manipulators vs. multi char madness

def mappy(chord):

    global all_chords
    global all_index
    global current_index

    old_index = current_index

    try:
        # all_chords[chord]
        return all_chords[chord]

    # map & reverse map
    except:
        all_chords[chord]        = current_index
        all_index[current_index] = chord

        # current_index            = chr(ord(current_index) + 1)
        current_index            = str(int(current_index) + 1)

        return old_index

#
# given a mapped chord, return the original chord
#
def unmappy(chord):
    
    global all_index
    global all_chords

    # return all_index[all_chords[chord]]
    return all_index[chord]


# adapted from https://stackoverflow.com/questions/11090289/find-longest-repetitive-sequence-in-a-string

def getsubs(loc, s):
    substr = s[loc:]
    i = -1
    while(substr):
        yield substr
        substr = s[loc:i]
        i -= 1

def longest(r):

    occ     = defaultdict(int)

    # tally all occurrences of all substrings
    for i in range(len(r)):
        for sub in getsubs(i,''.join(r)):
            occ[sub] += 1

    # filter out all substrings with fewer than minocc occurrences
    matches = [k for k,v in occ.items() if v >= MIN_TIMES and len(k) <= len(r)/2]

    # import pdb
    # pdb.set_trace()
    # print(matches)

    if matches:

        #
        # ... ok... the above finds a list of all the matches and their
        # frequency... want to return the top one. But it also finds
        # overlapping strings... so this tries to ensure the substrings
        # are >= MIN_TIMES in frequency.
        #
        while True:
            maxkey =  max(matches, key=len)

            # matches above can overlap... count only non-overlappers
            occ[maxkey] = ''.join(r).count(maxkey)

            if occ[maxkey] < MIN_TIMES:
                # print("nuking for < min")
                matches.remove(maxkey)
            else:
                break 

            # print("trying again...")



        return len(maxkey), occ[maxkey], maxkey

        # return len(maxkey), 1, maxkey
    else:
        return 0,0,""

#
# initialize mappings
#

#
# generate single character mappings for chords
#
new_chords = []

for chord in chords:
    new_chords.append(mappy(chord))
    # c = mappy(chord)
    # print("%s\t%s" % (chord, c))
    # new_chords.append(c)

#
# loop over chords until you can't loop no more
#

print "N-in-seq\tN-times\t\tGroup of Chords"

# runs of chords will get tossed in here
chord_clumps = []

# keep going 'till ya can't go no more... e.g. run out of chords to chomp on
while True:

    # n, m = longest(chords)
    l, n, m = longest(new_chords)

    if not m:
        break

    if l < MIN_LENGTH:
        break

    rehydrated = ""
    # print("")
    # print(m)
    for c in m:
        # print(c)
        # print(unmappy(c))
        # try:
        rehydrated = rehydrated + unmappy(c) + ' '
        # except:
        #     import pdb
        #     pdb.set_trace()

    print "%d\t%d\t%s" % (l, n, rehydrated)

    # append each chord clumps
    for z in range(n):
        chord_clumps.append(rehydrated.strip())

    # convert to string, remove matches
    # s = ''.join(chords)
    s = ''.join(new_chords)

    for i in range(1, n + 1):
        s = s.replace(m,"_")

    # chords = list(s)
    new_chords = list(s)

print("\n")

# print("NEW")
# print(new_chords)
# print("")

# nc_n = len(new_chords)
# print(nc_n)

rehydrated = ""

nc_n2 = 0

for c in new_chords:
    if c != "_":
        rehydrated = rehydrated + unmappy(c) + ' '
        nc_n2 = nc_n2 + 1

# print("Left Over Chords:\n\n\t%d\t%s\n" % (nc_n2, rehydrated))


chords_in_order = ' '.join(chords)

final_chords       = ""
chord_n            = 0
remaining_chords   = chords_in_order
final_chords       = chords_in_order
final_chord_clumps = ""

for clump in chord_clumps:

    # print('hunting for...')
    # print(clump)
    # print('in....')
    # print(remaining_chords)

    location = remaining_chords.find(clump)

    # this shouldn't happen :)
    if location < 0:
        # import pdb
        # pdb.set_trace()
        print("wait a second... something is wrong here...")
        sys.exit(666)

    # keep track of what chord we're on
    chord_n = chord_n + location

    # carve out the matching chords
    remaining_chords = remaining_chords.replace(clump, REPLACEMENT * len(clump), 1)

    # insert newlines around match
    final_chords     = final_chords[:location] + final_chords[location:].replace(clump, "\n" + clump + "\n", 1)


#
# that's all, folks!
#

print("FINAL RUN:\n")

final_string = (os.linesep.join([s.strip() for s in final_chords.splitlines() if s]))

print(final_string)

print("\n... also writtten to %s" % chord_file + ".max")

with open(chord_file + ".max", "wt") as f:
    f.write(final_string + "\n")

