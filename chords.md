
The many ways chords may be represented that `play_chords.py` understands.

So you might say -

    Cdim

    Cdom7dim5

    Cm6

    Cø11

Etcetera.

    # chord types                                      abbr         other abbr's
    major                       1,3,5                   ''          M, maj
    minor                       1,-3,5                  m           min
    augmented                   1,3
    diminished                  1,-3,-5                 dim         o
    
    # sevenths
    dominant-seventh            1,3,5,-7                7           dom7
    major-seventh               1,3,5,7                 maj7        M7
    minor-major-seventh         1,-3,5,7                mM7         m
    minor-seventh               1,-3,5,-7               m7          min7
    augmented-major-seventh     1,3
    augmented-seventh           1,3
    half-diminished-seventh     1,-3,-5,-7              ø7          m7b5
    diminished-seventh          1,-3,-5,--7             o7          dim7
    seventh-flat-five           1,3,-5,-7               dom7dim5        
    
    # sixths
    major-sixth                 1,3,5,6                 6
    minor-sixth                 1,-3,5,6                m6
    
    # ninths
    major-ninth                 1,3,5,7,9               M9          Maj9
    dominant-ninth              1,3,5,-7,9              9           dom9
    minor-major-ninth           1,-3,5,7,9              mM9         minmaj9
    minor-ninth                 1,-3,5,-7,9             m9          min9
    augmented-major-ninth       1,3
    augmented-dominant-ninth    1,3
    half-diminished-ninth       1,-3,-5,-7,9            ø9        
    half-diminished-minor-ninth 1,-3,-5,-7,-9           øb9        
    diminished-ninth            1,-3,-5,--7,9           o9          dim9
    diminished-minor-ninth      1,-3,-5,--7,-9          ob9         dimb9
    
    # elevenths
    dominant-11th               1,3,5,-7,9,11           11          dom11
    major-11th                  1,3,5,7,9,11            M11         Maj11
    minor-major-11th            1,-3,5,7,9,11           mM11        minmaj11
    minor-11th                  1,-3,5,-7,9,11          m11         min11
    augmented-major-11th        1,3
    augmented-11th              1,3
    half-diminished-11th        1,-3,-5,-7,9,11         ø11        
    diminished-11th             1,-3,-5,--7,9,11        o11         dim11
    
    # thirteenths
    major-13th                  1,3,5,7,9,11,13         M13         Maj13
    dominant-13th               1,3,5,-7,9,11,13        13          dom13
    minor-major-13th            1,-3,5,7,9,11,13        mM13        minmaj13
    minor-13th                  1,-3,5,-7,9,11,13       m13         min13
    augmented-major-13th        1,3
    augmented-dominant-13th     1,3
    half-diminished-13th        1,-3,-5,-7,9,11,13      ø13        
    
    # other
    suspended-second            1,2,5                   sus2        
    suspended-fourth            1,4,5                   sus         sus4
    suspended-fourth-seventh    1,4,5,-7                7sus        7sus4
    Neapolitan                  1,-2,3,-5               N6        
    Italian                     1
    French                      1,2
    German                      1,-3
    pedal                       1                       pedal        
    power                       1,5                     power        
    Tristan                     1


