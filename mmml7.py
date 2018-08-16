"""
7th iteration:
Harmony
armony
rmony
mony

"""
import random as r
octaveSign=''
title="Blank"
# Take a tempo between 12 and 15.
tempo=r.randint(12,15)
# Determine the song length depending on the tempo
# It should be about 50 at 12
songLength=int(4.5*tempo) #in bars
song= {"voice1":[],"voice2":[],"voice3":[],"voice4":[],"leadOctaves":[],"bassOctaves":[]}
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
    song["voice1"].append(result+' ') # Add the result to the dict.
    

# --------------------------------------------------------Lead--------------------------------------------------------

# This is a 2D table containing the odds for a markov chain (values need to be cumulative).
markovChain=[[5,60,90,100], # Half note
             [10,50,90,100], # Quarter note
             [5,70,90,100], # Eighth note
             [5,40,90,100]] # Sixteenth note
# In order, these are half (2), quarter (4), eighths and sixteenths.
# If the aim is to reduce the odds of sixteenths, increase the third number.
import math
def markov(noteLength,i):
    noteLength=int(math.log(noteLength,2)-1) # Determine the selector through simple base 2 maths.
    while True:
        c=r.randint(0,100) # Roll that die!
        if c<markovChain[noteLength][0] and i<1: # Check those odds!
            return 2 # Output that note length!
        elif c<markovChain[noteLength][1] and i<2:
            return 4
        elif c<markovChain[noteLength][2] and i<3:
            return 8
        elif c<markovChain[noteLength][3]:
            return 16


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
octave=''
noteLength=r.choice([2,4,8,16])
for x in range(songLength):
    #for y in range(8): #
    y=16
    while y>0:
        i=0
        noteLength=markov(noteLength,i)
        #while y+int(16/noteLength)>8:
        while y-int(16/noteLength)<0:
            i+=1
            noteLength=markov(noteLength,i) # no half notes, they clearly don't fit.
        #y+=int(16/noteLength)
        y-=int(16/noteLength)
        # Add the result from the loop, which is admittedly a bit of an unusual place.
        result+=(octaveSign+note+str(noteLength)) if int(noteLength)!=16 else (octaveSign+note)
        octave+=str(leadOctave)
        # Empty the sign, otherwise it might just go crazy.
        octaveSign=''
        dnote=algorithm(note) #returns either a rest or an index
        if dnote != "r":
            if dnote>5 and leadOctave<6: # Going up an octave.
                while dnote>=5:
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
        # Now for the note length, which can be done by looping again.
    song["leadOctaves"].append(octave)
    # Write down the result into the dictionary.
    song["voice2"].append(result+' ')
    # Empty the result for recycling.
    result=""
    octave=""


# --------------------------------------------------------Harmony------------------------------------------------------

bassOctave=4
for x in range(songLength):
    octave=""
    result=""
    z=0 # Keep tabs of the octave index.
   # Select note based on lead track note
    for y in song["voice2"][x]: # Go through the string at large.
        # If it's a number, copy it to this track.
        # If it's an octave shift, ignore it.
        # If it's a letter, transpose it.
        try:
            int(y) # y is currently a number maybe.
            result+=y # So put it on the output.
        except(ValueError): # I guess it wasn't.
            if not (y=="<" or y==">" or y==' '): # Ignore octave shifts
                octaveSign=''
                dnote=notes.index(y)-3 if y!="r" else "r" # Check the lead note at this place and lower it by 5.
                if dnote!="r":
                    while dnote>5 and bassOctave!=int(song["leadOctaves"][x][z])+1: # Going up an octave.
                        bassOctave+=1
                        octaveSign+=">"
                        dnote-=5
                    while dnote<0 and bassOctave>int(song["leadOctaves"][x][z])-1: # Going down an octave.
                        bassOctave-=1
                        octaveSign+="<"
                        dnote+=5
                    while bassOctave<int(song["leadOctaves"][x][z])-1:
                        bassOctave += 1
                        octaveSign += ">"
                    note=notes[dnote] # dnote is accurate now.
                else:
                    note=dnote # I do not know this type mismatch thing you speak of.
                result+=octaveSign+note # Add note here.
                octave+=str(bassOctave)
                z+=1
    song["voice3"].append(result+" ") # Add the result to the dict.
    song["bassOctaves"].append(octave)
    octaveSign=''

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
    song["voice4"].append(result+' ')


# ---------------------------------------------------------Output----------------------------------------------
output=";[ "+title+" ];\n\n"
output+="CH1Verse_1.s = \"t"+str(tempo)+" \\12 w5 v40 l8 " # Set up basic variables for the drum track.
for x in range(songLength):
    output+=song["voice1"][x] # And then add it to the output
    # Add the first three bars again after every 50 bars.
    if x%10==0 and x>0:
        for y in range(3):
            output+=song["voice1"][y]


output+="\"\n\nCH2Verse_1.s = \"t"+str(tempo)+" \\6 w3 v50 o4 l16 " # Set up basic variables for the lead track.
w=3
for x in range(songLength):
    output+=song["voice2"][x] # This should be fine as long as x remains an index.

    if x%10==0 and x>0: # Add the first three bars again after every 20 bars.
        w=1 if (w+1)%5==0 else (w+1)%5 # Also change the instrument (again).
        output+="o4w"+str(w) # Set the octave to match the start of the song.
        for y in range(3):
            output+=song["voice2"][y]
        output+="o"+str(song["leadOctaves"][x][0]) # set the octave back.



output+="\"\n\nCH3Verse_1.s = \"t"+str(tempo)+" \\3 w2 v55 o4 l16 " # Set up basic variables for the harmony track.
w=3
for x in range(songLength):
    output+=song["voice3"][x] # This should be fine as long as x remains an index.

    if x%10==0 and x>0: # Add the first three bars again after every 20 bars.
        w=1 if (w+1)%5==0 else (w+1)%5 # Instruments go from 1 to 4.
        # Technically there's a 0, but that's reserved for the bass and it's the tri wave.
        output+="o4w"+str(w) # Set the octave to match the start of the song.
        for y in range(3):
            output+=song["voice3"][y]
        output+="o"+str(song["bassOctaves"][x][0]) # set the octave back.



output+="\n\nCH4Verse_1.s = \"t"+str(tempo)+" \\2 w1 v50 o2 l2 " # Set up basic variables for the bass track.
for x in range(songLength):
   # Add the track to the song.
    output+=song["voice4"][x]
    # Add the first three bars again after every 50 bars.
    if x %10 == 0 and x>0:
        for y in range(3):
            output += song["voice4"][y]
    if x==songLength/2:
       output+='>'


output+="c1\""
# This next part is for multiple verses.
#output+="\n\nChannel_1.s = CH1Verse_1\nChannel_2.s = CH2Verse_1\nChannel_3.s = CH3Verse_1\nChannel_4.s = CH4Verse_1"
file=open(title+".txt","w")
file.write(output)
file.close()
print(song["leadOctaves"])
print(song["bassOctaves"])
"""
Macrotune MML sample
;[ The riddle ];

CH1Verse_1.s = "t12 w5 o1 \4 v40 l8r4"
CH1Verse_2.s = "o1gg>>g<<ggg>>gr"

CH2Verse_1.s = "t12 w4 o4 \4 v40 l8ef+g4gagf+edd4ef+f+4ef+g4a4gf+ede4edd4b>dc<bage4d4e2r4"

Channel_1.s = CH1Verse_1 + CH1Verse_2 + CH1Verse_2 + CH1Verse_2 + CH1Verse_2 + CH1Verse_2 + CH1Verse_2
Channel_2.s = CH2Verse_1
"""