import urllib
import requests
import time 

from bs4 import BeautifulSoup

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.utils.timezone import utc

OPENSUBTITLES_URL = 'http://api.opensubtitles.org/xml-rpc'

def index(request):
	if request.method == 'POST':
		startApp = time.clock()
		if request.POST.get('q') == '':
			return HttpResponseRedirect('/')	
		query = urllib.quote( request.POST.get('q') )
		# htmlData = urllib2.urlopen(PIRATEBAY_URL+SEARCH_PATERN.replace('%s',query)).read()
		htmlData = requests.get(PIRATEBAY_URL+SEARCH_PATERN.replace('%s',query)).text
		tableData = trimTable(htmlData)
		soup = BeautifulSoup(tableData)
		torrents = makeList(soup)
		stopApp = time.clock()
		print '[performance-APP] ' + str(stopApp - startApp)
		return render(request, 'opensubtitles/index.html', {'torrents': torrents, 'q': request.POST.get('q')})
	else:
		return render(request, 'opensubtitles/index.html')


def trimTable(htmlData):
	begin = '<table id="searchResult">'
	end = '</table>' 
	start = time.clock()
	tableData = 'not found ):'
	if (htmlData):
		tableData = htmlData[htmlData.find(begin):htmlData.find(end)+len(end)]
	stop = time.clock()
	print '[performance-trimTable] ' + str(stop - start)
	return tableData


def trimTorrentLink(htmlData):
	begin = 'href="magnet:'
	end = 'Get this torrent">'
	start = time.clock()
	tableData = 'not found ):'
	if (htmlData):
		tableData = htmlData[htmlData.find(begin)+6:htmlData.find(end)-9]
	stop = time.clock()
	print '[performance-trimTorrentLink] ' + str(stop - start)
	return tableData


def makeList(table):
	start = time.clock()
	result = []
	allrows = table.findAll('tr', limit=3)
	for row in allrows:
		result.append([])
		allcols = row.findAll('td')
		for col in allcols:
			thestrings = [unicode(s) for s in col.findAll(text=True)]
			thetext = ''.join(thestrings)
			result[-1].append(thetext)
			print 'col' + str(col)
			urlTag = col.find('a', 'detLink')
			if urlTag:
				url = PIRATEBAY_URL+urlTag.get('href')
				result[-1].append(url)
			urlTag = col.find('a', title='Download this torrent using magnet')
			if urlTag:
				url = urlTag.get('href')
				result[-1].append(url)
	stop = time.clock()
	print '[performance-makeList] ' + str(stop - start)
	return result


def logIn(user, password, language, userAgent):
	xmlRequest = '<?xml version="1.0"?>' \
		'<methodCall>' \
		'  <methodName>LogIn</methodName>' \
		'  <params>' \
		'    <param>' \
		'      <value><string>'+user+':s</string></value>' \
		'    </param>' \
		'    <param>' \
		'      <value><string>'+password+':s</string></value>' \
		'    </param>' \
		'    <param>' \
		'      <value><string>'+language+':s</string></value>' \
		'    </param>' \
		'    <param>' \
		'      <value><string>'+userAgent+':s</string></value>' \
		'    </param>' \
		'  </params>' \
		'</methodCall>'

	return xmlRequest


def logOut(token):
	xmlRequest = '<?xml version="1.0"?>' \
		'<methodCall>' \
		'  <methodName>LogOut</methodName>' \
		'  <params>'   \
		'    <param>'  \
		'      <value><string>'+token+':s</string></value>' \
		'    </param>' \
		'  </params>'  \
		'</methodCall>'

	return xmlRequest


def searchSubtitles(token, language, movieHash, movieSize):
	xmlRequest = '<?xml version="1.0"?>' \
		'<methodCall>' \
		'  <methodName>SearchSubtitles</methodName>' \
		'  <params>' \
		'    <param>' \
		'      <value><string>'+token+':s</string></value>' \
		'    </param>' \
		'  <param>' \
		'   <value>' \
		'    <array>' \
		'     <data>' \
		'      <value>' \
		'       <struct>' \
		'        <member>' \
		'         <name>sublanguageid</name>' \
		'         <value><string>'+language+':s</string>' \
		'         </value>' \
		'        </member>' \
		'        <member>' \
		'         <name>moviehash</name>' \
		'         <value><string>'+movieHash+':s</string></value>' \
		'        </member>' \
		'        <member>' \
		'         <name>moviebytesize</name>' \
		'         <value><double>'+movieSize+':d</double></value>' \
		'        </member>' \
		'       </struct>' \
		'      </value>' \
		'     </data>' \
		'    </array>' \
		'   </value>' \
		'  </param>' \
		' </params>' \
		'</methodCall>'

	return xmlRequest

def searchSubtitlesQuery(token, language, query):
	xmlRequest = '<?xml version="1.0"?>' \
		'<methodCall>' \
		'  <methodName>SearchSubtitles</methodName>' \
		'  <params>' \
		'    <param>' \
		'      <value><string>'+token+':s</string></value>' \
		'    </param>' \
		'  <param>' \
		'   <value>' \
		'    <array>' \
		'     <data>' \
		'      <value>' \
		'       <struct>' \
		'        <member>' \
		'         <name>sublanguageid</name>' \
		'         <value><string>'+language+':s</string>' \
		'         </value>' \
		'        </member>' \
		'        <member>' \
		'         <name>query</name>' \
		'         <value><string>'+query+':s</string></value>' \
		'        </member>' \
		'       </struct>' \
		'      </value>' \
		'     </data>' \
		'    </array>' \
		'   </value>' \
		'  </param>' \
		' </params>' \
		'</methodCall>'

	return xmlRequest

# def getTorrentLink(url):
# 	torrentURL = 'error'
# 	htmlData = urllib2.urlopen(PIRATEBAY_URL+url).read()
# 	print '[getTorrentLink] ' +PIRATEBAY_URL+url

# 	start = time.clock()

# 	# soup = BeautifulSoup(trimHTML('href="magnet:','Get this torrent">',htmlData))
# 	# print 'get this torrent: ' + trimTorrentLink(htmlData)
# 	# torrentURL = soup.find('a', title='Get this torrent').get('href')

# 	stop = time.clock()
# 	print '[performance-getTorrentLink] ' + str(stop - start)

# 	return trimTorrentLink(htmlData) 

# 	# print '[torrentURL] '+str(torrentURL)


# @login_required
# def story(request):
# 	if request.method == 'POST':
# 		form = StoryForm(request.POST)
# 		if form.is_valid():
# 			story =	form.save(commit=False)
# 			story.moderator = request.user
# 			story.save()
# 			return HttpResponseRedirect('/')
# 	else:
# 		form = StoryForm()
# 	return render(request, 'stories/story.html', {'form': form})

# @login_required
# def vote(request):
# 	story = get_object_or_404(Story, pk=request.POST.get('story')) 
# 	story.points += 1
# 	story.save()
# 	user = request.user
# 	user.liked_stories.add(story)

# 	return HttpResponse()