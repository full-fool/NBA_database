#!/usr/bin/env python2.7

"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver

To run locally:

    python server.py

Go to http://localhost:8111 in your browser.

A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response
import datetime
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


DATABASEURI = "postgresql://yc3121:2196@w4111vm.eastus.cloudapp.azure.com/w4111"


engine = create_engine(DATABASEURI)


@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass

@app.route('/')
def index():
  return render_template('index.html')

  # # DEBUG: this is debugging code to see what request looks like
  # print request.args

  # cursor = g.conn.execute("SELECT name FROM test")
  # names = []
  # for result in cursor:
  #   names.append(result['name'])  # can also be accessed using result[0]
  # cursor.close()


  # context = dict(data = names)


  # #
  # # render_template looks in the templates/ folder for files.
  # # for example, the below file reads template/index.html
  # #
  # return render_template("index.html", **context)

@app.route('/index.html')
def gotoindex():
  return render_template('index.html')

@app.route('/another')
def another():
  print 'render another.html'
  return render_template("another.html")



@app.route('/search_player', methods=['POST'])
def search_player():
  # first step: select all pid
  # where clause
  #print 'in search_player'
  whereClause = ''
  whereClauseList = []
  fPname = request.form['pname']
  if fPname != '':
    whereClauseList.append('player.pname = \'%s\'' % fPname)
  
  fPnationality = request.form['pnationality']
  if fPnationality != '':
    whereClauseList.append('player.pnationality = \'%s\'' % fPnationality)
  
  fPage = request.form['page']
  if fPage != '':
    nowTime = datetime.datetime.now()
    #currentDate = '%s-%s-%s' % (nowTime.year, nowTime.month, nowTime.day)
    nowYear = nowTime.year
    birthYear = nowYear - int(fPage)
    whereClauseList.append('player.pdob >= \'%s-1-1\' AND player.pdob <= \'%s-12-31\'' % (birthYear, birthYear))
  
  fPposition = request.form['pposition']
  if fPposition != '':
    whereClauseList.append('player.pposition = \'%s\'' % fPposition)

  fClname = request.form['clname']
  if fClname != '':
    whereClauseList.append('club.clname = \'%s\' AND club.clid = playsin.clid AND player.pid = playsin.pid' % fClname)

  # to be finished
  fMatchNum = request.form['matchnum']
  if fMatchNum != '':
    whereClauseList.append('(select count(*) from performedin where performedin.pid = player.pid) = %s' % fMatchNum)
  
  fFoulNum = request.form['foulnum']
  if fFoulNum != '':
    whereClauseList.append('(select count(*) from foul where foul.pid = player.pid) = %s' % fFoulNum)

  fStartNum = request.form['startnum']
  if fStartNum != '':
    whereClauseList.append('(select count(*) from startsin where startsin.pid = player.pid) = %s' % fStartNum)

  firstStepClause = ''
  if len(whereClauseList) == 0:
    firstStepClause = '(select pid from player)'
  else:
    firstStepClause = '(select distinct(player.pid) from player, club,  playsin where ' + ' AND '.join(whereClauseList) + ')'

  #print 'first firstStepClause'
  #print firstStepClause
  # second step
  # select clause
  selectClause = ''
  secWhereClauseList = []
  secFromList = []
  selectClauseList = []
  selectAttriList = []
  if request.form.has_key('cbpname'):
    selectClauseList.append('player2.pname')
    selectAttriList.append('pname')
    # if not 'player2' in secFromList:
    #   secFromList.append('player2')
  
  if request.form.has_key('cbpnationality'):
    selectClauseList.append('player2.pnationality')
    selectAttriList.append('pnationality')

    # if not 'player2' in secFromList:
    #   secFromList.append('player2')

  if request.form.has_key('cbpage'):
    selectClauseList.append('player2.pdob')
    selectAttriList.append('data of birth')

    # if not 'player2' in secFromList:
    #   secFromList.append('player2')
  
  if request.form.has_key('cbpposition'):
    selectClauseList.append('player2.pposition')
    selectAttriList.append('position')

    # if not 'player2' in secFromList:
    #   secFromList.append('player2')

  if request.form.has_key('cbclname'):
    #selectClauseList.append('club2.clname')
    selectClauseList.append('(select club2.clname from club club2, playsin playsin2 where playsin2.pid = player2.pid AND\
      playsin2.clid = club2.clid) AS clname' )
    selectAttriList.append('club name')

    # if not 'club2' in secFromList:
    #   secFromList.append('club2')
    # if not 'playsin2' in secFromList:
    #   secFromList.append('playsin2')
    #secWhereClauseList.append('club2.clid = playsin2.clid AND playsin2.pid = player2.pid')
  
  if request.form.has_key('cbclowner'):
    #selectClauseList.append('club2.clowner')
    selectClauseList.append('(select club2.clowner from club club2, playsin playsin2 where playsin2.pid = player2.pid AND\
      playsin2.clid = club2.clid) AS clowner' )
    selectAttriList.append('club owner')

    #secWhereClauseList.append('club2.clid = playsin2.clid AND playsin2.pid = player2.pid')

  if request.form.has_key('cbclzone'):
    #selectClauseList.append('club2.clzone')
    selectClauseList.append('(select club2.clzone from club club2, playsin playsin2 where playsin2.pid = player2.pid AND\
      playsin2.clid = club2.clid) AS clzone' )
    selectAttriList.append('club zone')

    #secWhereClauseList.append('club2.clid = playsin2.clid AND playsin2.pid = player2.pid')

  if request.form.has_key('cbmatchnum'):
    #selectClauseList.append('count(performedin2.mid)')
    selectClauseList.append('(select count(distinct(mid)) from performedin performedin2 where performedin2.pid = player2.pid) AS matchNum')
    #secWhereClauseList.append('performedin2.pid = player2.pid')
    selectAttriList.append('participated match times')

  # if request.form.has_key('cbconame'):
  #   #selectClauseList.append('coach2.coname')
  #   selectClauseList.append('(select coach2.coname from coach coach2, coachin coachin2, club club2 where player2.pid = )')
  #   secWhereClauseList.append('club2.clid = playsin2.clid AND playsin2.pid = player2.pid AND coach2.coid = coachin2.coid\
  #     AND coachin2.clid = club2.clid')

  if request.form.has_key('cbfoulnum'):
    #selectClauseList.append('count(foul2.fid)')
    selectClauseList.append('(select count(distinct(foul2.fid)) from foul foul2 where foul2.pid = player2.pid) AS foulnum')
    #secWhereClauseList.append('foul2.pid = player2.pid')
    selectAttriList.append('foul times')

  if request.form.has_key('cbstartnum'):
    #selectClauseList.append('count(startsin2.pid)')
    selectClauseList.append('(select count(distinct(startsin2.mid)) from startsin startsin2 where startsin2.pid = player2.pid ) AS partInNum')
    #secWhereClauseList.append('startsin2.pid = player2.pid')
    selectAttriList.append('starts in times')

  if request.form.has_key('cbsalary'):
    #selectClauseList.append('playsin2.salary')
    selectClauseList.append('(select playsin2.salary from playsin playsin2 where playsin2.pid = player2.pid) AS salary')
    #secWhereClauseList.append('playsin2.pid = player2.pid')
    selectAttriList.append('salary')


  if len(selectClauseList) == 0:
    context = dict(klen=0,  keys = [], data = [], recordnum=0)
    return render_template("search_result.html", **context)



    #selectClause = 'select distinct * '
  else:
    selectClause = 'select distinct ' + ' , '.join(selectClauseList) + ' '

  # from clause
  #fromClause = 'from player player2, club club2, playsin playsin2, coach coach2, coachin coachin2'
  fromClause = ' from player player2'
  #fromClause = 'from player player2, club club2, playsin playsin2, coach'

  secWhereClause = ''
  if len(secWhereClauseList) == 0:
    secWhereClause = 'player2.pid in %s' % firstStepClause + ';'
  else:
    secWhereClause = ' AND '.join(secWhereClauseList) + ' AND player2.pid in %s' % firstStepClause + ';'
  totalClause = selectClause  + fromClause + ' where ' + secWhereClause
  #print secWhereClauseList
  print 'totalClause'
  print totalClause


  cursor = g.conn.execute(totalClause)

  names = []
  rowNum = 0
  for result in cursor:
    names.append(result)  # can also be accessed using result[0]
    rowNum += 1
    #if rowNum >= 100:
    #  break
  cursor.close()
  print len(selectAttriList)
  print selectAttriList

  context = dict(klen=len(selectAttriList), keys = selectAttriList, data = names, recordnum=len(names))
  #context = dict(data = names)
  #print context
  return render_template("search_result.html", **context)
  #return render_template("search_result.html")


  #return redirect('/')


