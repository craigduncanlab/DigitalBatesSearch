# Search program for Bates database file 'allbates.csv'

By Craig Duncan 2023

Created 7 September 2023; last updated 4 October 2023.

# Introduction and source data

The source language data for this project from was obtained under a CC-BY-NC 4.0 Creative Commons Licence:

    Nick Thieberger. 2017. Digital Daisy Bates. Web resource. http://bates.org.au.
    https://creativecommons.org/licenses/by-nc/4.0/ 

I wish to thank Nick Thieberger for making the information available in a convenient online form.  

The data from the HTML page of the Digital Bates project has been adapted and modified in a new form (allbates.csv) to be used in an offline command line tool.  This search tool is the result of some specific queries I wished to perform for a digital humanities project, and I thought it might be useful to share.  If there is interest, and Nick is supportive, it should be easy to adapt this to a web-based search tool.

The Digital Bates source data was published on condition the moral rights of the speakers/authors of language were preserved.  I respect that request. I have extracted the informant names that appear in the introductory parts of the source manuscripts so that they appear in each entry and can be recognised and queried as required.  

Please note that the information includes specific author information, and a new field for 'region/dialect' that is my own opinion, for my own personal research.  The dialect is based on the locations given in the index.json file at the bates.org website.  In some cases, it has been supported with information within the header section of the questionnaires.  Please do not rely on the accuracy of this author and dialect information without checking it yourself.  

The above attributions and explanation are provided to conform to the original CC-BY-NC 4.0 licence terms. 

# Licence for this project 

The python code for search.py and the adapted data used for the program (in the allbates.csv file) is made available, under a CC-BY-NC-SA licence (https://creativecommons.org/licenses/by-nc-sa/4.0/). This is mostly the same as the original data, with an additional 'Share Alike" condition. This means you must include these same licence terms in any modified version of the code or data.  

All queries regarding this program and the data can be emailed to: craig[@]digihum.au).

# Instructions for running program

Run the program by typing the following instruction on the command line:
```
python3 search.py
```
You should run the code with all files in the same directory.

The program will present an interactive input screen where you can type search commands (see below, or type 'help' in the program).

Enter the word 'exit' to exit program.

# Search command-line options 

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

Please include a colon after each search term. All spaces between words after search commands will be treated as part of the search term (up to next search term entered)

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

 Exit and help 
 -------------------------

Enter exit or help on the command line.

# Illustrations of use

## Exact match on term

```
>:t:=dardar
NA
Current dialect:NA, input dialect:NA, currentmode:NA
T Boordenam>Beereenan>Boongong>Werdabirt Noongar 40-096T Dardar:Clay, white lime pb-40-115T
T Wooralgula tribe Noongar 41-050T Dardar:Clay, white lime pb-41-072T
T Wooralgula tribe Noongar 41-050T Dardar:White pb-41-087T
T Bardil Noongar 41-097T Dardar:Clay, white pb-41-107T
T Kajaman Noongar 41-133T Dardar:Clay, white lime pb-41-154T
T Ngilgi Noongar 41-179T Dardar:White pb-41-219T
T NA Noongar 42-186T Dardar:Clay, white pb-42-195T
T NA Noongar 42-217T Dardar:Clay, white pb-42-227T
T NA Noongar 42-217T Dardar:Lime pb-42-228T
T NA Noongar 42-217T Dardar:Clay, white lime pb-42-234T
T NA Noongar 42-217T Dardar:White pb-42-248aT
T Bardil Noongar 44-001T dardar:White pb-44-010T
T NA Noongar 45-067T dardar:Clay, white pb-45-078T
T NA Noongar 45-067T dardar:Lime pb-45-079T
t:=dardar. Total results returned:14 subset:NA
```

## Set to return only ngoongar words

```
>:d:noongar

```
You can do this initially with other options to perform search at same time
```
>:d:noongar m:url g:Swan


...

G NA Noongar 45-049T Swan:male>culgia pb-45-053T http://www.bates.org.au/images/45/45-053T.jpg
G NA Noongar 45-056T Swan:culjack pb-45-059T http://www.bates.org.au/images/45/45-059T.jpg
G NA Noongar 45-062T Swan:weel-ree>mar-lac pb-45-064T http://www.bates.org.au/images/45/45-064T.jpg
G NA Noongar 45-067T C. Symons, Perth, 1842 F.F. Armstrong, 1841 P. Chauncy, Swan River W. G. Knight, Swan River Captain Stokes, Swan River, 1837 R. M. Lyon, Perth, 1833. MSS:pb-45-067T 
G NA Noongar 45-067T Swan:gooljak>kooleeja>maalee pb-45-075T http://www.bates.org.au/images/45/45-075T.jpg
G Wingadee Noongar 56-145T Swan:Koorilya pb-56-153T http://www.bates.org.au/images/56/56-153T.jpg
d:noongar m:url g:Swan. Total results returned:49 subset:noongar
```

