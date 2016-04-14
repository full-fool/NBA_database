#coding=utf-8
import json
import sys
import urllib2, urllib
import re
import codecs
import json
import os
import socket
import time
from bs4 import BeautifulSoup
import random

socket.setdefaulttimeout(50)
reload(sys)
sys.setdefaultencoding('utf8')

tryTimes = 3




def getPageWithSpecTimes(decodeType, url):
    tryTimes = 4
    alreadyTriedTimes = 0
    html = None
    while alreadyTriedTimes < tryTimes:
        try:
            if decodeType == 0:
                html = urllib2.urlopen(url).read()                
            elif decodeType == 1:
                html = urllib2.urlopen(url).read().decode('gb2312', 'ignore').encode('utf8')
            elif decodeType == 2:
                html = urllib2.urlopen(url).read().decode('gbk', 'ignore').encode('utf8')
            elif decodeType == 3:
                html = urllib2.urlopen(url).read().decode('GBK', 'ignore').encode('utf8')
            else:
                html = urllib2.urlopen(url).read()
            break
        except Exception as ep:
            print ep.message
            alreadyTriedTimes += 1
            if alreadyTriedTimes == 1:
                time.sleep(1)
            elif alreadyTriedTimes == 2:
                time.sleep(60)
            elif alreadyTriedTimes == 3: 
                time.sleep(300)
            else:
                return None
    return html


def insertCompetition():
	fileContent = open('champions.html').read()

	#<tr> <td><strong>2014</strong></td> <td>San Antonio Spurs</td> <td>4-1</td> <td>Miami Heat</td> </tr>

	cpInfoPt = re.compile(r'<strong>(\d{4})</strong></td> <td>(.+?)</td>')
	cpInfoList = cpInfoPt.findall(fileContent)
	print cpInfoList
	filehandler = open('insertSql.sql', 'w')
	for eachCp in cpInfoList:
		year = eachCp[0]
		winner = eachCp[1]
		filehandler.write('INSERT INTO competition VALUES(%s, \'%s\');\n' % (year, winner))

	exit()


def insertReferees():
	fileContent = open('referees.html').read()
	#<p class="p1"><b>63</b> Derek Richardson<br />
	refereeNamePt = re.compile(r'<p class=".+?</b>(.+?)<br')
	refereesList = refereeNamePt.findall(fileContent)
	#print refereesList
	filehandler = open('insertReferee.sql', 'w')
	alreadyList = ['Derrick Collins', 'Dan Crawford', 'David Guthrie', 'Ed Malloy', 'Eli Roe', 'Gary Zielinski']
	crrId = 11
	for i in range(len(refereesList)):
		if refereesList[i].strip() in alreadyList:
			continue
		year = random.randrange(1950, 1971)
		month = random.randrange(1, 13)
		day = random.randrange(1, 29)
		filehandler.write('INSERT INTO referee VALUES (%s, \'%s\', \'USA\', \'%s-%s-%s\');\n' % (crrId, refereesList[i].strip(), year, month, day))
		crrId += 1
	filehandler.close()


def insertPlayerPlaysin(url, clubid, startId):
	htmlPage = getPageWithSpecTimes(0, url)
	#print htmlPage
	#return
	#<td >0</td><td class="sortcell"><a href="http://espn.go.com/nba/player/_/id/4240/avery-bradley">Avery Bradley</a></td><td>PG</td><td >25</td><td >6-2</td><td >180</td><td>Texas</td><td>$7,730,337</td></tr><tr class="evenrow player-46-6581">
	#class="sortcell"><a href="http://espn.go.com/nba/player/_/id/4240/avery-bradley">Avery Bradley</a></td><td>PG</td><td >25</td><td >6-2</td><td >180</td><td>Texas</td><td>$7,730,337</td>
