import sys


def checkTag(st):
	tags = ["INDI", "NAME", "SEX", "BIRT", "DEAT", "FAMC", "FAMS", "FAM", "MARR", "HUSB", "WIFE", "CHIL", "DIV", "DATE", "TRLR", "NOTE"]
	for t in tags:
		if st == t:
			return st

	return "Invalid tag"

f = open('My-Family-1-Feb-2015.ged','r');
for line in f:

	#write the whole line
	sys.stdout.write(line)

	l=line.split()
	
	#write the level number
	print l[0]

	#print the tag, if it's valid
	if l[0] =='0':
		if len(l) ==2:
			print checkTag(l[1])
		else:
			print checkTag(l[2])

	else:
		print checkTag(l[1])
	print