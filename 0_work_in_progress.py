#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# ------------------------------------------------------- Imports and settings -------------------------------------------------------
import music21
from music21 import *
import random

application_path = "/usr/bin/timidity"
music21.environment.set('midiPath', application_path)


# ------------------------------------------------------- RAW -------------------------------------------------------

#my_raw_string = 'tinyNotation: 4/4 c4 d=id2 e f C4 trip{c8 d e} trip{f4 g a} b-1 D4 C.4 D8~ D8 r c4 E4 F4 G4 E8 F G16 A B c A4 B4 c4'



balez ="4/4 c4 d=id2 e f C4 trip{c8 d e} trip{f4 g a} b-1 D4 C.4 D8~ D8 r c4 E4 chord{C4 e g} F.4 chord{D8 F# A} F4 G4 chord{C4 e g} chord{C4 e g} E8 F G16 A B c A4 chord{D8 F# A} B4 c4"

#------------------------------------------------------- POO

class ChordState(tinyNotation.State):
    def affectTokenAfterParse(self, n):
       super(ChordState, self).affectTokenAfterParse(n)
       return None # do not append Note object

    def end(self):
        ch = chord.Chord(self.affectedTokens)
        ch.duration = self.affectedTokens[0].duration
        return ch

# ------------------------------------------------------- making Object from RAW -------------------------------------------------------

#s = converter.parse(my_raw_string)

tnc = tinyNotation.Converter()
tnc.bracketStateMapping['chord'] = ChordState
tnc.load(balez)


# ------------------------------------------------------- Surgery -------------------------------------------------------
# ------------------------------------------------------- EXEC -------------------------------------------------------

newstream = tnc.parse().stream
newstream.write("midi", "mozart.mid")

# DOCS -------------

print(" PDF   http://www.flexatone.org/static/docs/music21Stream.pdf")

print("https://www.apprendrelesolfege.com/les-gammes")

#-------------------------------------------------------- GOALS



def give_game_from_tonic(note_tonic = 'C', kind = 'Major'):
	print(f"game degres from {note_tonic}   {kind}  ")


	print(f" I : La tonique {note_tonic}")
	print(f" II : La sus-tonique {sus_tonic}")
	print(f" III : La mediante {mediante}")
	print(f" IV : La sous-dominante {sub_dominant}")
	print(f" V : La dominante {dominant}")
	print(f" VI : La sus-dominante {sus_dominant}")
	print(f" VII : La sensible {sensible}")



	


	

def give_chord_from_tonic(note_tonic = 'C', kind = "Major"):

	if kind == "Major":
		pass
	else:
		pass

	print(f"Chord from {note_tonic}   {kind}  ")
	print(f"tierce  {tierce}")
	print(f"quinte   {quinte}")


def give_chord_name(*notelist):
	the_chord = chord.Chord(notelist)
	print(f" the_chord  {notelist}  is called  {the_chord.commonName}")



def pitch_class_numbers(*notelist):

	# c = chord.Chord([0, 2, 3, 5])
	# OR
	# c = chord.Chord([72, 76, 79])
	
	c = chord.Chord(notelist)
	print(f" pitch_from_numbers {notelist} is {c.pitches}")



def fifth(*notelist):
	#c = chord.Chord(['E3', 'C4', 'G5'])
	c = chord.Chord(notelist)
	fifth = c.fifth

	print(f"fifth from {notelist} is {fifth}")


def midi_from_pitch(pitch):
	midi = pitch.midi

	print(f"midi from {pitch} is {midi}")


def inspect_pitch(pitch):

	the_pitch = pitch.Pitch(pitch)
	the_pitch_name = the_pitch.name
	the_pitch_step = the_pitch.step
	the_pitch_accidental = the_pitch.accidental
	the_pitch_octave = the_pitch.octave

	the_pitch_nameWithOctave = the_pitch.nameWithOctave

	nameWithOctave

	print(f" the_pitch is {pitch} = {the_pitch_name} {the_pitch_step} {the_pitch_accidental} {the_pitch_octave}  {the_pitch_nameWithOctave}")




def make_pitch_from_midi(midi: int):
	# lowE = pitch.Pitch(midi=3)

	new_pitch = pitch.Pitch(midi)

	new_pitch_name = new_pitch.name
	new_pitch_octave = new_pitch.octave