@app.route('/search_club', methods=['POST'])
def search_club():
  whereClause = ''
  whereClauseList = []
  firstFromList = ['club']
  fCowner = request.form['clowner']
  if fCowner != '':
    whereClauseList.append('club.clowner = \'%s\'' % fCowner)
  fCName = request.form['clname']
  if fCName != '':
    whereClauseList.append('club.clname = \'%s\'' % fCName)

  fCzone = request.form['clzone']
  if fCzone != '':
    whereClauseList.append('club.clzone = \'%s\'' % fCzone)

  fWintimes = request.form['clwinnum']
  if fWintimes != '':
    whereClauseList.append('(select count(*) from participatedinm where club.clid = participatedinm.clid AND \
      participatedinm.iswinner=True) = %s' % fWintimes)

  fLosetimes = request.form['clwinnum']
  if fLosetimes != '':
    whereClauseList.append('(select count(*) from participatedinm where participatedinm.clid = club.clid) - \
      (select count(*) from participatedinm where club.clid = participatedinm.clid \
      AND participatedinm.iswinner=True) = %s' % fLosetimes )

  fConame = request.form['coname']
  if fConame != '':
    whereClauseList.append('club.clid = coachin.clid AND coach.coid = coachin.coid AND coach.coname = \'%s\'' % fConame)
    firstFromList.append('coach')
    firstFromList.append('coachin')

  fPname = request.form['pname']
  if fPname != '':
    whereClauseList.append('club.clid = playsin.clid AND playsin.pid = player.pid AND player.pname = \'%s\'' % fPname)
    firstFromList.append('playsin')
    firstFromList.append('player')
  # fTotalScore = request.form['fTotalScore']
  # if fTotalScore != '':
  #   whereClauseList.append('')

  fChampTime = request.form['clchampionnum']
  if fChampTime != '':
    whereClauseList.append('(select count(*) from competition where competition.cpchampion = club.clname) = %s' % fChampTime)


  firstStepClause = ''
  if len(whereClauseList) == 0:
    firstStepClause = '(select clid from club)'
  else:
    firstStepClause = '(select distinct(club.clid) from ' + ' , '.join(firstFromList) + '  where ' + \
      ' AND '.join(whereClauseList) + ')'
  #print firstStepClause


  # # second step
  # # select clause
  
  selectClause = ''
  secWhereClauseList = []
  secFromList = []
  selectClauseList = []
  selectAttriList = []
  if request.form.has_key('cbclname'):
    selectClauseList.append('club2.clname')
    selectAttriList.append('club name')
    # if not 'player2' in secFromList:
    #   secFromList.append('player2')
  
  if request.form.has_key('cbconame'):
    selectClauseList.append('(select coach2.coname from coach coach2, coachin coachin2 where \
      coach2.coid = coachin2.coid AND coachin2.clid = club2.clid) AS coname' )
    selectAttriList.append('club coach name')

    # if not 'player2' in secFromList:
    #   secFromList.append('player2')

  if request.form.has_key('cbcoage'):
    selectClauseList.append('(select coach2.codob from coach coach2, coachin coachin2 where\
      coach2.coid = coachin2.coid AND coachin2.clid = club2.clid) AS codob' )
    selectAttriList.append('data of birth')

    # if not 'player2' in secFromList:
    #   secFromList.append('player2')
  
  if request.form.has_key('cbconationality'):
    selectClauseList.append('(select coach2.cnationality from coach coach2, coachin coachin2 where\
      coach2.coid = coachin2.coid AND coachin2.clid = club2.clid) AS conationality')
    selectAttriList.append('coach nationality')

    # if not 'player2' in secFromList:
    #   secFromList.append('player2')

  if request.form.has_key('cbclonwer'):
    selectClauseList.append('club2.clowner' )
    selectAttriList.append('club owner')

  if request.form.has_key('cbclzone'):
    selectClauseList.append('club2.clzone')
    selectAttriList.append('club zone')


  if request.form.has_key('cbclwinnum'):
    selectClauseList.append('(select count(mid) from participatedinm participatedinm2 where\
      participatedinm2.clid = club2.clid AND participatedinm2.iswinner = True) AS wintimes')
    selectAttriList.append('win times')

  
  if request.form.has_key('cbclchampionnum'):
    #selectClauseList.append('club2.clowner')
    selectClauseList.append('(select count(competition2.cpyear) from competition competition2 where\
      competition2.cpchampion = club2.clname) AS championnum' )
    selectAttriList.append('champion times')



  if len(selectClauseList) == 0:
    context = dict(klen=0,  keys = [], data = [], recordnum=0)
    return render_template("search_result.html", **context)


  else:
    selectClause = 'select distinct ' + ' , '.join(selectClauseList) + ' '

  # from clause
  #fromClause = 'from player player2, club club2, playsin playsin2, coach coach2, coachin coachin2'
  fromClause = 'from club club2'
  #fromClause = 'from player player2, club club2, playsin playsin2, coach'

  secWhereClause = ''
  if len(secWhereClauseList) == 0:
    secWhereClause = 'club2.clid in %s' % firstStepClause + ';'
  else:
    secWhereClause = ' AND '.join(secWhereClauseList) + ' AND club2.clid in %s' % firstStepClause + ';'
  totalClause = selectClause  + fromClause + ' where ' + secWhereClause
  #print secWhereClauseList
  print 'totalClause'
  print totalClause


  cursor = g.conn.execute(totalClause)

  names = []
  rowNum = 0
  for result in cursor:
    names.append(result)  # can also be accessed using result[0]
    rowNum += 1
    #if rowNum >= 100:
    #  break
  cursor.close()

  context = dict(klen=len(selectAttriList), keys = selectAttriList, data = names, recordnum=len(names))
  return render_template("search_result.html", **context)


