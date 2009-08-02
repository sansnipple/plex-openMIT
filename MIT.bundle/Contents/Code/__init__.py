# Plex PLugin for MIT open courseware

# this program is distributed under the terms of the GNU General Public License

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import re, string
from PMS import *
from PMS.Objects import *
from PMS.Shortcuts import *

MIT_PREFIX   = "/video/MIT"

CACHE_INTERVAL = 3600


###################################################################################################
def Start():
  Plugin.AddPrefixHandler(MIT_PREFIX, MainMenu, 'MIT Open Courseware', )
  Plugin.AddViewGroup("Details", viewMode="InfoList", mediaType="items")
  MediaContainer.title1 = 'MIT Open Courseware'
  MediaContainer.content = 'Items'
#  MediaContainer.art = R('')
  HTTP.SetCacheTime(CACHE_INTERVAL)

###################################################################################################
def MainMenu():
	dir = MediaContainer()
	dir.Append(Function(DirectoryItem(video, title="Courses with Complete Video Lectures")))
	dir.Append(Function(DirectoryItem(audio, title="Courses with Complete Audio Lectures")))
	return dir

######################################

def video(sender):
	dir = MediaContainer(title2="Video Lectures")
	
	frontPage = XML.ElementFromURL("http://ocw.mit.edu/OcwWeb/web/courses/av/index.htm", isHTML=True, errors="ignore")
	vCourses = frontPage.xpath("//img[@alt='Complete video lectures']//parent::*//parent::*//parent::*//td[4]/a")
	
	for x in range(len(vCourses)):
		title = vCourses[x].text
		url = "http://ocw.mit.edu" + frontPage.xpath("//img[@alt='Complete video lectures']//parent::*//parent::*//parent::*//td[4]/a//@href")[x]
#		Log(title)
#		Log(url)
		dir.Append(Function(DirectoryItem(getListing, title=title+""), title2=title+"", url=url+"", media="video"))

	
	return dir

def audio(sender):
	dir = MediaContainer(title2="Audio Lectures")	
#	"//img[@alt='Complete audio lectures']"
	
	frontPage = XML.ElementFromURL("http://ocw.mit.edu/OcwWeb/web/courses/av/index.htm", isHTML=True, errors="ignore")
	aCourses = frontPage.xpath("//img[@alt='Complete audio lectures']//parent::*//parent::*//parent::*//td[4]/a")
	
	for x in range(len(aCourses)):
		title = aCourses[x].text
		url = "http://ocw.mit.edu" + frontPage.xpath("//img[@alt='Complete audio lectures']//parent::*//parent::*//parent::*//td[4]/a//@href")[x]
#		Log(title)
#		Log(url)
		dir.Append(Function(DirectoryItem(getListing, title=title+""), title2=title+"", url=url+"", media="audio"))
	

	
	
	
	return dir

def getListing(sender, title2, url, media):
	dir = MediaContainer(title2=title2)
	# For Video Courses
	if media == "video":
		url = url.replace("CourseHome/index.htm", "VideoLectures/index.htm")
 		page= XML.ElementFromURL(url, isHTML=True, errors="ignore")
		if page == None:
			url = url.replace("VideoLectures/index.htm", "Videos/index.htm")
			page = XML.ElementFromURL(url, isHTML=True, errors="ignore")
		if page == None:
			url = url.replace("Videos/index.htm", "LectureNotes/index.htm")
			page = XML.ElementFromURL(url, isHTML=True, errors="ignore")
		titles = page.xpath("id('BodyCopy1')/div/table/tbody//tr/td[2]/a")
		for x in range(len(titles)):
			title = titles[x].text
			vURL = "http://ocw.mit.edu" + page.xpath("id('BodyCopy1')/div/table/tbody//tr/td[2]/a/@href")[x]
			vPage = XML.ElementFromURL(vURL, isHTML=True, errors="ignore")
			video = str(vPage.xpath("//table[2]/tbody/tr[1]/td[2]/p[1]/a[2]/@href")).strip("[]'")
			if video == "":
				video = str(vPage.xpath("//div[1]/table[2]/tbody/tr[1]/td[1]/p[1]/a[2]/@href")).strip("[]'")
			Log(video)
			if video == "":
				video = str(vPage.xpath("//div[1]/table[2]/tbody/tr[1]/td[1]/p/span/a/@href")).strip("[]'")
			if video == "":
				video = str(vPage.xpath("//div[1]/table[2]/tbody/tr[1]/td[1]/p/a[2]/@href")).strip("[]'")
			dir.Append(VideoItem(video, title=title))
			
			
	# for Audio Courses
#	elif media == "audio":

		
		
	return dir



