# search.py created ~ 18-20 August 2023
# (c) Craig Duncan
# Last updated 31 August 2023, 7 Sep 2023, 21 Sep 2023
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

def testinput():
	options=["d:Noongar t:war chest g:yeti","t:Noongar g:Half","g:Fish (generic)","g:Fish (generic) d:Noongar m:url p:41-010"]
	for testinput in options:
		data=openData()
		d=getTokenArgument(testinput,"d:")
		print("region:"+d)
		t=getTokenArgument(testinput,"t:")
		print("term:"+t)
		p=getTokenArgument(testinput,"p:")
		print("page:"+p)
		g=getTokenArgument(testinput,"g:")
		print("gloss:"+g)
		print("gloss 1st char")
		print(g[0:1])
		print(g[1:])

def testinput2():
	options=["d:Noongar ts:dab g:Slow","d:Noongar g:slow te:bal","g:slow t:dab"]

	testcount=0
	passes=[]
	pass1=["Noongar","NA","dab","NA","Slow"]
	pass2=["Noongar","NA","NA","bal","slow"]
	pass3=["NA","dab","NA","NA","slow"]
	passes=[pass1,pass2,pass3]
	commands=["d:","t:","ts:","te:","g:"]
	data=openData()
	for testinput in options:
		print("Test Command:"+str(testcount))
		print("input:"+testinput)
		index=0
		passlist=passes[testcount]
		for a in commands:
			result=getTokenArgument(testinput,a)
			testvalue=passlist[index]
			if (result==testvalue):
				print(a+" passed test")
			else:
				print(a+" failed test with value:"+result)
				print(len(result))
			index=index+1
		testcount=testcount+1

def testinput3():
	options=["d:Noongar ts:ba g:Slow","d:Noongar ts:goo","d:Noongar te:doo","d:Noongar te:loo", "d:Noongar g:slow ts:dab"]
	for testinput in options:
		programmedSearch(testinput)

def testinput4():
	options=["d:Noongar g:slow ts:dab"]
	for testinput in options:
		programmedSearch(testinput)

def testinput5():
	options=["d:Noongar t:dab g:slow"]
	passlist=[38]
	testcount=0
	for testinput in options:
		a=programmedSearch(testinput)
		resultcount=int(a[1])
		passvalue=int(passlist[testcount])
		print("values returned:"+str(resultcount))
		if resultcount == passvalue:
			print('Passed test '+str(testcount+1)+" of "+str(len(options)))
		else:
			print('Failed test '+str(testcount+1)+" of "+str(len(options)))
		testcount=testcount+1

def testtoken():
	inputtxt="g:root test"
	delim="g:"
	mytest=getTokenArgument(inputtxt,delim)
	if(mytest != "root test"):
		print("Token Test Failed")
		print(mytest)
	else:
		print("Token Test Passed")
		print(mytest)
	inputstring="Kangaroo, test"
	mymatchtest=matchAnywhere(mytest,inputstring)
	if (mymatchtest==False):
		print("Match string test Passed")
		print(inputstring)
	else:
		print("Match string test FAILED")
		print(inputstring)
	inputstring="This is a root test string"
	mymatchtest=matchAnywhere(mytest,inputstring)
	if (mymatchtest==True):
		print("2nd Match string test Passed")
		print(inputstring)
	else:
		print("2nd Match string test FAILED")
		print(inputstring)

def testpage():
	inputtxt="p:45-010"
	delim="p:"
	mytest=getTokenArgument(inputtxt,delim)
	if(mytest != "45-010"):
		print("Page Test Failed")
		print(mytest)
	else:
		print("Page Test Passed")
		print(mytest)