@app.route('/search_match', methods=['POST'])
def search_match():
  whereClause = ''
  whereClauseList = []
  firstFromList = ['match']
  fMwinner = request.form['mwinner']
  if fMwinner != '':
    whereClauseList.append('match.mwinner = \'%s\'' % fMwinner)

  fMTime = request.form['mtime']
  if fMTime != '':
    whereClauseList.append('match.mtime = \'%s\'' % fMTime)

  fMType = request.form['mtype']
  if fMType != '':
    whereClauseList.append('match.mtype = \'%s\'' % fMType)

  fMHome = request.form['ptypehome']
  if fMHome != '':
    whereClauseList.append('participatedinm.ptype = \'home\' AND participatedinm.clid = club.clid AND club.clname = \'%s\' \
      AND participatedinm.mid = match.mid' % fMHome)
    firstFromList.append('club')
    firstFromList.append('participatedinm')

  fMAway = request.form['ptypeaway']
  if fMAway != '':
    whereClauseList.append('participatedinm3.ptype = \'away\' AND participatedinm3.clid = club3.clid AND club3.clname = \'%s\' \
      AND participatedinm3.mid = match.mid' % fMAway)
    if not 'club club3' in firstFromList:
      firstFromList.append('club club3')
    if not 'participatedinm participatedinm3' in firstFromList:
      firstFromList.append('participatedinm participatedinm3')
  

  fSDiff = request.form['scoredifference']
  if fSDiff != '':
    whereClauseList.append('participatedinm.ptype = \'away\' AND participatedinm.mid = match.mid AND\
      participatedinm3.ptype = \'home\' AND participatedinm3.mid = match.mid AND (participatedinm.totalscores - \
        participatedinm3.totalscores > %s OR participatedinm3.totalscores - participatedinm.totalscores > %s)' % (fSDiff, fSDiff))
    if not 'participatedinm' in firstFromList:
      firstFromList.append('participatedinm')
    if not 'participatedinm participatedinm3' in firstFromList:
      firstFromList.append('participatedinm participatedinm3')

  fRefereename = request.form['rname']
  if fRefereename != '':
    whereClauseList.append('refereein.rid = referee.rid AND refereein.mid = match.mid AND \
      referee.rname = \'%s\'' % fRefereename )
    firstFromList.append('referee')
    firstFromList.append('refereein')

  fPartPlayer = request.form['ppname']
  if fPartPlayer != '':
    whereClauseList.append('player.pid = performedin.pid AND performedin.mid = match.mid AND \
      player.pname= \'%s\'' % fPartPlayer)
    firstFromList.append('player')
    firstFromList.append('performedin')



  firstStepClause = ''
  if len(whereClauseList) == 0:
    firstStepClause = '(select mid from match)'
  else:
    firstStepClause = '(select distinct(match.mid) from ' + ' , '.join(firstFromList) + '  where ' + \
      ' AND '.join(whereClauseList) + ')'
  print firstStepClause


  # second step
  # select clause
  
  selectClause = ''
  secWhereClauseList = []
  secFromList = []
  selectClauseList = []
  selectAttriList = []
  if request.form.has_key('cbmwinner'):
    selectClauseList.append('match2.mwinner')
    selectAttriList.append('match winner')
    # if not 'player2' in secFromList:
    #   secFromList.append('player2')
  
  if request.form.has_key('cbmtime'):
    selectClauseList.append('match2.mtime' )
    selectAttriList.append('match time')

    # if not 'player2' in secFromList:
    #   secFromList.append('player2')

  if request.form.has_key('cbmtype'):
    selectClauseList.append('match2.mtype' )
    selectAttriList.append('match type')

    # if not 'player2' in secFromList:
    #   secFromList.append('player2')
  
  if request.form.has_key('cbptypehome'):
    selectClauseList.append('(select club.clname from club, participatedinm where club.clid = participatedinm.clid\
      AND participatedinm.mid = match2.mid AND participatedinm.ptype=\'home\' ) AS home_club')
    selectAttriList.append('home club')

    # if not 'player2' in secFromList:
    #   secFromList.append('player2')

  if request.form.has_key('cbptypeaway'):
    selectClauseList.append('(select club.clname from club, participatedinm where club.clid = participatedinm.clid\
      AND participatedinm.mid = match2.mid AND participatedinm.ptype = \'away\' ) AS away_club' )
    selectAttriList.append('away club')

  if request.form.has_key('cbscoredifference'):
    selectClauseList.append('(select participatedinm1.totalscores - participatedinm2.totalscores from\
      participatedinm participatedinm1, participatedinm participatedinm2 where participatedinm1.ptype = \'home\' \
      AND participatedinm2.ptype = \'away\' AND participatedinm1.mid = match2.mid AND participatedinm2.mid = match2.mid) AS score_difference' )
    selectAttriList.append('score difference')


  if request.form.has_key('cbrname'):
    selectClauseList.append('(select referee.rname from referee, refereein where referee.rid = refereein.rid AND \
      refereein.mid = match2.mid) AS rname' )
    selectAttriList.append('referee name')


  if request.form.has_key('cbrage'):
    selectClauseList.append('(select referee.rdob from referee, refereein where referee.rid = refereein.rid AND \
      refereein.mid = match2.mid) AS rdob')
    selectAttriList.append('referee date of birth')

  
  if request.form.has_key('cbrnationality'):
    #selectClauseList.append('club2.clowner')
    selectClauseList.append('(select referee.rnationality from referee, refereein where referee.rid = refereein.rid AND \
      refereein.mid = match2.mid) AS rnationality' )
    selectAttriList.append('referee nationality')

  if request.form.has_key('cbfoulnum'):
    selectClauseList.append('(select count(foul.fid) from foul where foul.mid = match2.mid) AS foul_num')
    selectAttriList.append('foul times')



  if len(selectClauseList) == 0:
    context = dict(klen=0,  keys = [], data = [], recordnum=0)
    return render_template("search_result.html", **context)

  else:
    selectClause = 'select distinct ' + ' , '.join(selectClauseList) + ' '

  # from clause
  #fromClause = 'from player player2, club club2, playsin playsin2, coach coach2, coachin coachin2'
  fromClause = ' from match match2'
  #fromClause = 'from player player2, club club2, playsin playsin2, coach'

  secWhereClause = ''
  if len(secWhereClauseList) == 0:
    secWhereClause = 'match2.mid in %s' % firstStepClause + ';'
  else:
    secWhereClause = ' AND '.join(secWhereClauseList) + ' AND match2.mid in %s' % firstStepClause + ';'
  totalClause = selectClause  + fromClause + ' where ' + secWhereClause
  #print secWhereClauseList
  print 'totalClause'
  print totalClause


  cursor = g.conn.execute(totalClause)

  names = []
  rowNum = 0
  for result in cursor:
    names.append(result)  # can also be accessed using result[0]
    rowNum +=1 
    #if rowNum >= 100:
    #  break
  cursor.close()
  #print 'search match rownum is %s' % rowNum

  context = dict(klen=len(selectAttriList), keys = selectAttriList, data = names, recordnum=len(names))
  return render_template("search_result.html", **context)

  #return render_template('index.html')

