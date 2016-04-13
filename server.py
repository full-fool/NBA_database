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
    selectClause = 'select distinct * '
  else:
    selectClause = 'select distinct ' + ' , '.join(selectClauseList) + ' '

  # from clause
  #fromClause = 'from player player2, club club2, playsin playsin2, coach coach2, coachin coachin2'
  fromClause = 'from player player2'
  #fromClause = 'from player player2, club club2, playsin playsin2, coach'

  secWhereClause = ''
  if len(secWhereClauseList) == 0:
    secWhereClause = 'player2.pid in %s' % firstStepClause + ';'
  else:
    secWhereClause = ' AND '.join(secWhereClauseList) + ' AND player2.pid in %s' % firstStepClause + ';'
  totalClause = selectClause +'\n'  + fromClause + '\n where ' + secWhereClause
  #print secWhereClauseList
  print 'totalClause'
  print totalClause


  cursor = g.conn.execute(totalClause)

  names = []
  for result in cursor:
    names.append(result)  # can also be accessed using result[0]
  cursor.close()
  print len(selectAttriList)
  print selectAttriList

  context = dict(klen=len(selectAttriList), keys = selectAttriList, data = names, recordnum=len(names))
  #context = dict(data = names)
  #print context
  return render_template("search_result.html", **context)
  #return render_template("search_result.html")


  #return redirect('/')


# @app.route('search_club', methods=['POST'])
# def search_club():






if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='127.0.0.1')
  @click.argument('PORT', default=8100, type=int)
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
