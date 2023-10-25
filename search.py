# search.py created ~ 18-20 August 2023
# (c) Craig Duncan
# Last updated 31 August 2023, 7 Sep 2023, 21 Sep 2023, 22 October 2023
# For use with allbates.csv

import string

def openData():
	f = open("allbates.csv", "r")
	page=f.read() # reads as string
	#pagestr= page.decode('utf-8') # this converts the binary file to string (converts bytes for EOL, LF etc to characters)
	f.close()
	Lines=page.split("\n");  # alternative to save, then readlines (which achieves the same outcome, but slower)
	return Lines

def main():
	data=openData()
	global introtext
	print("Lines opened:"+str(len(data)))
	print("Welcome!")
	print(introtext)
	# testrow(data[15000])
	interface(data) # mutemode True = print out results

def bulkSearch(mylist,mutemode):
	global searchlog,currentregion
	data=openData()
	mutemode=False
	for ui in mylist:
		counter=processinput(ui,data,mutemode)
		threshold=0 # results over ...
		if (counter[1]>threshold):
			outstring=counter[0]+","+str(counter[1])
			searchlog.append(outstring)
			print(outstring)
	writestr=""
	myname='searchresults'
	for t in searchlog:
		writestr=writestr+t+"\n"
	writecsv(myname,writestr)

def programmedSearch(input):
	global searchlog,currentregion
	data=openData()
	counter=processinput(input,data)
	return counter

def writecsv(name,input):
	fname=name+".csv"
	f = open(fname, "w")
	f.write(input) # writes a string
	f.close()

def testrow(input):
	print(input)
	cells=input.split("|")
	# print(cells[6])
	print(cells[7])
	print(cells[8])

def interface(data):
	global searchlog,currentregion,helptext,introtext
	userinput=""
	print("Enter the search term:")
	while (userinput!="exit"):
		userinput=input(">:")
		if (userinput!="exit" and userinput!="help" and userinput!="licence"):
			counter=processinput(userinput,data)
			outstring=userinput+","+str(counter)
			searchlog.append(outstring)
			# option to print a list of terms found, no additional details
			# termlist=counter[2]
			# for x in termlist:
			#	print(x)
		elif userinput=="help":
			print(helptext)
		elif userinput=="licence":
			print(introtext)

	# option(inactive at moment)
	#print("search terms used this session:") # should log results too? save?
	#for y in searchlog:
	#	print(y)


def filterByRegion(userinput,data):
	global currentregion,currentmode
	check=len(data)
	regiontoken=userinput.getRegionToken()
	if (regiontoken=="NA" or regiontoken.lower()=="all"):
		return data

	# treat invalid region as if no region filter
	if (regiontoken.lower() not in ["noongar","yamaji","yingarda","ngarluma","jukan","eucla"]):
		return data 

	matches=[]
	for x in data:
		cells = x.split("|")
		if (len(cells)>9):
			#argument=userinput.replace("t:","")
			docid=cells[0]
			region=cells[1]
			if (regiontoken.lower() in region.lower()):
				matches.append(x)
	if (len(matches)>len(data)):
		print("Region filter Error")
		print("Length of input:"+str(len(matches)))
		print("Length of output:"+str(len(data)))
		exit()
	return matches

def filterByAuthor(y,data):
	authortoken=y.getAuthorToken()
	if (authortoken=="NA"):
		return data

	matches=[]
	for x in data:
		cells = x.split("|")
		if (len(cells)>9):
			#argument=userinput.replace("t:","")
			docid=cells[0]
			author=cells[3]
			if (authortoken.lower() in author.lower()):
				matches.append(x)
	if (len(matches)>len(data)):
		print("Author filter Error")
		print("Length of input:"+str(len(matches)))
		print("Length of output:"+str(len(data)))
		exit()
	return matches