@app.route('/search_performance', methods=['POST'])
def search_performance():
  whereClause = ''
  whereClauseList = []
  #firstFromList = ['match']
  pname = request.form['pname']


  mtime = request.form['mtime']
  #04/06/2016
  month, day, year = mtime.split('/')[0], mtime.split('/')[1], mtime.split('/')[2]
  newMtime = '%s-%s-%s' % (year, month, day)

  query = 'select player.pname, performedin.totalscores, performedin.backboard, performedin.assist, \
  performedin.steals, performedin.penaltyshoot, performedin.twopointshoot, performedin.threepointshoot,\
  performedin.fieldgoalpercentage\
   from player, performedin, match where match.mtime = \'%s\' \
  AND match.mid = performedin.mid AND performedin.pid = player.pid AND \
  player.pname = \'%s\' ' % (newMtime, pname)

  print query
  cursor = g.conn.execute(query)

  names = []
  for result in cursor:
    names.append(result)  # can also be accessed using result[0]
  cursor.close()
  attriList = ['player name', 'total scores', 'backboard', 'assist', \
    'steals', 'penaltyshoot', 'twopointshoot', 'threepointshoot', 'fieldgoalpercentage']
  print 'performance result'
  print names
  context = dict(klen=9 , keys = attriList, data = names, recordnum=len(names))
  return render_template("search_result.html", **context)

