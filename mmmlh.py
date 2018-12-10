"""
14th iteration:
But what about the chorus?

"""
import random as r
octaveSign=''
title="Blank"
# Take a tempo between 10 and 12.
tempo=r.randint(12,14)
# Determine the song length depending on the tempo
# It should be about 50 at 12
songLength=int(2*tempo) #in bars, and as a multiple of 4.
song= {"voice1":[],"voice2":[],"voice3":[],"voice4":[],"leadOctaves":[],"bassOctaves":[],"progressCycle":[]}
song2= {"voice1":[],"voice2":[],"voice3":[],"voice4":[],"leadOctaves":[],"bassOctaves":[],"progressCycle":[]}
whipeFlag=r.randint(0,1) # either start with only drums, or only without drums, for 16 or so lengths
#v1 is drums/noise
drums=["o4g","o6g","r","o4g","o6g"]
#the rest is just notes
#notes=["a","a+","b","c","c+","d","d+","e","f","f+","g","g+"]
notes=["c","d","e","f","g","a","b"]
#notes=["c","d","f","g","a"]
# Define chords independent from scale.
chords=[[0,2,4],[1,3,5],[2,4,6],[0,3,5],[1,4,6],[0,2,5],[1,3,6]]
# --------------------------------------------------------Drums--------------------------------------------------------

def drumGen():
    # With L8, it stands to reason there should be 16 total hits for two bars.
    # Time to implement the three part system again.
    result="o2gr"
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
    result+="o2gr "
    song["voice1"].append(result) # Add the result to the dict.
    return result

def drumGen2():
    # With L8, it stands to reason there should be 16 total hits for two bars.
    # Time to implement the three part system again.
    result="o2gr"
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
    result+="o2gr "
    song2["voice1"].append(result) # Add the result to the dict.
    return result
    

# --------------------------------------------------------Lead--------------------------------------------------------

# This is a 2D table containing the odds for a markov chain (values need to be cumulative).
markovChain=[[30,60,90,100], # Half note
             [30,55,90,100], # Quarter note
             [30,70,90,100], # Eighth note
             [30,60,70,100]] # Sixteenth note
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
            if dnote>5 and leadOctave<5: # Going up an octave.
                while dnote>=7:
                    leadOctave+=1
                    octaveSign+=">"
                    dnote-=7
            elif dnote<0 and leadOctave>3: # Going down an octave.
                while dnote<0:
                    leadOctave-=1
                    octaveSign+="<"
                    dnote+=7
            else: # It's running out of the octave bounds.
                dnote=(dnote+7)%7
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
# ------------------ song 2
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
            if dnote>5 and leadOctave<5: # Going up an octave.
                while dnote>=7:
                    leadOctave+=1
                    octaveSign+=">"
                    dnote-=7
            elif dnote<0 and leadOctave>3: # Going down an octave.
                while dnote<0:
                    leadOctave-=1
                    octaveSign+="<"
                    dnote+=7
            else: # It's running out of the octave bounds.
                dnote=(dnote+7)%7
            note=notes[dnote] # dnote is sanitized now.
        else:
            note=dnote # what is, how you say, type mismatch?
        # Now for the note length, which can be done by looping again.
    song2["leadOctaves"].append(octave)
    # Write down the result into the dictionary.
    song2["voice2"].append(result+' ')
    # Empty the result for recycling.
    result=""
    octave=""


# --------------------------------------------------------Rhythm------------------------------------------------------
def progress():
    # Generate a progression cycle.
    result=[0]
    for x in range(3):
        # Keep it simple, 4 chords, call this routine again to make another.
        result.append(r.randint(0,len(notes)-1))
    return result

def arpeggiate(inList):
    # Fill the song list with all the notes in a cycle over all 4 bars in 4 lists.
    # inputList looks like [0,x,y,z]
    for x in inList:
        # This number x is the index for
        chord=chords[x]
        # which consists of three numbers, which themselves are the index for
        a=[notes[chord[0]],notes[chord[1]],notes[chord[2]]]
        # which can then be used to make a bar. For now, just a simple arpeggio of 16ths.
        b=''
        for y in range(4):
            # Yea we're doing it this way now
            b+=a[0]+a[1]+a[2]+a[1]+' '
        # Great, bar is made, put it in the song directly.
        song["voice3"].append(b)
    return

bassOctave=4
for x in range(songLength):
    progressCycle=progress()
    # Place 4 bars.
    for y in range(tempo):
        # The song length is tempo*4, so tempo is song length/4
        arpeggiate(progressCycle)
    # place the current cycle in the dictionary.
    song["progressCycle"].append(progressCycle[x%4])
    if x%tempo==0 and x>0:
        # Change the progress cycle 4 times.
        progressCycle=progress()
    #song["voice3"].append(result) # Add the result to the dict.
    song["bassOctaves"].append(octave)
    octaveSign=''

