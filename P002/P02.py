import sys

tags = {"INDI":0, "NAME":1, "SEX":1, "BIRT":1, "DEAT":1, "FAMC":1, "FAMS":1, "FAM":0, "MARR":1, "HUSB":1, "WIFE":1, "CHIL":1, "DIV":1, "DATE":2, "TRLR":0, "NOTE":0}

def checkTag(st, level):
	
	if st not in tags:
		return "Invalid tag"

	else:
		if tags[st] == level:
			return st

		else:
			return "Invalid tag"

f = open('sample.ged','r');
for line in f:

	#write the whole line
	sys.stdout.write(line)

	l=line.split()
	
	lnum = int(l[0])
	
	#write the level number
	print lnum

	#print the tag, if it's valid
	if lnum ==0:
		if len(l) ==2:
			print checkTag(l[1], lnum)
		else:
			print checkTag(l[2], lnum)

	else:
		print checkTag(l[1], lnum)
	print