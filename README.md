# chm2c
Turns midi tracks into Clone Hero charts.

# Read Me
Alright, this thing is a buggy mess, but it works. Kind of. Feel free to fork this and do wathever, my Python sucks, but I hope it can be useful. Couple of disclaimers: 

+ The algorithm that places notes is very crude still, equal sections will play differently on different times, pitched notes like glissandos will count as one note only, and so on. It needs work, but it's playable and I've had a ton of fun with it.
+ I did not make a stand alone program of this, but I did enclude a working python environment so anyone can run by starting "run.bat". If you want to setup your own env, though, just clone the repo and install the dependecies on the 'how to python' section.
+ This only works on 64bit because I'm lazy. If you're on 32bit, change the bit in 'main.py' with 'x64' to 'x32' when KMC is called.
+ The GUI is awful, but the program is worse, it may crash, restart and bug out of nowhere. 
+ Some midis don't work well, they get out of tempo. It's weird and will take some investigation to find out why.
+ As of now, the program can only do 1 midi track. This is *most times* enough to make a fun Clone Hero chart, but some songs split their sections in multiple tracks, those won't, as you play a small section and the rest of the song will be just silent. I do want to make a "merge" option, so you can select multiple tracks and sections that you want to play. I kind of started this, but I'm way too lazy to finish it.
+ To convert the song to "ogg", the format that Clone Hero plays, chm2c uses [Keepy's KMC](https://github.com/KeppySoftware/KMC/releases). Since this was just slapped together, it would take way too much time and work to put KMC embed in source, so the program is just called from within chm2c after the chart is generated. Read the pop up.

# Instructions
+ Download the [latest release](https://github.com/mp-pinheiro/chm2c/releases) and extract it anywhere you want.
+ Run 'run.bat'.
+ Choose a midi file.
+ Choose the track you want to be converted into chart.
+ Read the pop-up if you haven't.
+ A folder with the same name as your midi file will be created with both chart and ini files for the song. That's the song folder.
+ Render the midi file as ogg with KMC by clicking "File -> Render to OGG" and put it on the generated folder.
+ Rename the ogg file rendered by KMC to 'song.ogg'.
+ Copy and paste the song folder to your Clone Hero songs folder.
+ Scan songs on Clone Hero and have fun.

# Errors
![Unknown](https://i.imgur.com/09uHlII.png)  
Something broke with the program, not much can be done, try another midi. If you know python, you can take out the "except" and check out the error. You can also create an issue here on Github, put the midi there and I'll take a look when I have some free time.

![Can't play song](https://i.imgur.com/IBeTxEW.png)  
Something is wrong with the 'song.ogg' file. Did you render the ogg file? Did you rename the rendered ogg to 'song.ogg'?

# How to python
+ Install miniconda: https://conda.io/miniconda.html
+ Create environment: ``conda create -n env_name python=2.7``
+ Install mido: ``env_path\python -m pip install mido``