def arpeggiate2(inList):
    # Fill the song list with all the notes in a cycle over all 4 bars in 4 lists.
    # inputList looks like [0,x,y,z]
    for x in inList:
        # This number x is the index for
        chord=chords[x]
        # which consists of three numbers, which themselves are the index for
        a=[notes[chord[0]],notes[chord[1]],notes[chord[2]]]
        # which can then be used to make a bar. For now, just a simple arpeggio of 16ths.
        b=''
        for y in range(4):
            # Yea we're doing it this way now
            b+=a[0]+a[1]+a[2]+a[1]+' '
        # Great, bar is made, put it in the song directly.
        song2["voice3"].append(b)
    return

bassOctave=4
for x in range(songLength):
    progressCycle=progress()
    # Place 4 bars.
    for y in range(tempo):
        # The song length is tempo*4, so tempo is song length/4
        arpeggiate2(progressCycle)
    # place the current cycle in the dictionary.
    song2["progressCycle"].append(progressCycle[x%4])
    if x%tempo==0 and x>0:
        # Change the progress cycle 4 times.
        progressCycle=progress()
    #song["voice3"].append(result) # Add the result to the dict.
    song2["bassOctaves"].append(octave)
    octaveSign=''

# --------------------------------------------------------Bass--------------------------------------------------------

for y in range(songLength):
    # Initialize the procedure.
    credit=8
    result=''
    # Start each bar (as it were) with a random note taken from the rhythm track.
    note=notes[song["progressCycle"][y]]
    # Make it either half or half dotted.
    if r.choice([True,False]):
        note+='.'
        credit-=4
    # Add this note for a start
    result+=note
    while credit>0:
        # Guess a next note's length
        nextLength=r.choice([4,8])
        # If it doesn't fit, guess another
        while credit-16/nextLength<0:
            # 4 (quarter) isn't going to fit at this point
            nextLength=8
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


for y in range(songLength):
    # Initialize the procedure.
    credit=8
    result=''
    # Start each bar (as it were) with a random note taken from the rhythm track.
    note=notes[song2["progressCycle"][y]]
    # Make it either half or half dotted.
    if r.choice([True,False]):
        note+='.'
        credit-=4
    # Add this note for a start
    result+=note
    while credit>0:
        # Guess a next note's length
        nextLength=r.choice([4,8])
        # If it doesn't fit, guess another
        while credit-16/nextLength<0:
            # 4 (quarter) isn't going to fit at this point
            nextLength=8
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
    song2["voice4"].append(result+' ')

# ---------------------------------------------------------Output----------------------------------------------

output=";[ "+title+" ];\n\n"
output+="CH1Verse_1.s = \"t"+str(tempo)+" \\12 w5 v50 l8 \"t"+str(tempo)+" \\12 w5 v50 l8 " # Set up basic variables for the drum track.
riff=[drumGen(),drumGen()] # Make a drum riff that's two bars long.
for x in range(songLength):
    output+=riff[x%2] # And then add it to the output
    if x%tempo==0 and x>0: # Generate a new riff after every so many bars.
        riff=[drumGen(),drumGen()]
        for y in range(3):
            output+=song["voice1"][0]

output+="\"\nCH1Verse_2.s = \"t"+str(tempo-1)+" \\12 w5 v40 l8 " # Set up basic variables for the second drum track.
riff=[drumGen2(),drumGen2()] # Make a drum riff that's two bars long.
for x in range(songLength):
    output+=riff[x%2] # And then add it to the output
    if x%tempo==0 and x>0: # Generate a new riff after every so many bars.
        riff=[drumGen2(),drumGen2()]
        for y in range(3):
            output+=song2["voice1"][0]

output+="\"\n\nCH2Verse_1.s = \"t"+str(tempo)+" w3 v50 o4 l16 \\6 \"t"+str(tempo)+" w3 v50 o4 l16 \\6 " # Set up basic variables for the lead track.
w=3
for x in range(songLength):
    output+=song["voice2"][x] # This should be fine as long as x remains an index.
    if x%tempo==0 and x>0: # Add the first three bars again after every so many bars.
        w=1 if (w+1)%5==0 else (w+1)%5 # Also change the instrument (again).
        output+="o4w"+str(w) # Set the octave to match the start of the song.
        for y in range(3):
            output+=song["voice2"][y]
        output+="o"+song["leadOctaves"][x][0] if x >= songLength / 2 else "o"+str(int(song["leadOctaves"][x][0])+1)# set the octave back.

