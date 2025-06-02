#!/bin/bash

# sanitiez
if [ -z "$1" ]; then
    echo "usage: $0 chord-to-image"
    exit 1
fi

# requirements
if ! command -v lilypond >/dev/null 2>&1; then
    echo "requires 'lilypond' to run"
    exit 2
fi
if ! command -v magick >/dev/null 2>&1; then
    echo "requires 'magick' (from imagemagick) to run"
    exit 3
fi

# set -e

notez="$*"

tmp=$(mktemp)

trap "rm -rf $tmp" INT ERR EXIT

cat > $tmp <<_EOF_
\version "2.24.4"
\include "predefined-guitar-fretboards.ly"
\new FretBoards {
  \override FretBoards.FretBoard.size = 4.0
  \chordmode {
    $notez
  }
}
_EOF_

# arcane magix
lilypond -dbackend=eps -dno-pdf -dcrop --png -o "$notez" "$tmp" &> /dev/null

rez="$notez".png

rm -f "$rez"
mv "$notez".cropped.png "$rez"

# image magix
magick "$rez" -bordercolor white -border 20 "$rez"

echo -e "rendered image is in:\n\n    $rez\n"