## Footnote mode

```
>:t:gwert m:fn
...
Gwert:To throw (41-027T,pb-41-033T)
Wanga gwert:Call him back (41-050T,pb-41-072T)
Ngoogoo gwert:Sugar (41-050T,pb-41-085T)
Yang gwert:Birth (41-097T,pb-41-112T)
Ұeng gwert:Born (41-097T,pb-41-112T)
Wang gwert:Call, to (41-097T,pb-41-113T)
Baam bullarra gwert:Knock, to (down) (41-097T,pb-41-118T)
Burrong wat gwert a bardong:Push, to (41-097T,pb-41-121T)
Jed gwert:Recover, to (41-097T,pb-41-121T)
Wang gwert:Call him back (41-133T,pb-41-154T)
Wanga gwert:Call, to (41-179T,pb-41-200T)
Yookat gwert:Fall, to (41-179T,pb-41-204T)
Mūn gwert, mūn-i-ēja:Throw it away (41-227T,pb-41-249T)
Wânga gwert:To call>call (41-227T,pb-41-261T)
Yūkăt gwert:To fall (41-227T,pb-41-264T)
Yeya kwejjert yena-gwert:Birth (41-320T,pb-41-342T)
Yeya kwejjat-yena gwert:Born (41-320T,pb-41-343T)
Ngardee gwert:Drown, to (42-001T,pb-42-025T)
Bōm burrong gwert:Knock, to (down) (42-001T,pb-42-030T)
Burrong gwert:Push, to (42-001T,pb-42-034T)
Geejal gwert:Spear, to (42-001T,pb-42-037T)
Kwert don>gwert don:Throw, to (42-001T,pb-42-039T)
Kwert don>gwert don:Throwing (42-001T,pb-42-039T)
Yoodurn gwert:Tie, to (42-001T,pb-42-039T)
Bărdong gwert ngundīn:Flat>to lie (42-154T,pb-42-159T)
```

## Search for a phrase at start

Let's say you think that 'wa' has something to do with wind and you want to search for all the Noongar terms that start with wa and have 'Wind' in the glossary.

You then can do this search:

is 'wa' for wind?

```
>:ts:wa g:wind
Current dialect:noongar, input dialect:noongar, currentmode:NA
GT Indar>Joowel>Baiungan>Frenchman's Peak>Meerungup Noongar 40-007T Wardee:Wind (North) pb-40-018T
GT NA Noongar 40-195T Mar warditch:Wind (North) pb-40-211T
GT Kaiar>Wirijan Noongar 41-000T Wanbar:Whirlwind pb-41-013T
GT Kaiar>Wirijan Noongar 41-027T Wanbar:Whirlwind pb-41-045T
GT Kajaman Noongar 41-133T Wangin:Windpipe pb-41-140T
GT Kajaman Noongar 41-133T Mar yoola>or walbunya:Wind (North) NA
GT Ngilgi Noongar 41-179T Wardurr:Whirlwind pb-41-197T
GT NA Noongar 41-273T Manna wa guttuk:Wind (North) pb-41-290T
GT NA Noongar 41-273T Mara wadarnoo:Wind (West) pb-41-290T
GT Joobaitch Noongar 41-320T Wagarr ma-ar:Wind (light) pb-41-340T
GT Ngwoonbib Noongar 42-051T Wardan goombar>too hot:Wind (North) pb-42-064T
Total results returned:11
```
If you want to compare 'wada' to 'waga' words you can do separate searches with :
```
>:ts:wada 
>:ts:waga 
```
or more specific:
```
>:ts:wada g:wind
>:ts:waga g:wind
```

## Search for words with gloss term, and specific start and end

