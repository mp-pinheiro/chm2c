import mido
import json
import sys

from pnote import Note
from ptrack import Track

SONG_NAME = 'Test'
TEMPO_MOD_CONSTANT = 8.0/5.0

def createIniFile(mid):
	file = open('songTest/song.ini', 'w')
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
charter=Unknown Charter
delay=0
song_length=%d
""" % (SONG_NAME, mid.length))
	file.close()

def getTempo(mid):
	track = mid.tracks[0]
	for msg in track:
		if 'set_tempo' in msg.type:
			return mido.tempo2bpm(msg.tempo)

def getTimeSignature(mid):
	track = mid.tracks[0]
	for msg in track:
		if 'time_signature' in msg.type:
			return msg.numerator, msg.denominator

def createChartFile(mid):
	file = open('songTest/notes.chart', 'w')
	tempo = getTempo(mid)
	header = """[Song]
{
    Resolution = 192
    Offset = 0
}
[SyncTrack]
{
    0 = B %s000
}
[ExpertSingle]
{
""" % (tempo)
	file.write(header)
	track = createTrackByMid(mid)
	file.write(track.generateChart())
	file.write('}')
	file.close()

def createTrackByMid(mid):
	currentTime = 0
	noteStarts = {}
	midTrack = mid.tracks[1]
	track = Track(mid.ticks_per_beat, getTempo(mid), getTimeSignature(mid))

	for msg in midTrack:
		if 'note' in msg.type or 'pitchwheel' in msg.type:
			# print msg
			currentTime += msg.time
			if 'note_on' == msg.type:
				noteStarts[msg.note] = currentTime 
			elif 'note_off' == msg.type:
				track.addNote(noteStarts[msg.note], currentTime - noteStarts[msg.note], msg.note)

	return track

mid = mido.MidiFile('midis/input.mid')
createIniFile(mid)
createChartFile(mid)