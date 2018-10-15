from pnote import Note
import mido

class Track:
	RESOLUTION = 192.0

	def __init__(self, ticksPerBeat, tempo, signature):
		self.ticksPerBeat = ticksPerBeat
		self.tempo = tempo
		self.notes = []
		self.signature = signature

	def definePitches(self, notes):
		# TODO COISA ERRADA NESSE CODIGO 

		counter = {}
		pitches = []
		for note in notes:
			if note.pitch not in counter:
				counter[note.pitch] = True
				pitches.append(note.pitch)
		pitches.sort()

		pitchMap = {}
		noteCount = len(counter)
		lastGroupSize = noteCount % 5
		lastFullGroup = noteCount - lastGroupSize
		for i, pitch in enumerate(pitches):
			newPitch = 0
			posInGroup = i % 5
			if i<lastFullGroup:
				# Is in a full group
				newPitch = posInGroup
			else:
				# Sort into new group
				if lastGroupSize == 1:
					newPitch = 2
				elif lastGroupSize == 2:
					newPitch = 2*posInGroup + 1
				elif lastGroupSize == 3:
					newPitch = 2*posInGroup
				elif lastGroupSize == 4:
					if lastGroupSize < 2:
						newPitch = lastGroupSize
					else:
						newPitch = lastGroupSize + 1
			pitchMap[pitch] = newPitch

		for note in notes:
			note.pitch = pitchMap[note.pitch]

	def generateChart(self):
		chart = ''

		numerator, denominator = self.signature
		tempo = mido.bpm2tempo(self.tempo)
		sectionEnd = numerator ** 2 * self.ticksPerBeat
		sectionNotes = []
		lastSection = 1

		def closeSection(sectionNotes):
			# Close section
			self.definePitches(sectionNotes)
			sectionNotes = []

		for note in self.notes:
			if note.position >= sectionEnd*lastSection:
				lastSection += 1
				closeSection(sectionNotes)
			
			# Add note to section
			sectionNotes.append(note)
		closeSection(sectionNotes)

		for note in self.notes:
			mod = Track.RESOLUTION / self.ticksPerBeat
			newPos = int(round(note.position * mod))
			newPitch = note.pitch
			newDur = int(round(note.duration * mod))
			if newDur <= Track.RESOLUTION//2:
				newDur = 0
			chart += "\t{} = N {} {}\n".format(newPos, newPitch, newDur)

		return chart

	def addNote(self, position, pitch, duration):
		self.notes.append(Note(position, pitch, duration))