@app.route('/special_request_1.html')
def specialRequest1():
  query = 'select player.pname, performedIn.totalScores, club.clname, playsIn.salary \
    from player, performedIn, club, playsIn \
    where performedIn.totalScores = (select max(PI.totalScores) from performedIn PI) AND performedIn.pid = player.pid \
    AND player.pid = performedIn.pid AND playsIn.pid = player.pid AND playsIn.clid = club.clid; '
  cursor = g.conn.execute(query)
  names = []
  for result in cursor:
    names.append(result)  # can also be accessed using result[0]
  cursor.close()
  selectAttriList = ['player name', 'total scores', 'club name', 'salary']
  context = dict(klen=4, keys = selectAttriList, data = names, recordnum=len(names))
  return render_template("search_result.html", **context)



@app.route('/special_request_2.html')
def specialRequest2():
  # query = 'SELECT C1.clname, C2.clname, M.mtime\
  #   FROM participatedInM PM1 join club C1 on PM1.clid = C1.clid, participatedInM PM2 JOIN club C2 on PM2.clid = C2.clid, \
  #   match M \
  #   where PM1.ptype = \'home\' AND PM2.ptype = \'away\' \
  #   AND PM2.iswinner = TRUE AND PM1.totalScores >= 95 AND PM2.totalScores >= 95 AND M.mid = PM1.mid \
  #   AND M.mid = PM2.mid AND PM2.totalScores - PM1.totalScores <= 5;'
  query = 'SELECT C1.clname, C2.clname, M.mtime \
    FROM participatedInM PM1 join club C1 on PM1.clid = C1.clid, participatedInM PM2 JOIN club C2 on PM2.clid = C2.clid, \
    match M \
    where PM1.ptype = \'home\' AND PM2.ptype = \'away\' \
    AND PM2.iswinner = TRUE AND PM1.totalScores >= 95 AND PM2.totalScores >= 95 AND M.mid = PM1.mid\
    AND M.mid = PM2.mid AND PM2.totalScores - PM1.totalScores <= 5;'
  
  cursor = g.conn.execute(query)
  names = []
  iterNum = 0
  for result in cursor:
    iterNum += 1
    names.append(result)  # can also be accessed using result[0]
    if iterNum >= 100:
      break
  cursor.close()
  selectAttriList = ['club1 name', 'club2 name', 'match date']
  context = dict(klen=3, keys = selectAttriList, data = names, recordnum=len(names))
  return render_template("search_result.html", **context)

