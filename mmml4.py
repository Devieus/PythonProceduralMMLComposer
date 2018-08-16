#determine tempo
#determine default note length
#determine octave (probably 4 for melody, 2-3 for bass, whatever for drums)
import random as r
octaveSign=''
title="Blank"
# Take a tempo between 12 and 15.
tempo=r.randint(12,15)
# Determine the song length depending on the tempo
# It should be about 50 at 12
songLength=int(4.5*tempo) #in bars
song= {"voice1":[],"voice2":[],"voice3":[],"voice4":[]}
whipeFlag=r.randint(0,1) # either start with only drums, or only without drums, for 16 or so lengths
#v1 is drums/noise
drums=["o4g","o6g","r","o4g","o6g"]
#the rest is just notes
#notes=["a","a+","b","c","c+","d","d+","e","f","f+","g","g+"]
#notes=["c","d","e","f","g","a","b"]
notes=["c","d","f","g","a"]

# --------------------------------------------------------Drums--------------------------------------------------------

for x in range(songLength):
    # With L8, it stands to reason there should be 8 total hits.
    # Time to implement the three part system again.
    result="o2g"+drums[2]+"v45"
    # go for the 2-4-2
    credit=8
    while credit>0:
        # Guess a next note's length
        nextLength=r.choice([4,8,16])
        # If it doesn't fit, guess another
        while credit-16/nextLength<0:
            # 4 (quarter) isn't going to fit at this point
            nextLength=r.choice([8,16])
        result+=r.choice(drums)+str(nextLength)
        credit-=16/nextLength
    result += "v50o2g" + drums[2]
    song["voice1"].append(result) # Add the result to the dict.
    

# --------------------------------------------------------Lead--------------------------------------------------------

# Time to separate the algorithm for precision strikes.
def algorithm(note):
    # If the previous note isn't a rest
    if note != "r":
        # Maybe make it a rest?
        if r.randint(1, 7) == 1:
            return "r"
        else:
            # Or don't, at which point do the magic algorithm.
            return int(r.gauss(0,2.5))+notes.index(note)
    else:
        # The last note was a rest, so just grab a random note.
        return r.randint(0,4)#int((r.gauss(0,1.5))+notes.index(song["voice2"][-2][-1]))

leadOctave=4
note=r.choice(notes)
result=''
for x in range(songLength):
    for y in range(8):
        # Add the result from the loop.
        result+=(octaveSign+note)
        # Empty the sign, otherwise it might just go crazy.
        octaveSign=''
        dnote=algorithm(note) #returns either a rest or an index
        if dnote != "r":
            if dnote>5 and leadOctave<6: # Going up an octave.
                while dnote>5:
                    leadOctave+=1
                    octaveSign+=">"
                    dnote-=5
            elif dnote<0 and leadOctave>3: # Going down an octave.
                while dnote<0:
                    leadOctave-=1
                    octaveSign+="<"
                    dnote+=5
            else: # It's running out of the octave bounds.
                dnote=(dnote+5)%5
            note=notes[dnote] # dnote is sanitized now.
        else:
            note=dnote # what is, how you say, type mismatch?
    # Write down the result into the dictionary.
    song["voice2"].append(result)
    # Empty the result for recycling.
    result=""

"""
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
    """
# --------------------------------------------------------Bass--------------------------------------------------------

for y in range(songLength):
    # Initialize the procedure.
    credit=8
    result=''
    # Start each bar (as it were) with a random note.
    note=r.choice(notes)
    # Make it either half or half dotted.
    if r.choice([True,False]):
        note+='.'
        credit-=4
    # Add this note for a start
    result+=note
    while credit>0:
        # Guess a next note's length
        nextLength=r.choice([4,8,16])
        # If it doesn't fit, guess another
        while credit-16/nextLength<0:
            # 4 (quarter) isn't going to fit at this point
            nextLength=r.choice([8,16])
        # Add the next note. The next note is up to two notes away, but not itself.
        flag=True
        while flag:
            try:
                result+=notes[notes.index(result[0])+r.choice([-1,-2,1,2])]+str(nextLength)
                credit-=16/nextLength
                flag=False
            except IndexError:
                # This is pretty crude, all said. It'll eventually reach a note it can use but it's terrible coding.
                # Either that or it's genius because there's no need to check the input for every conceivable problem.
                pass
    # Add the result to the song.
    song["voice4"].append(result)


# ---------------------------------------------------------Output----------------------------------------------
output=";[ "+title+" ];\n\n"
output+="CH1Verse_1.s = \"t"+str(tempo)+" \\12 w5 v50 l8 " # Set up basic variables for the track.
for x in range(songLength):
    output+=song["voice1"][x] # And then add it to the output

output+="\"\n\nCH2Verse_1.s = \"t"+str(tempo)+" \\6 w3 v50 o4 l8 " # Set up basic variables for the track.
for x in range(songLength):
    output+=song["voice2"][x] # This should be fine as long as x remains an index.
'''
output+="\"\n\nCH3Verse_1.s = \"t"+str(tempo)+" \\6 w3 v40 o4 l8 " # Set up basic variables for the track.
for x in range(songLength):
    output+=song["voice3"][x]
'''
output+="\n\nCH4Verse_1.s = \"t"+str(tempo)+" \\2 w1 v50 o2 l2 " # Set up basic variables for the track.
for x in range(songLength):
   # Add the track to the song.
    output+=song["voice4"][x]
    if x==songLength/2:
       output+='>'

output+="c1\""
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