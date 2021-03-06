#determine tempo
#determine default note length
#determine octave (probably 4 for melody, 2-3 for bass, whatever for drums)
import random as r
octaveSign=''
title="Blank"
tempo=r.randint(13,15)
songLength=400 #w/e
song= {"voice1":[],"voice2":[],"voice3":[],"voice4":[]}
whipeFlag=r.randint(0,1) # either start with only drums, or only without drums, for 16 or so lengths
#v1 is drums/noise
drums=["o2g","o4g","r"]
#the rest is just notes
#notes=["a","a+","b","c","c+","d","d+","e","f","f+","g","g+"]
notes=["c","d","e","f","g","a","b"]
# --------------------------------------------------------Drums--------------------------------------------------------

for x in range(songLength):
    song["voice1"].append(r.choice(drums)) # Add the result to the dict.
    

# --------------------------------------------------------Lead--------------------------------------------------------

leadOctave=3
note=r.choice(notes)
for x in range(songLength):
    song["voice2"].append(octaveSign+note) # Add the result to the dict. Maybe change length
    octaveSign=''
    dnote=int(r.gauss(0,2.5))+notes.index(note) if note!="r" else int(r.gauss(0,1.5))+notes.index(song["voice2"][-2][-1])
    dnote="r" if r.randint(1,7)==1 and song["voice2"][-1]!="r" else dnote
    if dnote != "r":
        if dnote>7 and leadOctave<6: # Going up an octave.
            leadOctave+=1
            octaveSign+=">"
            dnote-=7
        elif dnote<0 and leadOctave>2: # Going down an octave.
            leadOctave-=1
            octaveSign+="<"
            dnote+=7
        else: # It's running out of the octave bounds.
            dnote=(dnote+7)%7
        note=notes[dnote] # dnote is sanitized now.
    else:
        note=dnote # what is, how you say, type mismatch?
    

# --------------------------------------------------------Harmony------------------------------------------------------

bassOctave=4
for x in range(songLength):
   # Select note based on lead track note
    dnote=notes.index(song["voice2"][x][-1])-5 if song["voice2"][x][0]!="r" else "r" # Check the lead note at this place and lower it by 5
    if dnote!="r":
        if dnote>7 and bassOctave!=leadOctave+1: # Going up an octave.
            bassOctave+=1
            octaveSign+=">"
            dnote-=7
        elif dnote<0 and bassOctave!=leadOctave-1: # Going down an octave.
            bassOctave-=1
            octaveSign+="<"
            dnote+=7
        note=notes[dnote] # dnote is accurate now.
    else:
        note=dnote # I do not know this type mismatch thing you speak of.
    song["voice3"].append(octaveSign+note) # Add the result to the dict.
    octaveSign=''
    
# --------------------------------------------------------Bass--------------------------------------------------------

for x in range(int(songLength/8)):
   # Add the result to the dict.
    song["voice4"].append(r.choice(notes)+"1")

# ---------------------------------------------------------Output----------------------------------------------
output=";[ "+title+" ];\n\n"
output+="CH1Verse_1.s = \"t"+str(tempo)+" \\12 w5 v35 l8 " # Set up basic variables for the track.
for x in range(songLength):
    output+=song["voice1"][x] # And then add it to the output

output+="\"\n\nCH2Verse_1.s = \"t"+str(tempo)+" \\6 w3 v40 o3 l8 " # Set up basic variables for the track.
for x in range(songLength):
    output+=song["voice2"][x] # This should be fine as long as x remains an index.

output+="\"\n\nCH3Verse_1.s = \"t"+str(tempo)+" \\6 w3 v40 o4 l8 " # Set up basic variables for the track.
for x in range(songLength):
    output+=song["voice3"][x]

output+="\"\n\nCH4Verse_1.s = \"t"+str(tempo)+" \\1 w1 v45 o2 l8 " # Set up basic variables for the track.
for x in range(int(songLength/8)):
   # Add the result to the dict.
    output+=song["voice4"][x]

output+="\""
# This next part is for multiple verses.
#output+="\n\nChannel_1.s = CH1Verse_1\nChannel_2.s = CH2Verse_1\nChannel_3.s = CH3Verse_1\nChannel_4.s = CH4Verse_1"
file=open(title+".txt","w")
file.write(output)
file.close()
"""
Macrotune MML sample
;[ The riddle ];

CH1Verse_1.s = "t12 w5 o1 \4 v40 l8r4"
CH1Verse_2.s = "o1gg>>g<<ggg>>gr"

CH2Verse_1.s = "t12 w4 o4 \4 v40 l8ef+g4gagf+edd4ef+f+4ef+g4a4gf+ede4edd4b>dc<bage4d4e2r4"

Channel_1.s = CH1Verse_1 + CH1Verse_2 + CH1Verse_2 + CH1Verse_2 + CH1Verse_2 + CH1Verse_2 + CH1Verse_2
Channel_2.s = CH2Verse_1
"""