@app.route('/special_request_3.html')
def specialRequest3():
  query = """

select CL4.clname, PLI2.pid, P4.pname as rising_star, PLI2.salary
from playsIn PLI2, player P4, club CL4,
    (SELECT CL.clid
         FROM club CL
         WHERE (SELECT count(TMP.mid)
                FROM (SELECT M.mid FROM match M, participatedInM PM
                      WHERE PM.clid = CL.clid AND M.mid = PM.mid AND M.mwinner = CL.clname) TMP) >=
               (select AVG(NW.win_num) as ave_win
               from (select C1.clname, count(*) AS win_num
                     from club C1, match M1
                     where C1.clname = M1.mwinner
                     group by C1.clname) NW) ) satisfiedClub,


      (select  P1.pid
      from 
      player P1, playsIn PS1,
      (select PI2.pid, AVG(PI2.totalScores) as pas
          from performedIn PI2, player PL2
          where PI2.pid = PL2.pid
          group by PI2.pid) PSC1,
        (select C1.clid, AVG(PSC.pas) as club_ave_score
        from 

        club C1, playsIn PSI,
          (select PI.pid, AVG(PI.totalScores) as pas
          from performedIn PI, player PL
          where PI.pid = PL.pid
          group by PI.pid) PSC

        where C1.clid = PSI.clid AND PSI.pid = PSC.pid
        group by C1.clid)  CAS
      where P1.pid = PS1.pid AND PS1.clid = CAS.clid AND P1.pid = PSC1.pid AND PSC1.pas > CAS.club_ave_score) satisfiedPlayer

where PLI2.pid = satisfiedPlayer.pid AND PLI2.clid = satisfiedClub.clid AND PLI2.pid = P4.pid AND CL4.clid = PLI2.clid;

  """
  cursor = g.conn.execute(query)
  names = []
  for result in cursor:
    names.append(result)  # can also be accessed using result[0]
  cursor.close()
  selectAttriList = ['club name', 'player id', 'playe name', 'salary']
  context = dict(klen=4, keys = selectAttriList, data = names, recordnum=len(names))
  return render_template("search_result.html", **context)




if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