def filterByPage(y,data):
	pagetoken=y.getPageToken()
	if (pagetoken=="NA"):
		return data

	matches=[]
	for x in data:
		cells = x.split("|")
		if (len(cells)>9):
			#argument=userinput.replace("t:","")
			pageref=cells[9]
			if (pagetoken.lower() in pageref.lower()):
				matches.append(x)

	if (len(matches)>len(data)):
		print("Page filter Error")
		print("Length of input:"+str(len(matches)))
		print("Length of output:"+str(len(data)))
		exit()
	return matches

def filterByFile(y,data):
	filetoken=y.getFileToken()
	if (filetoken=="NA"):
		return data

	matches=[]
	for x in data:
		cells = x.split("|")
		if (len(cells)>2):
			#argument=userinput.replace("t:","")
			fileref=cells[0]
			if (filetoken.lower() in fileref.lower()):
				matches.append(x)
	return matches


def updateMode(um):
	if (um.lower()=="url"):
		return "url"
	elif (um.lower()=="fn"):
		return "fn"
	elif (um.lower()=="net"):
		return "net"
	elif (um.lower()=="def"):
		return "def"
	else:
		return "NA"

def testmatching():
	glosstoken="slow" 
	gloss="Slow, You are very"
	match=matchAnywhere(glosstoken,gloss)
	print(str(match))

def matchAnywhere(token,phrase):
	match=False
	tt=token.lower().strip()
	phrase2=phrase.lower().strip()
	if tt in phrase2:
		match=True
	return match

# match start of any word in terms with search term
def matchStart(termtoken,term):
	match=False
	teststart=termtoken.lower().strip()
	arglen=len(teststart)
	termsplits=term.lower().split(" ")
	for x in termsplits:
		if teststart in x:
			if (teststart[0:arglen] == x[0:arglen]):
				match=True
	return match		

def matchEnd(termtoken,term):
	match=False
	testend=termtoken.lower().strip()
	endlen=len(testend)
	termsplits=term.lower().strip().split(" ")
	# print("processing termend:"+testend)
	for x in termsplits:
		a=len(x)
		if testend in x and a>=endlen:
			if (testend == x[a-endlen:]):
				match=True
	return match

def matchExactly(termtoken,term):
	match=False
	if (termtoken[1:].lower().strip()==term.lower().strip()):
		match=True
	return match

def logTokens(glosstoken,termtoken,gloss,term,gm,m):
	print("glosstoken:"+glosstoken)
	print("gloss:"+gloss)
	print("gmatch:"+str(gm))
	print("term token:"+termtoken)
	print("term:"+term)
	print("tmatch:"+str(m))
	#print("g test and t start test")
	#print("g:"+str(gmatch)+" t:"+str(match))