def getTokenArgument(input,delim):
	searchtext="NA"
	if(delim) in input:
		start=input.find(delim)
		if (start!=-1):
			rightsplit=input[start+len(delim):]
			rhstext=rightsplit.split(":")
			searchtext=rhstext[0] # second entry
			#print("text arg:"+searchtext)
			cmdlist=["g","d","t","a","m","ts","te","p","f"]
			lt=len(searchtext)
			for x in cmdlist:
				captured=searchtext[lt-(len(x)+1):lt]
				captured=captured.strip()
				#print("captured pre test:"+captured)
				if (captured in cmdlist):
					searchtext=searchtext[:lt-len(captured)].strip()
					#print("delim:"+delim)
					#print("new text arg:"+searchtext)
			return searchtext
	else:
		return searchtext

def testpage():
	input="pb-45-010T" # this is page result not doc id
	result=getURLfromPage(input)
	print(result)
	if (result=="http://www.bates.org.au/images/45/45-010T.jpg"):
		print("Passed test")
	else:
		print("Failed Test")

# http://www.bates.org.au/images/45/45-010T.jpg
def getURLfromPage(input):
	folder=input.strip("pb-")
	folio=folder[0:2]
	#print(folder)
	output='http://www.bates.org.au/images/'+folio+'/'+folder+'.jpg'
	return output

def isValidRegion(regioninput):
	if (regioninput.lower() not in ["noongar","yamaji","yingarda","ngarluma","jukan","eucla"]):
		if (regioninput.lower()=="all"):
			return True
		else:
			return False
	else:
		return True
	

def filterByRegion(regiontoken,data):
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
	return matches

def filterByAuthor(authortoken,data):
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
	return matches

def filterByPage(pagetoken,data):
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
	return matches

def filterByFile(filetoken,data):
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