def give_pitch_full_name(the_pitch):
	# p3 = pitch.Pitch(name='C', accidental='#', octave=7, microtone=-30)
	pitch_full_name = the_pitch.fullName

	print(f" p3.fullName {pitch_full_name}")


def pitch_french(the_pitch):

	# print(pitch.Pitch('B-').french)

	pitch_french = the_pitch.french

	print(f" pitch_french {pitch_french}")




print("Warning A Pitch without an accidental has a .accidental of None, not Natural.") 
print("This can lead to problems if you assume that every Pitch or Note has a .accidental that you can call .alter or something like that")


def give_pitch_class(the_pitch):
	"""
	Returns or sets the integer value for the pitch, 0-11, where C=0, C#=1, D=2…B=11. Can be set using integers (0-11) or ‘A’ or ‘B’ for 10 or 11.

	a = pitch.Pitch('a3')

	>>> a.pitchClass ==== 9

	"""

	print(f" pitch_class {the_pitch.pitchClass}")



--------------------

CEG = chord.Chord(['C','E','G']).pitchedCommonName
CEGB = chord.Chord(['C','E','G','B']).pitchedCommonName




print("['C','E','G']    =>  ", CEG)

print("['C','E','G','B']    =>  ", CEGB)


my_scale = "C4 G D A E B F# Dm Am Em Bm F C5"
my_full_scale = 'tinyNotation: 4/4 ' + my_scale
#s = converter.parse('tinyNotation: 4/4 c4 d=id2 e f C4 trip{c8 d e} trip{f4 g a} b-1 D4 C.4 D8~ D8 r c4 E4 F4 G4 E8 F G16 A B c A4 B4 c4')

#s = converter.parse('tinyNotation: 4/4 ' + my_scale)

tnc = tinyNotation.Converter()
tnc.load(my_full_scale)
newstream = tnc.parse().stream

newstream.show('midi')

sus = harmony.ChordSymbol('Dsus4')

x=[str(p) for p in sus.pitches]
print(x)

print("\n ..")

c = chord.Chord(['B-3', 'D-4', 'F4'])
harmony.chordSymbolFigureFromChord(c, True)
print(c)
print(harmony.chordSymbolFigureFromChord(c, True))
y=print(harmony.chordSymbolFigureFromChord(c, True))
print(y)
print(type(y))
print("\n ..")

c = chord.Chord(['C3', 'D3', 'E3'])
harmony.chordSymbolFigureFromChord(c, True)
print(c)
z=print(harmony.chordSymbolFigureFromChord(c, True))


print(z)
print(type(z))

"""

https://web.mit.edu/music21/doc/moduleReference/moduleHarmony.html

https://github.com/cuthbertLab/music21/blob/master/music21/harmony.py

THIRDS
    >>> c = chord.Chord(['C3', 'E3', 'G3'])
    >>> harmony.chordSymbolFigureFromChord(c, True)
    ('C', 'major')

"""

"""

d3 = inChord.semitonesFromChordStep(3)  # 4  triad
    d5 = inChord.semitonesFromChordStep(5)  # 7  triad
    d7 = inChord.semitonesFromChordStep(7)  # 11 seventh
    d9 = inChord.semitonesFromChordStep(2)  # 2  ninth
    d11 = inChord.semitonesFromChordStep(4)  # 5  eleventh
    d13 = inChord.semitonesFromChordStep(6)  # 9  thirteenth

"""

print("Line 1414:     https://github.com/cuthbertLab/music21/blob/master/music21/harmony.py")


"""
========>>>>>>>>>>>>>>>
Vidéo 15 - Progressions d'accords (harmonisation)
Muller
https://www.youtube.com/watch?v=KsWZysU9b1w
"""



__________________
"""
def isEnharmonic(other_piche):
	p1 = pitch.Pitch('C#3')

p2 = pitch.Pitch('D-3')

p3 = pitch.Pitch('D#3')

p1.isEnharmonic(p2)
True

p2.isEnharmonic(p1)
True

p3.isEnharmonic(p1)
False
"""

#c2b = chord.Chord(['c', 'f-', 'g'])
#c2b.commonName


"""

n = s.recurse().getElementById('id2')
ch = chord.Chord('D4 F#4 A4')
ch.style.color = 'pink'
n.activeSite.replace(n, ch)
"""
#s.show('midi')