class searchinput:

	def __init__(self):
		self.termtoken=""
		self.termtype=""
		self.glosstoken=""
		self.fntoken=""
		self.userinput=""
		self.data=""  # query if this is needed
		self.authortoken=""
		self.regiontoken=""
		self.modetoken=""
		self.pagetoken=""
		self.filetoken=""
		self.ztoken=""
		self.glosslogic=""
		self.termlogic=""

		self.termstarttoken=""
		self.termendtoken=""

	def logState(self):
		print("Term Token")
		print(self.termtoken)
		print("Term Type")
		print(self.termtype)
		print("Gloss Token")
		print(self.glosstoken)
		print("Region Token")
		print(self.regiontoken)

	def getTokenArgument(self,input,delim):
		searchtext="NA"
		if(delim) in input:
			start=input.find(delim)
			if (start!=-1):
				rightsplit=input[start+len(delim):]
				if (":" in rightsplit):
					rhstext=rightsplit.split(":")
					searchtext=rhstext[0]+":" # second entry
					cmdlist=["g","d","t","a","m","ts","te","p","f","z"]
					lt=len(searchtext)
					# capture up to next
					for x in cmdlist:
						a=x+":"
						place=searchtext.find(a)
						if (place>2):
							searchtext=searchtext[:place].strip()
							return searchtext
				else:
					searchtext=rightsplit
					return searchtext
		else:
			return searchtext

	def setupFromInput(self,userinput):
		regiontoken=self.getTokenArgument(userinput,"d:")
		termtype="any"
		termstarttoken=self.getTokenArgument(userinput,"ts:")
		termendtoken=self.getTokenArgument(userinput,"te:")
		termtoken=self.getTokenArgument(userinput,"t:")
		glosstoken=self.getTokenArgument(userinput,"g:")
		authortoken=self.getTokenArgument(userinput,"a:")
		modetoken=self.getTokenArgument(userinput,"m:")
		pagetoken=self.getTokenArgument(userinput,"p:")
		filetoken=self.getTokenArgument(userinput,"f:")
		ztoken=self.getTokenArgument(userinput,"z:")
		print(filetoken)
		if (pagetoken!="NA"):
			a=0

		# initialise variables object
		self.setRegionToken(regiontoken)
		self.setGlossToken(glosstoken)
		self.setTermToken(termtoken)
		self.setTermType(termtype)
		self.setTermStart(termstarttoken)
		self.setTermEnd(termendtoken)
		self.setAuthorToken(authortoken)
		self.setRegionToken(regiontoken)
		self.setModeToken(modetoken)
		self.setPageToken(pagetoken)
		self.setFileToken(filetoken)
		self.setZToken(ztoken)
		self.setUserInput(userinput)
		
		# userinput,data,authortoken,regiontoken,termtoken,termtype,glosstoken,modetoken,pagetoken,filetoken,ztoken

		# for single term processing in search
		if (termtoken=="NA" and termendtoken!="NA"):
			self.setTermToken(termendtoken)
			self.setTermType("end")
		if (termtoken=="NA" and termstarttoken!="NA"):
			self.setTermToken(termstarttoken)
			self.setTermType("start")
		if (termtoken!="NA" and termstarttoken!="NA"):
			termtoken=termstarttoken+"|"+termendtoken
			self.setTermToken(termtoken)
			self.setTermType("bookend")

		glogic=glosstoken[0:1]
		tlogic=termtoken[0:1]
		self.setGlossLogic(glogic)
		self.setTermLogic(tlogic)
		

	def refreshRegionToken(self,current):
		if (self.regiontoken=="NA"):
			self.regiontoken=current
		if (self.regiontoken.lower() not in ["noongar","yamaji","yingarda","ngarluma","jukan","eucla","all"]):
			self.regiontoken="NA"

	def setTermToken(self,input):
		self.termtoken=input

	def setTermType(self,input):
		self.termtype=input

	def setTermStart(self,input):
		self.termstarttoken=input

	def setTermEnd(self,input):
		self.termendtoken=input

	def setTermLogic(self,input):
		self.termlogic=input

	def setGlossToken(self,input):
		self.glosstoken=input

	def setGlossLogic(self,input):
		self.glosslogic=input

	def setFNToken(self,input):
		self.fntoken=input

	def setRegionToken(self,input):
		self.regiontoken=input

	def setAuthorToken(self,input):
		self.authortoken=input

	def setModeToken(self,input):
		self.modetoken=input

	def setPageToken(self,input):
		self.pagetoken=input

	def setFileToken(self,input):
		self.filetoken=input

	def setZToken(self,input):
		self.ztoken=input

	def setUserInput(self,input):
		self.userinput=input

	def setData(self,input):
		self.data=input

	# Getters

	def getTermToken(self):
		return self.termtoken
	
	def getTermType(self):
		return self.termtype	

	def getTermStart(self):
		return self.termstarttoken	

	def getTermEnd(self):
		return self.termendtoken

	def getTermLogic(self):
		return self.termlogic

	def getGlossToken(self):
		return self.glosstoken

	def getGlossLogic(self):
		return self.glosslogic

	def getFNToken(self):
		return self.fntoken

	def getRegionToken(self):
		return self.regiontoken

	def getAuthorToken(self):
		return self.authortoken

	def getModeToken(self):
		return self.modetoken

	def getPageToken(self):
		return self.pagetoken

	def getFileToken(self):
		return self.filetoken

	def getZToken(self):
		return self.ztoken

	def getUserInput(self):
		return self.userinput

	def getTermStart(self):
		return self.termstarttoken

	def getTermEnd(self):
		return self.termendtoken