```
>:ts:kool te:k g:Swan
NA
Current dialect:noongar, input dialect:noongar, currentmode:url
GT Wooralgula tribe Noongar 41-050T Swan:Kooljak pb-41-060T http://www.bates.org.au/images/41/41-060T.jpg
GT Ngilgi Noongar 41-179T Swan:Kooljak pb-41-189T http://www.bates.org.au/images/41/41-189T.jpg
GT Ngilgi Noongar 41-227T Swan:Kūljak pb-41-244T http://www.bates.org.au/images/41/41-244T.jpg
GT Ngilgi Noongar 41-265T Black swan:Kuljak pb-41-266T http://www.bates.org.au/images/41/41-266T.jpg
GT NA Noongar 41-273T Swan:Kuljak pb-41-282T http://www.bates.org.au/images/41/41-282T.jpg
GT Joobaitch Noongar 41-320T Swan:Kooljak pb-41-331T http://www.bates.org.au/images/41/41-331T.jpg
GT Balbuk Noongar 42-001T Swan:Kooljak pb-42-011T http://www.bates.org.au/images/42/42-011T.jpg
GT Woolberr Noongar 42-069T Swan:Kooljak pb-42-077T http://www.bates.org.au/images/42/42-077T.jpg
GT NA Noongar 43-055T Swan:koljuk>koljak pb-43-061T http://www.bates.org.au/images/43/43-061T.jpg
GT Nyilgee Noongar 44-011T Swan:cooljack pb-44-013T http://www.bates.org.au/images/44/44-013T.jpg
GT NA Noongar 45-056T Swan:culjack pb-45-059T http://www.bates.org.au/images/45/45-059T.jpg
ts:kool te:k g:Swan. Total results returned:11 subset:noongar
```

## Search for a specific manuscript

```
>:f:41-179

>:f:41-179
41-179
Current dialect:noongar, input dialect:noongar, currentmode:url
F Ngilgi Noongar 41-179T pb-41-180T:Native Vocabulary Compiled by Ngilgee, f. 
F Ngilgi Noongar 41-179T pb-41-180T:of Vasse Magisterial District 
F Ngilgi Noongar 41-179T pb-41-180T:Burrong wongee, spoken in 
F Ngilgi Noongar 41-179T pb-41-180T:Bunbury and Vasse districts 
F Ngilgi Noongar 41-179T Mungart:Aunt pb-41-181T http://www.bates.org.au/images/41/41-181T.jpg
F Ngilgi Noongar 41-179T Nobba>goonya>ngeeleean:Baby pb-41-181T http://www.bates.org.au/images/41/41-181T.jpg
F Ngilgi Noongar 41-179T Nyoongar:Blackfellow pb-41-181T http://www.bates.org.au/images/41/41-181T.jpg
F Ngilgi Noongar 41-179T Yogga:Blackwoman pb-41-181T http://www.bates.org.au/images/41/41-181T.jpg
F Ngilgi Noong

--- (etc) ---

F Ngilgi Noongar 41-179T Moon yenna ngarong:Work, Go to NA
F Ngilgi Noongar 41-179T Nganya ngordert Nganya ngardert:Wounded, I am pb-41-226T http://www.bates.org.au/images/41/41-226T.jpg
F Ngilgi Noongar 41-179T Noona kujjee nganya>ngela Nyinna kujjee nganya:You and I pb-41-226T http://www.bates.org.au/images/41/41-226T.jpg
F Ngilgi Noongar 41-179T Ngoruk>brother and sister>Bullallee>father and son>Bulla bullallee>father, mother and children>Bullin>man and wife:You two pb-41-226T http://www.bates.org.au/images/41/41-226T.jpg
F Ngilgi Noongar 41-179T I cousin two gave:Ngy'ingu dam'ina Koo'jallung yung'eer pb-41-226T http://www.bates.org.au/images/41/41-226T.jpg
F Ngilgi Noongar 41-179T I you tomorrow two carry + bye + bye give you:Ngyga mornong myeruk koojaling gonga burt yungin pb-41-226T http://www.bates.org.au/images/41/41-226T.jpg
F Ngilgi Noongar 41-179T What are you doing?:Naang-a-ginjee? pb-41-226T http://www.bates.org.au/images/41/41-226T.jpg
f:41-179. Total results returned:1356 subset:noongar

```

## Limit search to specific author

```
>:a:Ngilgi g:Sunset
NA
Current dialect:noongar, input dialect:noongar, currentmode:url
G Ngilgi Noongar 41-179T Sunset:Ngangarn gwerdin pb-41-196T http://www.bates.org.au/images/41/41-196T.jpg
G Ngilgi Noongar 41-227T The short "twilight">or "spit" between sunset and moonrise:Dēlya măr gwēding pb-41-234T http://www.bates.org.au/images/41/41-234T.jpg
G Ngilgi Noongar 41-227T Sunset:Nganggarn gwerdin pb-41-256T http://www.bates.org.au/images/41/41-256T.jpg
a:Ngilgi g:Sunset. Total results returned:3 subset:noongar

```

## Do same search in footnote mode

```
>:a:ngilgi g:sunset m:fn
NA
Current dialect:noongar, input dialect:noongar, currentmode:fn
Ngangarn gwerdin:Sunset (41-179T,pb-41-196T)
Dēlya măr gwēding:The short "twilight">or "spit" between sunset and moonrise (41-227T,pb-41-234T)
Nganggarn gwerdin:Sunset (41-227T,pb-41-256T)
a:ngilgi g:sunset m:fn. Total results returned:3 subset:noongar
```