#tnc.load("2/4 C4 chord{C4 e g} F.4 chord{D8 F# A}")




"""
tnc.write("midi", "mozart.mid")     # AttributeError: 'Converter' object has no attribute 'write'
"""


"""
exportStream = stream.Stream()
#exportStream.append(tnc) # $$$$$$$   music21.exceptions21.StreamException: The object you tried to add to the Stream, <music21.tinyNotation.Converter object at 0x7fa1d1198d90>, is not a Music21Object.  Use an ElementWrapper object if this is what you intend

#exportStream.insert(0, tnc) # *******   music21.exceptions21.StreamException: to put a non Music21Object in a stream, create a music21.ElementWrapper for the item


wrap = music21.ElementWrapper(tnc)

time_offset = 0
exportStream.insert(time_offset, wrap)
exportStream.write("midi", "mozart.mid")

exportStream.show('midi')
"""
"""

p1 = stream.Part()
p1.append([XXX1, XXX2])

s1 = stream.Score()
s1.append(p1)

"""


"""

exportStream = stream.Stream()
exportStream.append(h1)



print("writing stream")
exportStream.write("midi", "test005.mid")
"""







# https://github.com/syncopika/mmp-to-MusicXML

"""
https://medium.com/@william.borgomano/entra%C3%AEner-une-intelligence-artificielle-%C3%A0-composer-comme-beethoven-9212f5c78f70
"""
"""

https://stackoverflow.com/questions/34382213/how-to-save-output-in-music21-as-a-midi-file


If s is your Stream, just call:

fp = s.write('midi', fp='pathToWhereYouWantToWriteIt')

or to hear it immediately

s.show('midi')



/////////////////////////

https://stackoverflow.com/questions/34382213/how-to-save-output-in-music21-as-a-midi-file




mt = MidiTrack(1)

# duration, pitch, velocity
data = [[1024, 60, 90], [1024, 50, 70], [1024, 51, 120],[1024, 62, 80], ]

# Omit this part here, but full code in the links above
populateTrackFromData(mt, data)

mf = MidiFile()
mf.ticksPerQuarterNote = 1024 # cannot use: 10080
mf.tracks.append(mt)

mf.open('/src/music21/music21/midi/out.mid', 'wb')
mf.write()
mf.close()

"""

"""

ah, your original question was how to change the instrument in a midi file, but these files have no instruments defined, so they're falling back on piano as the default instrument. 
 The code I sent and you've given substitutes new instruments for old instruments; it doesn't add any instruments if they're not defined.  You could do:


s=converter.parse("sound.mid")
for p in s.parts:
     p.insert(0, instrument.Violin())
s.show('midi')

or if you want to do a different instrument for each part, something like:

s.parts[0].insert(0, instrument.Clarinet())
s.parts[1].insert(0, instrument.Trombone())
"""




"""



If you want to add additional pitches into existing notes, use the stream.Stream.insertIntoNoteOrChord method:

http://web.mit.edu/music21/doc/moduleReference/moduleStream.html#music21.stream.Stream.insertIntoNoteOrChord

For instance:

s = stream.Stream()
n = note.Note('C4') # qtr note default
s.append(n)

c = chord.Chord('E4 G4') # qtr
s.insertIntoNoteOrChord(0.0, c)
s.show('t')
{0.0} <music21.chord.Chord C4 E4 G4>

If you need to do something more complex, then I suggest just inserting all of the notes and chords to wherever you want them to be, and then running .chordify() on the Stream to make everything work.

A third option is to use different stream.Voice() objects for the different layers.


"""



"""

 Pitch.ps

    The ps property permits getting and setting a pitch space value, a floating point number representing pitch space, where 60.0 is C4, middle C, 61.0 is C#4 or D-4, and floating point values are microtonal tunings (0.01 is equal to one cent), so a quarter-tone sharp above C5 is 72.5.

    Note that the choice of 60.0 for C4 makes it identical to the integer value of 60 for .midi, but .midi does not allow for microtones and is limited to 0-127 while .ps allows for notes before midi 0 or above midi 127.
    >>>

a = pitch.Pitch('C4')

a.ps
60.0

Changing the ps value for a will change the step and octave:
>>>

a.ps = 45

a
<music21.pitch.Pitch A2>

a.ps
45.0

"""