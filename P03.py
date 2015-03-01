import sys
import re
import time
import datetime
from datetime import date
from __builtin__ import str

class GedI: 
	def __init__(self, pointer):
		self.pointer = pointer
		self.firstname = None
		self.lastname = None
		self.sex = None
		self.birt= None
		self.deat = None
		self.famc = None
		self.fams = None
		
	def getAge(self):
		if self.birt is not None:
			birtDate = datetime.datetime.strptime(self.birt, "%d %b %Y").date()
			curDate = date.today()
			return curDate.year - birtDate.year - ((curDate.month, curDate.day) < (birtDate.month, birtDate.day))
			
class GedF:
	def __init__(self, pointer):
		self.pointer = pointer
		self.marr = None
		self.husb = None
		self.wife = None
		self.chil = []
		self.div = None



class GedList:

	def __init__(self, filename):
		self.tagchecks = {"INDI":0, "NAME":1, "SEX":1, "BIRT":1, "DEAT":1, "FAMC":1, "FAMS":1, "FAM":0, "MARR":1, "HUSB":1, "WIFE":1, "CHIL":1, "DIV":1, "DATE":2, "TRLR":0, "NOTE":0}
		self.list={}
		numFamily = 0

		f = open(filename,'r')

		lines = f.readlines()

		i = 0;

		while i < len(lines):
			
			line = lines[i]

			spl = line.split()

			if spl[1] == "TRLR":
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
					tempged = GedI(spl[1])
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
							#print nextl
							if spl2[1] == "NAME":
								tempged.firstname = spl2[2]
								tempged.lastname = spl2[3].translate(None, "/")
							elif spl2[1] == "BIRT" or spl2[1] == "DEAT":
								dateline = lines[i+2].split()
								if spl2[1] == "BIRT":
									dateline[2] = "0" + dateline[2] if int(dateline[2]) < 10 else dateline[2]
									tempged.birt = dateline[2] + " " + dateline[3] + " " + dateline[4]
								else:
									dateline[2] = "0" + dateline[2] if int(dateline[2]) < 10 else dateline[2]
									tempged.deat = dateline[2] + " " + dateline[3] + " " + dateline[4]
								i += 1  #Skip an extra line since we read 2
							elif spl2[1] == "SEX":
								tempged.sex = spl2[2]
							elif spl2[1] == "FAMC":
								tempged.famc = spl2[2]
							elif spl2[1] == "FAMS":
								tempged.fams = spl2[2]
						i += 1
					self.list[tempged.pointer] = tempged
					# print "Added " + tempged.pointer + " to list"
					
				elif spl[2] == "FAM":
					tempged = GedF(spl[1])
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
							if spl2[1] == "HUSB":
								tempged.husb = spl2[2]
							elif spl2[1] == "WIFE":
								tempged.wife = spl2[2]
							elif spl2[1] == "CHIL":
								tempged.chil.append(spl2[2])
							elif spl2[1] == "MARR" or spl2[1] == "DIV":
								dateline = lines[i+2].split()
								if spl2[1] == "MARR":
									dateline[2] = "0" + dateline[2] if int(dateline[2]) < 10 else dateline[2]
									tempged.marr = dateline[2] + " " + dateline[3] + " " + dateline[4]
								else:
									dateline[2] = "0" + dateline[2] if int(dateline[2]) < 10 else dateline[2]
									tempged.div = dateline[2] + " " + dateline[3] + " " + dateline[4]
							
						i += 1
					# print "Added " + tempged.pointer + " to list"
					self.list[tempged.pointer] = tempged



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

	# def __str__(self):

	# 	ret = ""

	# 	return ret

	def getKey(self, item):
		if 'F' in item:
			return int("999999"+item.translate(None, "@F"))
		else:
			return int("0"+item.translate(None,"@I"))

		
	def printList(self):
		sorted_x = sorted(self.list.keys(), None, key=self.getKey)				
		for sorted_key in sorted_x:		
			for key, value in self.list.iteritems():
 						if re.search("@I.+", key) and key == sorted_key:
 							print key + " " + value.firstname + " " + value.lastname
					 	elif re.search("@F.+", key) and key == sorted_key:
					 		husb = self.list[value.husb]
					 		wife = self.list[value.wife]
					 		print key + " Husband: " + husb.firstname + " " + husb.lastname + " Wife: " + wife.firstname + " " + wife.lastname
							
	def parentMarriage(self):
		# note: in python 3, iter() is the exact same as iteritems(). https://stackoverflow.com/questions/10458437/what-is-the-difference-between-dict-items-and-dict-iteritems
		for id, item in self.list.iteritems():
			if re.search("@I.+", id):
				testFail = False
				if item.fams is not None and item.famc is not None:
					spouseId = self.list[item.fams].wife if self.list[item.fams].husb == id else self.list[item.fams].husb
					parentId1 = self.list[item.famc].wife
					parentId2 = self.list[item.famc].husb
					
					if parentId1 == spouseId:
						testFail = True
						print item.firstname + " " + item.lastname + " is married to their parent " + self.list[parentId1].firstname + " " + self.list[parentId1].lastname + " -- Failed"
					elif parentId2 == spouseId:
						testFail = True
						print item.firstname + " " + item.lastname + " is married to their parent " + self.list[parentId2].firstname + " " + self.list[parentId2].lastname + " -- Failed"
						
				if testFail == False:
					print item.firstname + " "  + item.lastname + " not married to parent -- Passed"
			
	def minorMarriage(self):
		for id, item in self.list.iteritems():
			if re.search("@I.+", id):
				testFail = False
				if item.fams is not None:
					spouseId = self.list[item.fams].wife if self.list[item.fams].husb == id else self.list[item.fams].husb
					
					if self.list[spouseId].getAge() < 18:
						testFail = True
						print item.firstname + " " + item.lastname + " is married to a minor " + self.list[spouseId].firstname + " " + self.list[spouseId].lastname + " -- Failed"
						
				if testFail == False:
					print item.firstname + " " + item.lastname + " not married to minor -- Passed"
						
	def birthDeathCheck(self):
		for id, item in self.list.iteritems():
			if "@I" in id:
				testFail = False
				if item.deat is None:
					continue
				birthDate = datetime.datetime.strptime(item.birt, "%d %b %Y").date()
				deathDate = datetime.datetime.strptime(item.deat, "%d %b %Y").date()
				if birthDate>deathDate:
					testFail = True
					print item.firstname + " " + item.lastname + " has died before they are born -- Failed"
						
				if testFail == False:
					print item.firstname + " " + item.lastname + "'s birth and death dates look normal -- Passed"
					
 	def childParentBirthDeathCheck(self):
 		childDod = None
 		for id, item in self.list.iteritems():
		    if "@F" in id:
		    	fatherDob = datetime.datetime.strptime(self.list.get(item.husb).birt, "%d %b %Y").date() 
		    	motherDob = datetime.datetime.strptime(self.list.get(item.wife).birt, "%d %b %Y").date()
		    	for child in item.chil:
		    		
		    		if self.list.get(child).birt:
		    		    childDob  = datetime.datetime.strptime(self.list.get(child).birt, "%d %b %Y").date()
		    		    if childDob < fatherDob or childDob < motherDob:
		    		        print "Error: " + self.list.get(child).firstname + " " + self.list.get(child).lastname + "'s birth is before their parent's birth."

		    		if self.list.get(child).deat:
		    		    childDod  = datetime.datetime.strptime(self.list.get(child).deat, "%d %b %Y").date()
		    		    if childDod < fatherDob or childDod < motherDob:	
		    			    print "Error: " + self.list.get(child).firstname + " " + self.list.get(child).lastname + "'s death is before their parent's birth."

				        			
	def timeLine(self):
		timelinelist = {}
		for id, item in self.list.iteritems():
			if "@I" in id:
				if item.birt is not None:
					birthday = datetime.datetime.strptime(item.birt, "%d %b %Y").date()
					timelinelist[birthday] = item.firstname + " " + item.lastname + " was born on " + str(birthday)
				if item.deat is not None:
					deathday = datetime.datetime.strptime(item.deat, "%d %b %Y").date()
					timelinelist[deathday] = item.firstname + " " + item.lastname + " died on " + str(deathday)
			elif "@F" in id:
				if item.marr is not None:
					marrday = datetime.datetime.strptime(item.marr, "%d %b %Y").date()
					husband = self.list.get(item.husb)
					wife = self.list.get(item.wife)
					timelinelist[marrday] = husband.firstname + " " + husband.lastname + " and " + wife.firstname + " " + wife.lastname + " were married on " +str(marrday)
				if item.div is not None:
					divday =datetime.datetime.strptime(item.div, "%d %b %Y").date()
					timelinelist[divday] = husband.firstname + " " + husband.lastname + " and " + wife.firstname + " " + wife.lastname + " got divorced on " + str(divday)

		sorted_x = [value for (key, value) in sorted(timelinelist.items())]

		for event in sorted_x:
			print event


		

#and now for the main

g = GedList("gedcoms/us24.ged")
#g.printList()
g.childParentBirthDeathCheck()
g.parentMarriage()
g.minorMarriage()
g.birthDeathCheck()
g.timeLine()