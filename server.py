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


#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@w4111a.eastus.cloudapp.azure.com/proj1part2
#
# For example, if you had username gravano and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://gravano:foobar@w4111a.eastus.cloudapp.azure.com/proj1part2"
#
#DATABASEURI = "postgresql://user:password@w4111a.eastus.cloudapp.azure.com/proj1part2"

DATABASEURI = "postgresql://yc3121:2196@w4111vm.eastus.cloudapp.azure.com/w4111"

#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#
# engine.execute("""CREATE TABLE IF NOT EXISTS test (
#   id serial,
#   name text
# );""")
#engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")


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


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """

  # DEBUG: this is debugging code to see what request looks like
  print request.args


  #
  # example of a database query
  #
  cursor = g.conn.execute("SELECT name FROM test")
  names = []
  for result in cursor:
    names.append(result['name'])  # can also be accessed using result[0]
  cursor.close()

  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be 
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #     
  #     # creates a <div> tag for each element in data
  #     # will print: 
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
  context = dict(data = names)


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  return render_template("index.html", **context)

#
# This is an example of a different path.  You can see it at:
# 
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#
@app.route('/another')
def another():
  print 'render another.html'
  return render_template("another.html")


# Example of adding new data to the database
# @app.route('/add', methods=['POST'])
# def add():
#   print request.form
#   #fetchedName = request.form['name']
#   #print 'fetched name = ' 
#   #print fetchedName
#   tmpQuery = 'INSERT INTO test(name) VALUES (\'%s\')' % fetchedName
#   print tmpQuery
#   #g.conn.execute("""INSERT INTO test VALUES (20, 'helo')""")
#   g.conn.execute(tmpQuery)
#   return redirect('/')

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
  if request.form.has_key('cbpname'):
    selectClauseList.append('player2.pname')
    # if not 'player2' in secFromList:
    #   secFromList.append('player2')
  
  if request.form.has_key('cbpnationality'):
    selectClauseList.append('player2.pnationality')
    # if not 'player2' in secFromList:
    #   secFromList.append('player2')

  if request.form.has_key('cbpage'):
    selectClauseList.append('player2.pdob')
    # if not 'player2' in secFromList:
    #   secFromList.append('player2')
  
  if request.form.has_key('cbpposition'):
    selectClauseList.append('player2.pposition')
    # if not 'player2' in secFromList:
    #   secFromList.append('player2')

  if request.form.has_key('cbclname'):
    #selectClauseList.append('club2.clname')
    selectClauseList.append('(select club2.clname from club club2, playsin playsin2 where playsin2.pid = player2.pid AND\
      playsin2.clid = club2.clid) AS clname' )
    # if not 'club2' in secFromList:
    #   secFromList.append('club2')
    # if not 'playsin2' in secFromList:
    #   secFromList.append('playsin2')
    #secWhereClauseList.append('club2.clid = playsin2.clid AND playsin2.pid = player2.pid')
  
  if request.form.has_key('cbclowner'):
    #selectClauseList.append('club2.clowner')
    selectClauseList.append('(select club2.clowner from club club2, playsin playsin2 where playsin2.pid = player2.pid AND\
      playsin2.clid = club2.clid) AS clowner' )
    #secWhereClauseList.append('club2.clid = playsin2.clid AND playsin2.pid = player2.pid')

  if request.form.has_key('cbclzone'):
    #selectClauseList.append('club2.clzone')
    selectClauseList.append('(select club2.clzone from club club2, playsin playsin2 where playsin2.pid = player2.pid AND\
      playsin2.clid = club2.clid) AS clzone' )
    #secWhereClauseList.append('club2.clid = playsin2.clid AND playsin2.pid = player2.pid')

  if request.form.has_key('cbmatchnum'):
    #selectClauseList.append('count(performedin2.mid)')
    selectClauseList.append('(select count(distinct(mid)) from performedin performedin2 where performedin2.pid = player2.pid) AS matchNum')
    #secWhereClauseList.append('performedin2.pid = player2.pid')

  # if request.form.has_key('cbconame'):
  #   #selectClauseList.append('coach2.coname')
  #   selectClauseList.append('(select coach2.coname from coach coach2, coachin coachin2, club club2 where player2.pid = )')
  #   secWhereClauseList.append('club2.clid = playsin2.clid AND playsin2.pid = player2.pid AND coach2.coid = coachin2.coid\
  #     AND coachin2.clid = club2.clid')

  if request.form.has_key('cbfoulnum'):
    #selectClauseList.append('count(foul2.fid)')
    selectClauseList.append('(select count(distinct(foul2.fid)) from foul foul2 where foul2.pid = player2.pid) AS foulnum')
    #secWhereClauseList.append('foul2.pid = player2.pid')

  if request.form.has_key('cbstartnum'):
    #selectClauseList.append('count(startsin2.pid)')
    selectClauseList.append('(select count(distinct(startsin2.mid)) from startsin startsin2 where startsin2.pid = player2.pid ) AS partInNum')
    #secWhereClauseList.append('startsin2.pid = player2.pid')

  if request.form.has_key('cbsalary'):
    #selectClauseList.append('playsin2.salary')
    selectClauseList.append('(select playsin2.salary from playsin playsin2 where playsin2.pid = player2.pid) AS salary')
    #secWhereClauseList.append('playsin2.pid = player2.pid')


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



  




  # print 'fetched name = ' 
  # print fetchedName
  # tmpQuery = 'INSERT INTO test(name) VALUES (\'%s\')' % fetchedName
  # print tmpQuery
  cursor = g.conn.execute(totalClause)

  names = []
  for result in cursor:
    names.append(result['name'])  # can also be accessed using result[0]
  cursor.close()

  context = dict(data = names)

  return render_template("search_result.html", **context)

  #return redirect('/')



@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()


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