class allbates:

	def __init__(self):

		self.docid="NA"
		self.dialect="NA"
		self.region="NA"
		self.author="NA"
		self.gloss="NA"
		self.term="NA"
		self.pageref="NA"
		self.count=0		

	def setup(self,x):
		cells = x.split("|")
		self.count=len(cells)
		if self.count>9:	
			self.docid=cells[0]
			self.region=cells[1]
			self.dialect=cells[2] # unused
			self.author=cells[3]
			# index 4,5,6 unusued at moment
			self.gloss=cells[7]
			self.term=cells[8].strip()
			self.pageref=cells[9] # this is page number ref as per Bates HTML class
		
	def logState(self):
		print("DocID:")
		print(self.docid)
		print("Region:")
		print(self.region)
		print("Dialect:")
		print(self.dialect)
		print("Author:")
		print(self.author)
		print("Gloss:")
		print(self.gloss)
		print("Term:")
		print(self.term)
		print("PageRef:")
		print(self.pageref)


	def getNumCells(self):
		return self.count

	def getDocID(self):
		return self.docid

	def getDialect(self):
		return self.dialect

	def getRegion(self):
		return self.region

	def getAuthor(self):
		return self.author

	def getGloss(self):
		return self.gloss

	def getTerm(self):
		return self.term

	def getPageRef(self):
		return self.pageref

	def getPageAndURL(self):
		page=self.getPageRef()
		bates=self.getBatesURL()
		output=page+" "+bates
		return output

	def getPageURLlink(self):
		linky=self.getBatesURL()
		output='<a href="'+linky+'">'+self.getPageRef()+'</a>'
		return output

	# http://www.bates.org.au/images/45/45-010T.jpg
	def getBatesURL(self):
		page=self.getPageRef()
		folder=page.strip("pb-")
		folio=folder[0:2]
		#print(folder)
		output='http://www.bates.org.au/images/'+folio+'/'+folder+'.jpg'
		return output

class resultobject:

	def __init__(self):
		self.cmdobject=searchinput()
		self.cells=allbates()
		self.term="NA"
		self.gloss="NA"
		self.termresult="NA"
		self.glossresult="NA"
		self.fnresult="NA"
		self.netresultTerm="NA"
		self.netresultGloss="NA"
		self.docid="NA"
		self.reftext="NA"
		self.currentmode="NA"

	def setup(self,cellobject,inputdata,mode):
		self.cells = cellobject
		self.cmdobject=inputdata
		self.currentmode=mode
		self.setCustomResults()

	def logState(self):
		print("Gloss Result:")
		print(self.glossresult)
		print("Term Result:")
		print(self.termresult)
		print("Net Result Term:")
		print(self.netresultGloss)

	def testpage():
		input="pb-45-010T" # this is page result not doc id
		result=getURLfromPage(input)
		print(result)
		if (result=="http://www.bates.org.au/images/45/45-010T.jpg"):
			print("Passed test")
		else:
			print("Failed Test")

	# give this the relevant data
	def setCustomResults(self):
		
		author=self.cells.getAuthor()
		region=self.cells.getRegion()
		gloss=self.cells.getGloss()
		term=self.cells.getTerm()
		docid=self.cells.getDocID()


		page=self.cells.getPageRef()
		if (len(page)>4 and self.currentmode=="url"):
			page=self.cells.getPageAndURL()

		# prepare strings
		self.glossresult=author+" "+region+" "+docid+" "+gloss+":"+term+" "+page
		self.termresult=author+" "+region+" "+docid+" "+term+":"+gloss+" "+page
		self.fnresult=term+":"+ gloss+" ("+docid+","+page+")"

		self.prepareNetworkLines()

	def prepareNetworkLines(self):
		gloss=self.cells.getGloss()
		term=self.cells.getTerm()

		cleanterm=term.replace(",","/")
		cleangloss=gloss.replace(",","/")
		
		bottomline='"'+cleanterm+'","'+cleangloss+'"'
		topline='+",'+bottomline

		# external termtoken, glosstoken used here
		termtoken=self.cmdobject.getTermToken()
		glosstoken=self.cmdobject.getGlossToken()
		spare=self.cells.getPageURLlink()
		netresultTT='"TM","'+termtoken+topline
		netresultGT='"TM","'+glosstoken+topline
		netresultG='"G",'+bottomline+',"'+spare+'"'
		self.netresultTerm=netresultTT+"\n"+netresultG
		self.netresultGloss=netresultGT+"\n"+netresultG

	def getTermResult(self,prefix):
		if (self.currentmode=="net"):
			return self.netresultTerm

		elif (self.currentmode=="fn"):
			return self.fnresult
		else:
			result=prefix+" "+self.termresult
			return result

	def getGlossResult(self,prefix):
		if (self.currentmode=="net"):
			return self.netresultGloss
		elif (self.currentmode=="fn"):
			return self.fnresult
		else:
			result=prefix+" "+self.glossresult
			return result