def doJoinSearch(userinput,data,authortoken,regiontoken,termtoken,termtype,glosstoken,modetoken,pagetoken,filetoken):
	global currentregion,currentmode
	filter1=filterByRegion(regiontoken,data)
	filter2=filterByAuthor(authortoken,filter1)
	if (pagetoken!="NA"):
		filter2=filterByPage(pagetoken,filter2)
	if (filetoken!="NA"):
		filter2=filterByFile(filetoken,filter2)
	# to do: filter by document reference

	if (modetoken!="NA"):
		currentmode=updateMode(modetoken)
	else:
		currentmode="NA"
	tagline="Current dialect:"+currentregion+", input dialect:"+regiontoken+", currentmode:"+currentmode
	logoutput(tagline)
	resultcount=0
	result=""
	justterms=[]
	glosscmd=glosstoken
	searchterm=""
	for x in filter2:
		cells = x.split("|")
		result=""
		if (len(cells)>9):
			#argument=userinput.replace("t:","")
			docid=cells[0]
			region=cells[1]
			author=cells[3]# dialect is [2]
			gloss=cells[7]
			term=cells[8].strip()
			page=cells[9] # this is page number ref as per Bates HTML class
			spare=page
			searchcode=0
			gtype=glosscmd[0:1]
			ttype=termtoken[0:1]
			multi=False
			#print("gt:"+gtype)
			#print("tt:"+ttype)
			if (len(spare)>4 and currentmode=="url"):
				spare2=getURLfromPage(spare)
				spare=spare+" "+spare2
			# prepare strings
			glossresult=author+" "+region+" "+docid+" "+gloss+":"+term+" "+spare
			termresult=author+" "+region+" "+docid+" "+term+":"+gloss+" "+spare
			fnresult=term+":"+gloss+" ("+docid+","+spare+")"

			if glosscmd!="NA" and termtoken!="NA":
				multi=True # "x AND y"
				searchcode=1
				searchterm=glosstoken+"|"+termtoken
				#print("Multi detected")

			if multi==False:
				if termtoken!="NA":
					if termtype=="any":
						if ttype!="=":
							searchcode=2
							searchterm=termtoken
						
						# exact match
						if ttype=="=":
							searchcode=3
							searchterm=termtoken

					if termtype=="start":
							searchcode=6
							searchterm=termtoken
					if termtype=="end":
							searchcode=7
							searchterm=termtoken

				if glosscmd!="NA":
		
					if gtype!="=":
						searchcode=4
						searchterm=glosscmd

					if gtype=="=":
						searchcode=5
						searchterm=glosscmd

			#print("Searchcode:"+str(searchcode))
			if multi==True and searchcode==1 and termtype=="any":	
				gmatch=matchAnywhere(glosscmd,gloss)
				match=matchAnywhere(termtoken,term)
				#logTokens(glosstoken,termtoken,gloss,term)
				if match==True and gmatch==True:
					if (currentmode=="fn"):
						result=fnresult
					else:
						result=getCustomResult("GT",glossresult)
					#result="GT "+author+" "+region+" "+docid+" "+gloss+":"+term+" "+spare
					resultcount=resultcount+1
			
			if multi==True and searchcode==1 and termtype=="start":
				gmatch=matchAnywhere(glosscmd,gloss)
				match=matchStart(termtoken,term)
				if match==True and gmatch==True:
					if (currentmode=="fn"):
						result=fnresult
					else:
						result=getCustomResult("GT",glossresult)
					#result="GT "+author+" "+region+" "+docid+" "+term+":"+gloss+" "+spare
					resultcount=resultcount+1
					searchterm=glosstoken+"|"+termtoken

			if multi==True and searchcode==1 and termtype=="end":
				#print("ok, entering g and te search...")
				gmatch=matchAnywhere(glosscmd,gloss)
				match=matchEnd(termtoken,term)
				#logTokens(glosstoken,termtoken,gloss,term,gmatch,match)
				if match==True and gmatch==True:
					#result="GT "+author+" "+region+" "+docid+" "+term+":"+gloss+" "+spare
					if (currentmode=="fn"):
						result=fnresult
					else:
						result=getCustomResult("GT",glossresult)
					resultcount=resultcount+1
					searchterm=glosstoken+"|"+termtoken

			if searchcode==2:
				match=matchAnywhere(termtoken,term)
				if match==True:
					#result="T "+author+" "+region+" "+docid+" "+term+":"+gloss+" "+spare
					if (currentmode=="fn"):
						result=fnresult
					else:
						result=getCustomResult("T",termresult)
					resultcount=resultcount+1
					
			if searchcode==3:
				match=matchExactly(termtoken,term)
				if match==True:
					if (currentmode=="fn"):
						result=fnresult
					else:
						result=getCustomResult("T",termresult)
					resultcount=resultcount+1
					

			if searchcode==4:	
				match=matchAnywhere(glosstoken,gloss)
				if match==True:
					if (currentmode=="fn"):
						result=fnresult
					else:
						result=getCustomResult("G",glossresult)
					#result="G "+author+" "+region+" "+docid+" "+gloss+":"+term+" "+spare
					resultcount=resultcount+1
					
			if searchcode==5:
				match=matchExactly(glosstoken,gloss)
				if match==True:
					if (currentmode=="fn"):
						result=fnresult
					else:
						result=getCustomResult("G",glossresult)
					#result="G "+author+" "+region+" "+docid+" "+gloss+":"+term+" "+spare
					resultcount=resultcount+1

			if searchcode==6:
				match=matchStart(termtoken,term)
				if match==True:
					if (currentmode=="fn"):
						result=fnresult
					else:
						result=getCustomResult("T",termresult)
					#result="T "+author+" "+region+" "+docid+" "+term+":"+gloss+" "+spare
					resultcount=resultcount+1	

			if searchcode==7:
				match=matchEnd(termtoken,term)
				if match==True:
					if (currentmode=="fn"):
						result=fnresult
					else:
						result=getCustomResult("T",termresult)
					#result="T "+author+" "+region+" "+docid+" "+term+":"+gloss+" "+spare
					resultcount=resultcount+1	

			if searchcode==0:
				if pagetoken!="NA":
					if (currentmode=="fn"):
						result=fnresult
					else:
						result=getCustomResult("P",termresult)
					#result="P "+author+" "+region+" "+docid+" "+term+":"+gloss+" "+spare
					resultcount=resultcount+1	
				elif (pagetoken=="NA" and filetoken!="NA"):
					if (currentmode=="fn"):
						result=fnresult
					else:
						result=getCustomResult("F",termresult)
					#result="F "+author+" "+region+" "+docid+" "+term+":"+gloss+" "+spare
					resultcount=resultcount+1	
				else:
					result="NIL" # do nothing
				#if (termtoken=="NA" and glosstoken=="NA"):
				#	result="A "+author+" "+region+" "+docid+" "+gloss+":"+term+" "+spare+" "+spare
				#	resultcount=resultcount+1
			#print(termtoken)
			if (len(result)>0 and result!="NIL"):
				print(result)
				justterms.append(term)
	resultline=userinput+". Total results returned:"+str(resultcount)+" subset:"+regiontoken
	logoutput(resultline)
	pair=[searchterm,resultcount,justterms]
	return pair