#	playersPt = re.compile(r'<td class="sortcell"><a href=".+?">(.+?)</a></td><td>(.+?)</td><td >(\d+)</td><td >.+?</td><td>$(.+?)</td>')
	playersList = ['Kobe Bryant','Anthony Brown','Louis Williams','Stephen Curry','Draymond Green','Andrew Bogut',\
		'Josh Smith','Dwight Howard','James Harden','David Lee','Jose Juan Barea','Aaron Gordon','Dewayne Dedmon',\
		'Jason Thompson','James Johnson']
	playersPt = re.compile(r'<td class="sortcell"><a href=".+?">(.+?)</a></td><td>(.+?)</td><td >(\d+)</td><td >.+?</td><td>\$(.+?)</td>')

	playersInfoList = playersPt.findall(htmlPage)
	print len(playersInfoList)
	filehandler = open('insertPlayers.sql', 'a')
	validPlayersNum = 0
	for i in range(len(playersInfoList)):
		#INSERT INTO PLAYER VALUES (1, 'Kobe Bryant', 'USA', '1978-8-23','SG');
		#INSERT INTO playsIn VALUES (1, 1, 25000000, 2015, 2016);

		name = playersInfoList[i][0].strip()
		if name in playersList or len(name) > 30:
			continue
		position = playersInfoList[i][1].strip()
		age = playersInfoList[i][2].strip()
		year = 2016 - int(age)
		month = random.randrange(1, 13)
		day = random.randrange(1, 29)
		tmpSalary = playersInfoList[i][3].strip()
		salary = tmpSalary.replace(',', '')
		filehandler.write('INSERT INTO PLAYER VALUES (%s, \'%s\', \'USA\', \'%s-%s-%s\',\'%s\');\n' % (startId + validPlayersNum, name, \
			year, month, day, position))
		filehandler.write('INSERT INTO PLAYSIN VALUES (%s, %s, %s, 2015, 2016);\n' % (startId + validPlayersNum, clubid, salary))
		validPlayersNum += 1
	filehandler.write('\n\n\n')
	filehandler.close()
	print 'finish %s' % clubid
	nextStartId = startId + validPlayersNum
	return nextStartId


def insertAllPlayers():
	urlList = ['http://espn.go.com/nba/team/roster/_/name/hou/houston-rockets', \
		'http://espn.go.com/nba/team/roster/_/name/dal/dallas-mavericks',\
		'http://espn.go.com/nba/team/roster/_/name/orl/orlando-magic',\
		'http://espn.go.com/nba/team/roster/_/name/tor/toronto-raptors',\
		'http://espn.go.com/nba/team/roster/_/name/phi/philadelphia-76ers',\
		'http://espn.go.com/nba/team/roster/_/name/bos/boston-celtics', \
		'http://espn.go.com/nba/team/roster/_/name/ny/new-york-knicks',\
		'http://espn.go.com/nba/team/roster/_/name/bkn/brooklyn-nets',\
		'http://espn.go.com/nba/team/roster/_/name/chi/chicago-bulls', \
		'http://espn.go.com/nba/team/roster/_/name/det/detroit-pistons',\
		'http://espn.go.com/nba/team/roster/_/name/cle/cleveland-cavaliers', \
		'http://espn.go.com/nba/team/roster/_/name/mil/milwaukee-bucks', \
		'http://espn.go.com/nba/team/roster/_/name/ind/indiana-pacers', \
		'http://espn.go.com/nba/team/roster/_/name/atl/atlanta-hawks', \
		'http://espn.go.com/nba/team/roster/_/name/wsh/washington-wizards', \
		'http://espn.go.com/nba/team/roster/_/name/cha/charlotte-hornets', \
		'http://espn.go.com/nba/team/roster/_/name/mia/miami-heat', \
		'http://espn.go.com/nba/team/roster/_/name/utah/utah-jazz', \
		'http://espn.go.com/nba/team/roster/_/name/den/denver-nuggets', \
		'http://espn.go.com/nba/team/roster/_/name/por/portland-trail-blazers', \
		'http://espn.go.com/nba/team/roster/_/name/min/minnesota-timberwolves', \
		'http://espn.go.com/nba/team/roster/_/name/okc/oklahoma-city-thunder', \
		'http://espn.go.com/nba/team/roster/_/name/lac/los-angeles-clippers', \
		'http://espn.go.com/nba/team/roster/_/name/phx/phoenix-suns', \
		'http://espn.go.com/nba/team/roster/_/name/sac/sacramento-kings', \
		'http://espn.go.com/nba/team/roster/_/name/sa/san-antonio-spurs', \
		'http://espn.go.com/nba/team/roster/_/name/mem/memphis-grizzlies', \
		'http://espn.go.com/nba/team/roster/_/name/no/new-orleans-pelicans']
	startId = 40
	for i in range(len(urlList)):
		startId = insertPlayerPlaysin(urlList[i], i + 3, startId)