# userinput,data,authortoken,regiontoken,termtoken,termtype,glosstoken,modetoken,pagetoken,filetoken,ztoken
def doJoinSearch(myinput,mydata):
	global currentregion,currentmode
	
	filter1=filterByRegion(myinput,mydata)
	filter2=filterByAuthor(myinput,filter1)
	pagetoken=myinput.getPageToken()
	filetoken=myinput.getFileToken()
	if (pagetoken!="NA"):
		filter2=filterByPage(myinput,filter2)
	if (filetoken!="NA"):
		filter2=filterByFile(myinput,filter2)

	# to do: filter by document reference

	modetoken=myinput.getModeToken()
	if (modetoken!="NA"):
		if (modetoken=="NIL"):
			currentmode=="NA"
		else:
			currentmode=updateMode(modetoken)

	regiontoken=myinput.getRegionToken()
	tagline="Current dialect:"+currentregion+", input dialect:"+regiontoken+", currentmode:"+currentmode
	logoutput(tagline)
	resultcount=0
	justterms=[]
	
	# input parameters
	termtoken=myinput.getTermToken()
	termtype=myinput.getTermType()
	glosstoken=myinput.getGlossToken()
	glosscmd=glosstoken
	glogic=myinput.getGlossLogic()
	tlogic=myinput.getTermLogic()
	termstarttoken=myinput.getTermStart()
	termendtoken=myinput.getTermEnd()
	
	searchcode=0
	searchterm=""
	ztoken=myinput.getZToken()
	if ztoken!="NA":
		print("z test ok")

		return
	counter=0
	for x in filter2:
		result=""
		
		mycell=allbates()
		mycell.setup(x)
		cellnum=mycell.getNumCells()
		gloss=mycell.getGloss()
		term=mycell.getTerm()

		myresult=resultobject()
		myresult.setup(mycell,myinput,currentmode)
		#mycell.logState()
		#myresult.logState()
		#myinput.logState()
		
		if (cellnum>9):
			multi=False
			searchcode=0
			if glosscmd!="NA" and termtoken!="NA":
				multi=True # "x AND y"
				searchcode=1
				searchterm=glosstoken+"|"+termtoken

			if multi==False:
				if termtoken!="NA":
					if termtype=="any":
						if tlogic!="=":
							searchcode=2
							searchterm=termtoken
						
						# exact match
						if tlogic=="=":
							searchcode=3
							searchterm=termtoken

					if termtype=="start":
							searchcode=6
							searchterm=termtoken
					if termtype=="end":
							searchcode=7
							searchterm=termtoken

					if termtype=="bookend":
							searchcode=8


				if glosscmd!="NA":
		
					if glogic!="=":
						searchcode=4
						searchterm=glosscmd

					if glogic=="=":
						searchcode=5
						searchterm=glosscmd

			if multi==True and searchcode==1 and termtype=="any":	
				gmatch=matchAnywhere(glosscmd,gloss)
				match=matchAnywhere(termtoken,term)
				#logTokens(glosstoken,termtoken,gloss,term)
				if match==True and gmatch==True:
					result=myresult.getGlossResult("GT")
					resultcount=resultcount+1
			
			if multi==True and searchcode==1 and termtype=="start":
				gmatch=matchAnywhere(glosscmd,gloss)
				match=matchStart(termtoken,term)
				if match==True and gmatch==True:
					result=myresult.getGlossResult("GT")
					resultcount=resultcount+1
					searchterm=glosstoken+"|"+termtoken

			if multi==True and searchcode==1 and termtype=="end":
				
				gmatch=matchAnywhere(glosscmd,gloss)
				match=matchEnd(termtoken,term)
				#logTokens(glosstoken,termtoken,gloss,term,gmatch,match)
				if match==True and gmatch==True:
					result=myresult.getGlossResult("GT")
					resultcount=resultcount+1
					searchterm=glosstoken+"|"+termtoken

			if multi==True and searchcode==1 and termtype=="bookend":
				gmatch=matchAnywhere(glosscmd,gloss)
				match=matchStart(termstarttoken,term)
				match2=matchEnd(termendtoken,term)
				if match==True and match2 ==True and gmatch==True:
					result=myresult.getGlossResult("GTT")
					resultcount=resultcount+1
					searchterm=glosstoken+"|"+termtoken

			if searchcode==2:
				match=matchAnywhere(termtoken,term)
				if match==True:
					result=myresult.getTermResult("T")
					resultcount=resultcount+1
					
			if searchcode==3:
				match=matchExactly(termtoken,term)
				if match==True:
					result=myresult.getTermResult("T")
					resultcount=resultcount+1
					

			if searchcode==4:	
				match=matchAnywhere(glosstoken,gloss)
				if match==True:
					result=myresult.getGlossResult("G")
					resultcount=resultcount+1
					
			if searchcode==5:
				match=matchExactly(glosstoken,gloss)
				if match==True:
					result=myresult.getGlossResult("G")
					resultcount=resultcount+1

			if searchcode==6:
				match=matchStart(termtoken,term)
				if match==True:
					result=myresult.getTermResult("T")
					resultcount=resultcount+1	

			if searchcode==7:
				match=matchEnd(termtoken,term)
				if match==True:
					result=myresult.getTermResult("T")
					resultcount=resultcount+1	

			if searchcode==8:
				match=matchStart(termstarttoken,term)
				match2=matchEnd(termendtoken,term)
				if match==True and match2 ==True:
					result=myresult.getGlossResult("TT")
					resultcount=resultcount+1
					searchterm=termstarttoken+"|"+termendtoken


			if searchcode==0:
				if pagetoken!="NA":
					result=myresult.getTermResult("P")
					resultcount=resultcount+1	
				elif (pagetoken=="NA" and filetoken!="NA"):
					result=myresult.getTermResult("F")
					resultcount=resultcount+1	
				else:
					result="NIL" # do nothing

			#print(termtoken)
			if (len(result)>0 and result!="NIL"):
				print(result)
				justterms.append(term)
	userinput=myinput.getUserInput()
	resultline=userinput+". Total results returned:"+str(resultcount)+" subset:"+regiontoken
	logoutput(resultline)
	pair=[searchterm,resultcount,justterms]
	return pair

