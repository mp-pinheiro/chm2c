from __future__ import print_function

from pnote import Note
import mido

class Track:
	RESOLUTION = 192.0

	def __init__(self, ticksPerBeat, signature, name):
		self.ticksPerBeat = ticksPerBeat
		#self.tempo = tempo
		self.notes = []
		self.signature = signature
		self.name = name

	def countPitches(self, notes):
		counter = {}
		pitches = []
		for note in notes:
			if note.pitch not in counter:
				counter[note.pitch] = True
				pitches.append(note.pitch)
		pitches.sort()

		return pitches

	def definePitches(self, notes):
		pitches = self.countPitches(notes)

		pitchMap = {}
		noteCount = len(pitches)
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
					if posInGroup < 2:
						newPitch = posInGroup
					else:
						newPitch = posInGroup + 1
			pitchMap[pitch] = newPitch

		##print(pitchMap)

		for note in notes:
			note.pitch = pitchMap[note.pitch]
			#print(self.getStringCloneHeroStyle(note.pitch))

	def getStringCloneHeroStyle(self, pitch):
		return ' ' * pitch + '*'

	def getRangeInSection(self, section):
		range = 0
		for noteL in section:
			for noteR in section:
				if noteL != noteR:
					r = abs(noteL.pitch - noteR.pitch)
					if r > range:
						range = r

		return r

	def checkSectionEnded(self, sectionNotes, noteIndex, lastPosition):
		if len(sectionNotes)==0:
			return False

		sectionSize = len(self.countPitches(sectionNotes))
		newSectionNotes = list(sectionNotes)

		i = noteIndex
		while i < len(self.notes) and self.notes[i].position < lastPosition:
			newSectionNotes.append(self.notes[i])
			i += 1

		newSectionSize = len(self.countPitches(newSectionNotes))
		#print(sectionSize, newSectionSize)
		return (newSectionSize-1)//5 > (sectionSize-1)//5

	def generateChart(self, sectionSizeMod):
		chart = ''

		if self.signature:
			numerator, denominator = self.signature
		else:
			numerator, denominator = 4, 4
		#tempo = mido.bpm2tempo(self.tempo)
		compassSize = numerator * self.ticksPerBeat
		sectionSize = compassSize * sectionSizeMod
		sectionNotes = []
		lastCompass = 1

		noteIndex = 0
		for note in self.notes:
			lastPosition = compassSize * lastCompass
			if note.position >= lastPosition:
				lastCompass += 1
				if self.checkSectionEnded(sectionNotes, noteIndex, lastPosition+compassSize):
					#print("next section", lastCompass-1)
					self.definePitches(sectionNotes)
					sectionNotes = []
			noteIndex += 1

			# Add note to section
			sectionNotes.append(note)
		self.definePitches(sectionNotes)
		sectionNotes = []

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

	def __len__(self):
		return len(self.notes)