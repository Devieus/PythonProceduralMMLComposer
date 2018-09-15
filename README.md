# PythonProceduralMMLComposer
The 2018 WeeklyBeats branch, 1/3 the size and 4 tracks only using Macrotune for parsing output.
# Python
Version 3.x, whatever's latest will work. 2.x might work too, it's not doing anything too fancy, just writes to a file.
The file is called "Blank.txt" and will appear in the same directory as whatever version of the program you're running.
# Macrotune
Read all about it here: https://posemotion.itch.io/macrotune

You'll need it if you want to use the output (unless you can read MML and want to play with an instrument). Other interpreters won't work as well.
# The tracks
- Track 1 is always the drum track, that's where it'll stay because track 1 is the only track in Macrotune with a noise waveform.
- Track 2 is the lead.
- Track 3 is the harmony.
- Track 4 is the bass.

You can swap those three around if you like, or even change their roles if you want. For example, by changing the 'o' variable in the track you can change the octave, so if you set track 4 to "o5" and track 2-3 to "o2" you'll have a melodic bass and a vocal track.