def logoutput(input):
	mode=True
	if (mode==True):
		print(input)

def processinput(userinput,data):
	global currentregion
	indata=searchinput()
	indata.setupFromInput(userinput)
	indata.refreshRegionToken(currentregion)
	#indata.logState()
	regiontoken=indata.getRegionToken()
	if regiontoken!="NA":
		currentregion=regiontoken
	output=doJoinSearch(indata,data)
	return output

#permutations of 3 letter search terms
def permuteAlpha3(input):
	g = list(string.ascii_lowercase)
	searchlist=[]
	print(g)
	for fp in g:
		for sp in g:
			for tp in g:
				chord=fp+sp+tp
				searchterm=input+":"+chord
				searchlist.append(searchterm)
				#print(searchterm) 
	return searchlist

#permutations of 3 letter search terms
def permuteAlpha4(input):
	g = list(string.ascii_lowercase)
	searchlist=[]
	print(g)
	for fp in g:
		for sp in g:
			for tp in g:
				for fr in g:
					chord=fp+sp+tp+fr
					searchterm=input+":"+chord
					searchlist.append(searchterm)
				#print(searchterm) 
	return searchlist

def bulkAlphaSearch():
	category="t"
	trigramlist=permuteAlpha3(category)
	bulkSearch(trigramlist,False)

