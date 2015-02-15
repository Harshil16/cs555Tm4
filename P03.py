import sys

class GedI: 
	def __init__(self):
		self.name = None
		self.sex = None
		self.birt= None
		self.deat = None
		self.famc = None
		self.fams = None
class GedF:
	def __init__(self):
		self.marr = None
		self.husb = None
		self.wife = None
		self.chil = None



class GedList:

	def __init__(self, filename):
		self.tagchecks = {"INDI":0, "NAME":1, "SEX":1, "BIRT":1, "DEAT":1, "FAMC":1, "FAMS":1, "FAM":0, "MARR":1, "HUSB":1, "WIFE":1, "CHIL":1, "DIV":1, "DATE":2, "TRLR":0, "NOTE":0}
		self.list={}

		f = open(filename,'r')

		lines = f.readlines()

		i = 0;

		while i < len(lines):
			
			line = lines[i]

			spl = line.split()

			if line == "0 TRLR":
				break

			#don't even bother if it's not a valid tag
			elif not self.checkTag(spl):
				i+=1
				continue

			#outer loop only cares about level 0
			elif spl[0] != '0':
				i+=1
				continue

			#it's good
			else:
				if spl[2] == "INDI":
					tempged = GedI()
					while True:
						#get the next line until the end of the new entity
						try:
							nextl = lines[i+1]
						except IndexError:
							i+=1

						spl2 = nextl.split()
						#do all the normal error checking stuff
						if not self.checkTag(spl2):
							i+=1
							continue

						elif spl2[0] == '0':
							break
						#here's where the magic happens
						else:
							if spl2[]
						i +=1
				elif spl[2] == "FAM":
					tempged = GedF()
					while True:
						#get the next line until the end of the new entity
						try:
							nextl = lines[i+1]
						except IndexError:
							i+=1

						spl2 = nextl.split()
						#do all the normal error checking stuff
						if not self.checkTag(spl2):
							i+=1
							continue

						elif spl2[0] == '0':
							break
						#here's where the magic happens
						else:

						i +=1



	def checkTag(self, spl):

		lnum = int(spl[0])

		if lnum ==0:
			if len(spl) ==2:
				tag = spl[1]
			else:
				tag = spl[2]

		else:
			tag = spl[1]
		
		if tag not in self.tagchecks:
			return False

		else:
			if self.tagchecks[tag] == lnum:
				return True

			else:
				return False

	def __str__(self):

		ret = ""

		return ret

#and now for the main

g = GedList("sample.ged")