def getCustomResult(prefix,fstring):
	result=prefix+" "+fstring
	return result
					

def logoutput(input):
	mode=True
	if (mode==True):
		print(input)

def processinput(userinput,data):
	global currentregion
	regiontoken=getTokenArgument(userinput,"d:")
	if (regiontoken=="NA"):
		regiontoken=currentregion
	else:
		if isValidRegion(regiontoken):
			currentregion=regiontoken
	termtype="any"
	termstarttoken=getTokenArgument(userinput,"ts:")
	termendtoken=getTokenArgument(userinput,"te:")
	termtoken=getTokenArgument(userinput,"t:")
	if (termtoken=="NA" and termendtoken!="NA"):
		termtoken=termendtoken
		termtype="end"
	if (termtoken=="NA" and termstarttoken!="NA"):
		termtoken=termstarttoken
		termtype="start"
	glosstoken=getTokenArgument(userinput,"g:")
	authortoken=getTokenArgument(userinput,"a:")
	modetoken=getTokenArgument(userinput,"m:")
	pagetoken=getTokenArgument(userinput,"p:")
	filetoken=getTokenArgument(userinput,"f:")
	print(filetoken)
	if (pagetoken!="NA"):
		a=0
		#
	output=doJoinSearch(userinput,data,authortoken,regiontoken,termtoken,termtype,glosstoken,modetoken,pagetoken,filetoken)
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

def runtests():
	# bulkAlphaSearch4()
	testinput()
	#testpage()
	#testinput4()
	#testmatching()
	#testinput2()
	#testinput5()
	#testtoken()

global searchlog
global currentregion
global currentmode
global helptext
global introtext

introtext="""
Digital Bates Search tool
---------------------------
By Craig Duncan October 2023 (Queries: craig[@]digihum.au). 

Source information and licence: 
Nick Thieberger. 2017. Digital Daisy Bates. Web resource. http://bates.org.au.
https://creativecommons.org/licenses/by-nc/4.0/ 

Disclaimer and adaption:
------------------------
The source data for this tool, allbates.csv is an adapted form 
of the HTML data at the origin site as at July 2023. It 
incorporates original terms, glossary, author, docid, page ID.

The dialect region (second field i.e. NA, noongar,yingarda etc) is 
approximate only, based on manuscript descriptions and original 
Bates document map information (index.json). Please make sure you
check dialects yourself if you wish to rely on it.

Licence for this work:
-----------------------
The python code for search.py and the allbates.csv file is made 
available under a CC-BY-NC-SA 4.0 licence. 
(https://creativecommons.org/licenses/by-nc-sa/4.0/).
Please include this notice if you adapt or modify.

Enter help at command line for further command line information.

Last updated: 4 October 2023.

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

- d: dialect (use this to filter results)
 
 dialect options: noongar,yamaji,yingarda,ngarluma,jukan,eucla
 (anything else will restore to NA i.e. all regions)

 Exit and help (this page)
 -------------------------
Enter help or licence on the command line to reproduce the information.
Enter exit to leave the program.

Last updated: 4 October 2023.

"""
currentmode="NA"
currentregion="NA"
searchlog=[]
#runtests()
main()