def bulkAlphaSearch4():
	category="t"
	trigramlist=permuteAlpha4(category)
	bulkSearch(trigramlist,False)

global searchlog
global currentregion
global currentmode
global helptext
global introtext

introtext="""
Digital Bates Search tool
---------------------------
By Craig Duncan October 2023 (Queries: craig[@]digihum.au). 

Source Data
------------
Source information and licence: 
Nick Thieberger. 2017. Digital Daisy Bates. Web resource. http://bates.org.au.
https://creativecommons.org/licenses/by-nc/4.0/ 

Source Data Disclaimer and adaption:
------------------------------------
The source data for this tool, allbates.csv is an adapted form 
of the HTML data at the origin site as at July 2023. It 
incorporates original terms, glossary, author, docid, page ID.

The dialect region (second field i.e. NA, noongar,yingarda etc) is 
approximate only, based on manuscript descriptions and original 
Bates document map information (index.json). Please make sure you
check dialects yourself if you wish to rely on it.

Licence for this work (script and adaptation):
----------------------------------------------
The python code for search.py and the allbates.csv file is made 
available under a CC-BY-NC-SA 4.0 licence. 
(https://creativecommons.org/licenses/by-nc-sa/4.0/).
Please include this notice if you adapt or modify.

Enter help at command line for further command line information.

Last updated: 20 October 2023.

"""

helptext="""

Digital Bates Search tool HELP
-------------------------------
General queries can be directed to craig[@]digihum.au

General Search Commands
------------------------
- a: specify author (e.g. Ngilgi) to filter search entries by
- t: search for term (indigenous) anywhere in the terms field
- t:= search for an exact textual match for the term field (case independent) 
- ts: search for match at start of any word in term field
- te: search for match at end of any word in term field.
- g: search for gloss (English) anywhere in the gloss field
- g:= search for an exact textual match in the gloss (English) field. (case independent) 
- p: specify the page numbers (filters the same search by page number e.g. 41-250)
- f: specify the file number (filters the same search by folder number) e.g. 42-186

If no other terms are used for the p and f options, the search will return all entries for page or folder/file as specified.

All spaces between words after search commands will be treated as part of the search term (up to next search term entered)

You can combine g and t,ts or te queries on the same line.  

Persistent mode options (do not need to be re-entered until you want to change)

Mode and Dialect options
------------------------
- m: set to NA (default), url or fn.  
	Default mode is full results, but with page numbers not URLs
	If url is on, all the Bates page numbers return as URL suitable for browser.  
	If fn (footnote) mode is on, returns abridged result (term, gloss and docid/pageid) is returned.
	If net (semantic net) mode is on, returns result in a data format to use with my pyvis utility.

- d: dialect (use this to filter results)
 
 dialect options: noongar,yamaji,yingarda,ngarluma,jukan,eucla
 (anything else will restore to NA i.e. all regions)

 Exit and help (this page)
 -------------------------
Enter help or licence on the command line to reproduce the information.
Enter exit to leave the program.

Last updated: 20 October 2023.

"""
currentmode="NA"
currentregion="NA"
searchlog=[]
#runtests()
main()
