import mido
import json
import sys
import os
import subprocess

from Tkinter import *
import Tkconstants, tkFileDialog, tkMessageBox

from pnote import Note
from ptrack import Track

SONG_NAME = 'Test'
TEMPO_MOD_CONSTANT = 8.0/5.0

def createIniFile(mid):
	file = open(SONG_NAME + '/song.ini', 'w')
	file.write("""[song]
name=%s
diff_band=-1
diff_rhythm=-1
diff_drums=-1
diff_keys=-1
diff_guitarghl=-1
diff_bassghl=-1
preview_start_time=-1
video_start_time=0
charter=ch2m2c
delay=0
song_length=%d
""" % (SONG_NAME, mid.length))
	file.close()

def getTempos(mid):
	tempos = []
	for track in mid.tracks:
		for msg in track:
			if 'set_tempo' in msg.type:
				tempos.append(msg)
	return tempos

def getTimeSignature(mid):
	track = mid.tracks[0]
	for msg in track:
		if 'time_signature' in msg.type:
			return msg.numerator, msg.denominator

def getTempoString(tempos, ticksPerBeat):
	string = ''
	for msg in tempos:
		string += '\t{} = B {}000\n'.format(int(msg.time * Track.RESOLUTION // ticksPerBeat), mido.tempo2bpm(msg.tempo))
	return string

def createChartFile(mid, track):
	file = open(SONG_NAME + '/notes.chart', 'w')
	tempoString = getTempoString(getTempos(mid), mid.ticks_per_beat)
	header = """[Song]
{
    Resolution = 192
    Offset = 0
}
[SyncTrack]
{
%s
}
[ExpertSingle]
{
""" % (tempoString)
	file.write(header)
	#track = getHighestNoteTrack(getAllTracks(mid))
	#track = getAllTracks(mid)[1]
	file.write(track.generateChart())
	file.write('}')
	file.close()

def getAllTracks(mid):
	trackList = []
	for track in mid.tracks:
		print(track)
		#if 'drums' in track.name.lower() or 'percussion' in track.name.lower() or 'bass' in track.name.lower():
		#	continue
		trackList.append(createTrackByMid(mid, track))
	return trackList

MAX_FREE_COMPASS = 2
def mergeTracks(tracks):
	#mainTrack = getHighestNoteTrack(tracks)
	mainTrack = tracks[1]
	mergedTrack = mainTrack.copy()
	remainingTracks = tracks.remove(mainTrack)
	
def getHighestNoteTrack(tracks):
	biggest = tracks[0]
	for track in tracks:
		if len(biggest) < len(track):
			biggest = track
	return biggest

def createTrackByMid(mid, midTrack):
	currentTime = 0
	noteStarts = {}
	# midTrack = mid.tracks[3]
	#track = Track(mid.ticks_per_beat, getTempo(mid), getTimeSignature(mid))
	track = Track(mid.ticks_per_beat, getTimeSignature(mid), midTrack.name)

	for msg in midTrack:
		if 'note' in msg.type or 'pitchwheel' in msg.type:
			# print msg
			currentTime += msg.time
			if 'note_on' == msg.type:
				if msg.velocity == 0:
					track.addNote(noteStarts[msg.note], currentTime - noteStarts[msg.note], msg.note)
				else:
					noteStarts[msg.note] = currentTime 
			elif 'note_off' == msg.type:
				track.addNote(noteStarts[msg.note], currentTime - noteStarts[msg.note], msg.note)

	return track

def generateSong(mid, track, filename):
	if not os.path.exists(SONG_NAME):
		os.makedirs(SONG_NAME)
	
	createIniFile(mid)
	createChartFile(mid, track)
	
	tkMessageBox.showwarning("Attention!", "Your chart and ini files were created. A new window will pop for the conversion of the midi file into ogg, so that you can hear it on Clone Hero.\n\nClick 'File -> Render to ogg' and select the directory '" + SONG_NAME + "' as output.\n\nThe file must be named 'song.ogg', don't forget to rename it after it renders.\n\nYes this is very lazy of me, life is way too short.")
	subprocess.call('keepy/bin/x64/KeppyMIDIConverter.exe "' + filename.replace('/', '\\') + '"')
	
def restart():
	os.execl(sys.executable, sys.executable, * sys.argv)

window = Tk()
window.title('chm2c')
window.filename = tkFileDialog.askopenfilename(initialdir = "/", title = "Select a midi file", filetypes = (("midi files","*.mid"),),)

SONG_NAME = str(window.filename.split('/')[-1:][0].replace('.mid', '')) # I hate this but meh

w = Label(window, text="Select one of the midi tracks:")
w.pack()

mid = mido.MidiFile(window.filename)
try:
	tracks = getAllTracks(mid)
except Exception as e:
	tkMessageBox.showerror('Error', 'An unknown error occurred.') # Disable for debugging
	os._exit(1)

choice = IntVar()

for counter in range(1, len(tracks)):
	track = tracks[counter]
	Radiobutton(window, text=track.name + '(' + str(len(track)) + ' notes)', variable=choice, value=counter).pack(anchor=W)
	counter += 1 

b = Button(window, text="Generate", command=lambda: generateSong(mid, tracks[choice.get()], window.filename))
b.pack()

b = Button(window, text="Open a different midi", command=restart)
b.pack()

window.mainloop()

