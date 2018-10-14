class Note:
	def __init__(self, position, duration, pitch):
		self.position = position
		self.duration = duration
		self.pitch = pitch

	def __repr__(self):
		return self.__str__()

	def __str__(self):
		return "\nPosition: {}, Duration: {}, Pitch: {}".format(self.position, self.duration, self.pitch)

	def getConvertedPitch(self, pitch):
		octaves = (pitch // 12)
		firstOctave = pitch - (octaves * 12)
		return firstOctave % 5

	def convertToChart(self, tempo):
		return "\t{} = N {} {}\n".format(self.position, self.getConvertedPitch(self.pitch), self.duration)
		