output+="\"\nCH2Verse_2.s = \"t"+str(tempo-1)+" w3 v50 o4 l16 \\7,9,5 " # Set up basic variables for the second lead track.
w=3
for x in range(songLength):
    output+=song2["voice2"][x] # This should be fine as long as x remains an index.
    if x%tempo==0 and x>0: # Add the first three bars again after every so many bars.
        w=1 if (w+1)%5==0 else (w+1)%5 # Also change the instrument (again).
        output+="o4w"+str(w) # Set the octave to match the start of the song.
        for y in range(3):
            output+=song2["voice2"][y]
        output+="o"+song2["leadOctaves"][x][0] if x >= songLength / 2 else "o"+str(int(song2["leadOctaves"][x][0])+1)# set the octave back.

output+="\"\n\nCH3Verse_1.s = \"t"+str(tempo)+" w2 v42 o5 l16 \\9,0,8,5 \"t"+str(tempo)+" w2 v42 o5 l16 \\9,0,8,5 " # Set up basic variables for the rhythm track.
w=3
for x in range(songLength):
    output+=song["voice3"][x] # This should be fine as long as x remains an index.
    if x%tempo==0 and x>0: # Add the first three bars again after every so many bars.
        w=1 if (w+1)%5==0 else (w+1)%5 # Instruments go from 1 to 4.
        # Technically there's a 0, but that's reserved for the bass and it's the tri wave.
        output+="o4w"+str(w) # Set the octave to match the start of the song.
        for y in range(3):
            output+=song["voice3"][y]
        output+="o"+song["leadOctaves"][x][0] if x >= songLength / 2 else "o"+str(int(song["leadOctaves"][x][0])+1) # set the octave back.

output+="\"\nCH3Verse_2.s = \"t"+str(tempo-1)+" w2 v42 o5 l16 \\2 " # Set up basic variables for the second rhythm track.
w=3
for x in range(songLength):
    output+=song2["voice3"][x] # This should be fine as long as x remains an index.
    if x%tempo==0 and x>0: # Add the first three bars again after every so many bars.
        w=1 if (w+1)%5==0 else (w+1)%5 # Instruments go from 1 to 4.
        # Technically there's a 0, but that's reserved for the bass and it's the tri wave.
        output+="o4w"+str(w) # Set the octave to match the start of the song.
        for y in range(3):
            output+=song2["voice3"][y]
        output+="o"+song2["leadOctaves"][x][0] if x >= songLength / 2 else "o"+str(int(song["leadOctaves"][x][0])+1) # set the octave back.

output+="\"\n\nCH4Verse_1.s = \"t"+str(tempo)+" w0 v63 o3 l2 \\9,2 \"t"+str(tempo)+" w0 v63 o3 l2 \\9,2 " # Set up basic variables for the bass track.
for x in range(songLength):
   # Add the track to the song.
    output+=song["voice4"][x]
    # Add the first three bars again after every so many bars.
    if x %tempo == 0 and x>0:
        for y in range(3):
            output+=song["voice4"][y]
    if x==songLength/2:
       output+='>'

output+="\"\nCH4Verse_2.s = \"t"+str(tempo-1)+" w0 v63 o3 l2 \\6 " # Set up basic variables for the second bass track.
for x in range(songLength):
   # Add the track to the song.
    output+=song2["voice4"][x]
    # Add the first three bars again after every so many bars.
    if x %tempo == 0 and x>0:
        for y in range(3):
            output+=song2["voice4"][y]
    if x==songLength/2:
       output+='>'

output+="c1\"" # the final note.
# This next part is for multiple verses.
output+="\n\nChannel_1.s = CH1Verse_1 + CH1Verse_2 + CH1Verse_1" \
        "\nChannel_2.s = CH2Verse_1 + CH2Verse_2 + CH2Verse_1" \
        "\nChannel_3.s = CH3Verse_1 + CH3Verse_2 + CH3Verse_1" \
        "\nChannel_4.s = CH4Verse_1 + CH4Verse_2 + CH4Verse_1"
file=open(title+".txt","w")
file.write(output)
file.close()
'''print(song["leadOctaves"])
print(song["bassOctaves"])'''
"""
Macrotune MML sample
;[ The riddle ];

CH1Verse_1.s = "t12 w5 o1 \4 v40 l8r4"
CH1Verse_2.s = "o1gg>>g<<ggg>>gr"

CH2Verse_1.s = "t12 w4 o4 \4 v40 l8ef+g4gagf+edd4ef+f+4ef+g4a4gf+ede4edd4b>dc<bage4d4e2r4"

Channel_1.s = CH1Verse_1 + CH1Verse_2 + CH1Verse_2 + CH1Verse_2 + CH1Verse_2 + CH1Verse_2 + CH1Verse_2
Channel_2.s = CH2Verse_1
"""