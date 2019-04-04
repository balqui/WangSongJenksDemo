# -*- coding: utf-8 -*-

"""
Demo of each single pass of the Jenks natural breaks algorithm.
Check for companion file index.html nearby.

The algorithm proper would run this demoed process for each data point
in increasing sequence.

However, to run the demo, I am taking the very slow path of calling
the general solver for each of the possibilities - of course the real 
scheme tabulates all of them as per the Dynamic Programming strategy.
"""

about_str = """Using Brython plus a Python version by Drew Dara-Abrams
(drewda at GitHub) of Jenks Natural Breaks (almost the 
same thing as the optimum 1D k-means discretization by 
Wang and Song) to construct a veeeery inefficient demo of 
the dynamic programming strategy behind these algorithms.

Aesthetics and usability to be taken care of some day.

Get this software from https://bitbucket.org/balqui/demowangsongjenks
(clone on Mercurial or download freely).

José L Balcázar (balqui at BitBucket or GitHub), 2018, 2019"""

from browser import document, alert, html # Brython in-browser support

# four global vars - in a future version maybe I will do it cleaner
# how many values, how many clusters, the list of values, 
# and a counter to handle them as they are obtained from the user
nval = -1 # marks lack of valid input yet
nclus = 0
data = []
i = 1

def getJenksBreaks( dataList, numClass ):
  """
  Taken from https://gist.github.com/drewda/1299198
  Code from http://danieljlewis.org/files/2010/06/Jenks.pdf
  described at http://danieljlewis.org/2010/06/07/jenks-natural-breaks-algorithm-in-python/
  (but these links seem not to work anymore)
  """
  dataList.sort()
  mat1 = []
  for i in range(0,len(dataList)+1):
    temp = []
    for j in range(0,numClass+1):
      temp.append(0)
    mat1.append(temp)
  mat2 = []
  for i in range(0,len(dataList)+1):
    temp = []
    for j in range(0,numClass+1):
      temp.append(0)
    mat2.append(temp)
  for i in range(1,numClass+1):
    mat1[1][i] = 1
    mat2[1][i] = 0
    for j in range(2,len(dataList)+1):
      mat2[j][i] = float('inf')
  v = 0.0
  for l in range(2,len(dataList)+1):
    s1 = 0.0
    s2 = 0.0
    w = 0.0
    for m in range(1,l+1):
      i3 = l - m + 1
      val = float(dataList[i3-1])
      s2 += val * val
      s1 += val
      w += 1
      v = s2 - (s1 * s1) / w
      i4 = i3 - 1
      if i4 != 0:
        for j in range(2,numClass+1):
          if mat2[l][j] >= (v + mat2[i4][j - 1]):
            mat1[l][j] = i3
            mat2[l][j] = v + mat2[i4][j - 1]
    mat1[l][1] = 1
    mat2[l][1] = v
  k = len(dataList)
  kclass = []
  for i in range(0,numClass+1):
    kclass.append(0)
  kclass[numClass] = float(dataList[len(dataList) - 1])
  countNum = numClass
  while countNum >= 2:#print "rank = " + str(mat1[k][countNum])
    id = int((mat1[k][countNum]) - 2)
    #print "val = " + str(dataList[id])
    kclass[countNum - 1] = dataList[id]
    k = int((mat1[k][countNum] - 1))
    countNum -= 1
  return kclass

def about():
	alert(about_str)

def t(d, b=[]):
	"get a text version of the data, optionally with clusters marked"
	tt = ""
	if b: 
		tt += "|"
	for e in d:
		endbar = False
		tt += " " + str(e)
		if e in b: 
			tt += " |"
			endbar = True
	if b and not endbar:
			tt += " |"
	return tt

def start(event):
	"get quantity of points and clusters"
	global nval, nclus
	nclus = int(document["numclusters"].value)
	nval = int(document["numvalues"].value)
	if nval+1 < nclus:
		"an additional value will come later on"
		alert("Please provide sufficient values to cluster.")
		nval = -1 # marks lack of valid input yet
		nclus = 0
		document["numclusters"].value = ""
		document["numvalues"].value = ""
		return
	if nclus < 2:
		alert("Please request a nontrivial clustering.")
		nval = -1 # marks lack of valid input yet
		nclus = 0
		document["numclusters"].value = ""
		document["numvalues"].value = ""
		return
	document["numclusters"].disabled = True
	document["numvalues"].disabled = True
	document['value'].disabled = False
	document['value'].placeholder = "Please input value " + str(i) + " and submit it"
	document['submitbutton'].disabled = False

def extenddata():
	"add one more point and recompute the optimum clustering of the points so far"
	global i
	i += 1
	new = float(document["value"].value)
	if new <= 0:
			alert("Please provide positive floats. Last input ignored.")
			i -= 1
			document['value'].value = ""
			document['value'].placeholder = "Please input value " + str(i) + " and submit it"
			return
	if data:
		if data[-1] >= new:
			alert("Please provide the points in increasing order. Last input ignored.")
			i -= 1
			document['value'].value = ""
			document['value'].placeholder = "Please input value " + str(i) + " and submit it"
			return
	data.append(new)
	if len(data) < nclus:
		document['allvalues'].text = t(data)
	else:
		b = getJenksBreaks(data, nclus)
		document['allvalues'].text = t(data, b)
	if i > nval:
		"i started counting at 1"
		document['value'].disabled = True
		document['submitbutton'].disabled = True
		document['startbutton'].disabled = True
		document['newvalue'].disabled = False
		document['submitnewbutton'].disabled = False
		document['newvalue'].placeholder = "Please input one additional value and submit it"
	else:
		document['value'].value = ""
		document['value'].placeholder = "Please input value " + str(i) + " and submit it"

def go(ev):
	"actual process: compute clusterings of initial segments"
	new = float(document["newvalue"].value)
	if data[-1] >= new:
		alert("Please provide the points in increasing order. Last input ignored.")
		document['newvalue'].value = ""
		document['newvalue'].placeholder = "Please input one additional value and submit it"
		return
	document['newvalue'].disabled = True
	document['submitnewbutton'].disabled = True
	data.append(new)
	for i in range(nclus-1, len(data)):
		b = getJenksBreaks(data[:i], nclus-1)
		document['allclus'] <= html.P(t(data, b))
	b = getJenksBreaks(data, nclus)
	document['bestclus'].text = t(data, b)



# main program: 
# bind buttons to processes and leave everything for Brython to care for.

document['aboutbutton'].bind('click', about)

document['startbutton'].bind('click', start)

document['submitbutton'].bind('click', extenddata)

document['submitnewbutton'].bind('click', go)