def insertMatchAccordingtoData(startId, date):
	# data should be yyyy-mm-dd
	url = 'http://sports.yahoo.com/nba/scoreboard/?date=%s' % date
	htmlPage = getPageWithSpecTimes(0, url)
	#htmlPage = open('matchinfo.html').read()

 	clubsDict ={'Los Angeles Lakers':1, 'Golden State Warriors':2,  'Houston Rockets':3, \
		'Dallas Mavericks':4, 'Orlando Magic':5, 'Toronto Raptors':6, \
	 	'Philadelphia 76er':7, 'Boston Celtics':8, 'New York Knicks':9,\
	 	'Brooklyn Nets':10, 'Chicago Bulls':11, 'Detroit Pistons':12, \
	  	'Cleveland Cavaliers':13, 'Milwaukee Bucks':14, 'Indiana Pacers':15, \
	  	'Atlanta Hawks':16,'Washington Wizards':17, 'Charlotte Hornets':18, \
	  	'Miami Heat':19, 'Utah Jazz':20,'Denver Nuggets':21,'Portland Trail Blazers':22,\
	  	'Minnesota Timberwolves':23,'Oklahoma City Thunder':24,'Los Angeles Clippers':25,\
	  	'Phoenix Suns':26, 'Sacramento Kings':27,'San Antonio Spurs':28,'Memphis Grizzlies':29,    \
		'New Orleans/OklaCity Pelicans':30 }


	matchPt = re.compile(r'<em>(.+?)</em>.+?<span class="away.+?">(\d+)</span>.+?<span class="home.+?">(\d+)</span>.+?<em>(.+?)</em>', re.S)
	matchInfoList = matchPt.findall(htmlPage)
	#print matchInfoList
	filehandler = open('insertMatch.sql', 'a')
	for i in range(len(matchInfoList)):
		away = matchInfoList[i][0]
		away = away.replace('LA', 'Los Angeles')

		awayScore = int(matchInfoList[i][1])
		homeScore = int(matchInfoList[i][2])
		home = matchInfoList[i][3]
		home = home.replace('LA', 'Los Angeles')
		for eachKey in clubsDict.keys():
			if away in eachKey:
				away = eachKey
			if home in eachKey:
				home = eachKey
		print home, away
		#return
		winner = None
		matchId = startId + i
		if awayScore > homeScore:
			winner = away
		else:
			winner = home
		#INSERT INTO match VALUES(3 ,'Dallas Mavericks','2016-01-27', 'regular');
		#INSERT INTO participatedInM VALUES (1, 1, 'home', TRUE, 112);

		filehandler.write('INSERT INTO match VALUES(%s ,\'%s\',\'%s\', \'regular\');\n' % (matchId, winner, date))
		if awayScore > homeScore:
			filehandler.write('INSERT INTO participatedInM VALUES (%s, %s, \'home\', FALSE, %s);\n' % (clubsDict[home], matchId, homeScore))
			filehandler.write('INSERT INTO participatedInM VALUES (%s, %s, \'away\', TRUE, %s);\n' % (clubsDict[away], matchId, awayScore))
		else:
			filehandler.write('INSERT INTO participatedInM VALUES (%s, %s, \'home\', TRUE, %s);\n' % (clubsDict[home], matchId, homeScore))
			filehandler.write('INSERT INTO participatedInM VALUES (%s, %s, \'away\', FALSE, %s);\n' % (clubsDict[away], matchId, awayScore))

	return startId + len(matchInfoList)

