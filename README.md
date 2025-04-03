And so it begins....

This is a set of programs that work with music notes/chords/etc in various ways.

An effort is made to make the various programs -

- do one thing
- read from stdin or arguments on the command line
- pipe-able to each other (e.g. foo | bar | baz)

## Install/requirements

It's fairly reliant on the mingus music package. You can install via -
```
    pip3 install -r requirements.txt
```
Or simply -
```
    pip3 install mingus==0.6.1
```

## programs

### n2c

c2n - AKA chords-to-notes. Takes a set of chords (from stdin or arguments) and attempts to convert them to notes.
n2c - AKA notes-to-chords. Takes a set of notes (from stdin or arguments) and attempts to convert them to chords.

Errors and some surpurfluous data are sent to /dev/stderr, the rest goes to stdout.

```bash
$ echo  B D# F# | n2c
BM
$ n2c C Eb G
...it might be one of...
Cm
EbM6
```

### c2n

c2n - AKA chords-to-notes. Takes a set of chords (from stdin or arguments) and attempts to convert them to notes.

Errors and some surpurfluous data are sent to /dev/stderr, the rest goes to stdout.
```bash
$ echo  B D# F# | n2c
BM
```
Since it can read from stdin, you can also do something like -
```bash
# note - the "BM" in the output was sent to stderr... this is for legibility but also permits easier piping
$ echo  B D# F# | n2c | c2n
BM         B D# F#
```
Or, conversely -
```bash
$ echo  C | c2n | n2c
C          CM
```