def insertMatchs():
	year = 2016
	startId = 320
	daysNum = [31,28,31,30,31,30,31,31,30,31,30,31]
	for month in range(2,5):
		end = daysNum[month - 1]
		if month == 4:
			end = 11
		start = 1
		if month == 2:
			start = 18
		for day in range(start, end+1):
			date = '2016-%s-%s' % (month, day)
			print date
			startId =  insertMatchAccordingtoData(startId, date)



#insertMatchs()


def insertMatchin():
	startId = 6
	filehandler = open('insertMatchin.sql', 'w')
	for i in range(startId, 722+1):
		#INSERT INTO matchIn VALUES (1, 2016);

		filehandler.write('INSERT INTO matchIn VALUES (%s, 2016);\n' % i)
	filehandler.close()


def insertRefereein():
	#INSERT INTO refereeIn VALUES (4, 2);
	filehandler = open('insertRefereein.sql', 'w')
	for i in range(1, 722+1):
		refereeId = random.randrange(1, 74)
		filehandler.write('INSERT INTO refereeIn VALUES (%s, %s);\n' % (refereeId, i))
	filehandler.close()


def insertPerformedin():
	playersDict = {1:(16,27), 2:(28,39), 3:(40,51), 4:(52,65),\
		5:(66,77), 6:(78, 90), 7:(91,104), 8:(105,118), 9:(119,134), \
		10:(135,149), 11:(150,164), 12:(165,179), 13:(180,193), 14:(194,209),\
		15:(210,224), 16:(225,239), 17:(240,254), 18:(255,269), \
		19:(270,282), 20:(283, 297), 21:(298,311), 22:(312,326), \
		23:(327, 339), 24:(340, 354), 25:(355, 369), 26:(370, 384), \
		27:(385,399), 28:(300, 414), 29:(415, 428), 30:(429, 447)}
	#print len(playersDict)
	#INSERT INTO performedIn VALUES (9, 2, 10, 2,3,1,7,2,2, 50);
	fileContent = open('insertMatch.sql').read()
	startFileHandler = open('insertStartsin.sql', 'w')
	#foulFileHandler = open('insertFoul.sql', 'w')
	#performHandler = open('insertPerformedin.sql', 'w')
	foulFileHandler = open('newinsertFoul.sql', 'w')
	performHandler = open('newinsertPerformedin.sql', 'w')
	currentFoulId = 1
	for mid in range(6, 722+1):
		print 'processing match %s' % mid
		#INSERT INTO match VALUES(709 ,'Milwaukee Bucks','2016-4-10', 'regular');
		#INSERT INTO participatedInM VALUES (7, 709, 'home', FALSE, 108);
		#INSERT INTO participatedInM VALUES (14, 709, 'away', TRUE, 109);
		homeClubPt = re.compile(r'INSERT INTO participatedInM VALUES \((\d+), %s, \'home\',' % mid)
		awayClubPt = re.compile(r'INSERT INTO participatedInM VALUES \((\d+), %s, \'away\',' % mid)
		homeClubId = int(homeClubPt.findall(fileContent)[0])
		awayClubId = int(awayClubPt.findall(fileContent)[0])
		homePlayerList = [i for i in range(playersDict[homeClubId][0], playersDict[homeClubId][1]+1)]
		awayPlayerList = [i for i in range(playersDict[awayClubId][0], playersDict[awayClubId][1]+1)]
		homePlayerNum = len(homePlayerList)
		awayPlayerNum = len(awayPlayerList)
		homePerformPlayerList = []
		awayPerformPlayerList = []



		homeStartList = []

		# insert 5 starts in info
		for i in range(5):
			startId = random.randrange(0, homePlayerNum)
			while homePlayerList[startId] in homeStartList:
				startId = random.randrange(0, homePlayerNum)
			homeStartList.append(homePlayerList[startId])
			startFileHandler.write('INSERT INTO startsIn VALUES (%s, %s);\n' % (homePlayerList[startId], mid))
		awayStartList = []
		for i in range(5):
			startId = random.randrange(0, awayPlayerNum)
			while  awayPlayerList[startId] in awayStartList:
				startId = random.randrange(0, awayPlayerNum)
			#awayStartList.append(startId)
			awayStartList.append(awayPlayerList[startId])
			startFileHandler.write('INSERT INTO startsIn VALUES (%s, %s);\n' % (awayPlayerList[startId], mid))

		# add active players
		homePerformPlayerList = homeStartList
		for i in range(3):
			newPid = random.randrange(0, homePlayerNum)
			while homePlayerList[newPid] in homePerformPlayerList:
				newPid = random.randrange(0, homePlayerNum)
			#homePlayerList.append(newPid)
			homePerformPlayerList.append(homePlayerList[newPid])


		awayPerformPlayerList = awayStartList
		for i in range(3):
			newPid = random.randrange(0, awayPlayerNum)
			while awayPlayerList[newPid] in awayPerformPlayerList:
				newPid = random.randrange(0, awayPlayerNum)
			awayPerformPlayerList.append(awayPlayerList[newPid])

		# add foul and performance of home players
		for i in range(8):
			foulNum = random.randrange(0, 4)
			for j in range(foulNum):
				#INSERT INTO foul VALUES (1, 2, 1);
				foulFileHandler.write('INSERT INTO foul VALUES (%s, %s, %s);\n' % (currentFoulId + j, \
					homePerformPlayerList[i], mid))
			currentFoulId += foulNum

			backboard = random.randrange(0, 10)
			assist = random.randrange(0, 8)
			steals = random.randrange(0, 10)
			penalty = random.randrange(0, 5)
			twopoint = random.randrange(0,8)
			threepoint = random.randrange(0,5)
			totalScore = 1*penalty + 2*twopoint + 3*threepoint
			fieldPerc = random.randrange(30, 90)
			performHandler.write('INSERT INTO performedIn VALUES (%s, %s, %s, %s,%s,%s,%s,%s,%s, %s);\n' % \
				(homePerformPlayerList[i], mid, totalScore, backboard, assist, steals, penalty, twopoint, threepoint, fieldPerc))


		# add foul and performance of away players
		for i in range(8):
			foulNum = random.randrange(0, 4)
			for j in range(foulNum):
				#INSERT INTO foul VALUES (1, 2, 1);
				foulFileHandler.write('INSERT INTO foul VALUES (%s, %s, %s);\n' % (currentFoulId + j, \
					awayPerformPlayerList[i], mid))
			currentFoulId += foulNum

			backboard = random.randrange(0, 10)
			assist = random.randrange(0, 8)
			steals = random.randrange(0, 10)
			penalty = random.randrange(0, 5)
			twopoint = random.randrange(0,8)
			threepoint = random.randrange(0,5)
			totalScore = 1*penalty + 2*twopoint + 3*threepoint
			fieldPerc = random.randrange(30, 90)
			performHandler.write('INSERT INTO performedIn VALUES (%s, %s, %s, %s,%s,%s,%s,%s,%s, %s);\n' % \
				(awayPerformPlayerList[i], mid, totalScore, backboard, assist, steals, penalty, twopoint, threepoint, fieldPerc))

	startFileHandler.close()
	foulFileHandler.close()
	performHandler.close()



insertPerformedin()










#insertPerformedin()








