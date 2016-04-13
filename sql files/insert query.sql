CREATE TABLE club (
clid INTEGER NOT NULL,
clowner varchar(20) NOT NULL,
clname varchar(30) NOT NULL,
clzone varchar(20) NOT NULL,
PRIMARY KEY (clid),
CHECK (clzone = 'west' OR clzone = 'east' )
);

INSERT INTO club VALUES(1 ,'Jeanie Buss','Los Angeles Lakers', 'west');
INSERT INTO club VALUES(2 ,'Peter Guber','Golden State Warriors', 'west');
INSERT INTO club VALUES(3 ,'Leslie Alexander','Houston Rockets', 'west');
INSERT INTO club VALUES(4 ,'Mark Cuban','Dallas Mavericks', 'west');
INSERT INTO club VALUES(5 ,'Richard DeVos','Orlando Magic', 'east');
INSERT INTO club VALUES(6 ,'Larry Tanenbaum','Toronto Raptors', 'east');



	
	


CREATE TABLE match (
mid INTEGER NOT NULL, 
mwinner VARCHAR(30) NOT NULL,
mtime DATE NOT NULL,
mtype VARCHAR(10) NOT NULL,
PRIMARY KEY (mid),
CHECK (mtype = 'regular' OR mtype = 'playoff') 
);

INSERT INTO match VALUES(1 ,'Los Angeles Lakers','2016-03-07', 'regular');
INSERT INTO match VALUES(2 ,'Houston Rockets','2016-01-18', 'regular');
INSERT INTO match VALUES(3 ,'Dallas Mavericks','2016-01-27', 'regular');
INSERT INTO match VALUES(4 ,'Toronto Raptors','2015-12-08', 'regular');
INSERT INTO match VALUES(5 ,'Orlando Magic','2015-11-12', 'regular');




CREATE TABLE competition(
cpyear INTEGER NOT NULL,
cpchampion VARCHAR(30) NOT NULL,
PRIMARY KEY(cpyear)
);

INSERT INTO competition VALUES(2015, 'Golden State Warriors');
INSERT INTO competition VALUES(2014, 'San Antonio Spurs');
INSERT INTO competition VALUES(2013, 'Miami Heat');
INSERT INTO competition VALUES(2012, 'Miami Heat');
INSERT INTO competition VALUES(2011, 'Dallas Mavericks');
INSERT INTO competition VALUES(2010, 'Los Angeles Lakers');
INSERT INTO competition VALUES(2009, 'Los Angeles Lakers');
INSERT INTO competition VALUES(2008, 'Boston Celtics');
INSERT INTO competition VALUES(2007, 'San Antonio Spurs');
INSERT INTO competition VALUES(2006, 'Miami Heat');
INSERT INTO competition VALUES(2005, 'San Antonio Spurs');




CREATE TABLE player(
pid INTEGER NOT NULL,
pname VARCHAR(30) NOT NULL,
pnationality VARCHAR(20) NOT NULL,
pdob DATE NOT NULL,
pposition VARCHAR(5) NOT NULL,
PRIMARY KEY(pid),
CHECK (pposition = 'PG' OR pposition = 'SG' OR pposition = 'SF' OR pposition = 'PF' OR pposition = 'C' )
);

INSERT INTO PLAYER VALUES (1, 'Kobe Bryant', 'USA', '1978-8-23','SG');
INSERT INTO PLAYER VALUES (2, 'Anthony Brown', 'USA', '1992-10-10','SF');
INSERT INTO PLAYER VALUES (3, 'Louis Williams', 'USA', '1986-10-27','SF');
INSERT INTO PLAYER VALUES (4, 'Stephen Curry', 'USA', '1988-3-14','SF');
INSERT INTO PLAYER VALUES (5, 'Draymond Green', 'USA', '1990-3-4','SF');
INSERT INTO PLAYER VALUES (6, 'Andrew Bogut', 'USA', '1984-11-28','C');
INSERT INTO PLAYER VALUES (7, 'Josh Smith', 'USA', '1985-12-5','SF');
INSERT INTO PLAYER VALUES (8, 'Dwight Howard', 'USA', '1985-12-8','C');
INSERT INTO PLAYER VALUES (9, 'James Harden', 'USA', '1989-8-26','SG');
INSERT INTO PLAYER VALUES (10, 'David Lee', 'USA', '1983-4-29','SF');
INSERT INTO PLAYER VALUES (11, 'Jose Juan Barea', 'USA', '1984-6-26','SG');
INSERT INTO PLAYER VALUES (12, 'Aaron Gordon', 'USA', '1995-9-16','SF');
INSERT INTO PLAYER VALUES (13, 'Dewayne Dedmon', 'USA', '1989-8-12','C');
INSERT INTO PLAYER VALUES (14, 'Jason Thompson', 'USA', '1986-7-21','SF');
INSERT INTO PLAYER VALUES (15, 'James Johnson', 'USA', '1987-2-20','SF');










CREATE TABLE foul(
fid INTEGER NOT NULL,
ftype VARCHAR(20) NOT NULL,
pid INTEGER NOT NULL REFERENCES player(pid),
mid INTEGER NOT NULL REFERENCES match(mid),
PRIMARY KEY(fid)
);


INSERT INTO foul VALUES (1, 'technical foul', 2, 1);
INSERT INTO foul VALUES (2, 'blocking', 1, 5);
INSERT INTO foul VALUES (3, 'charging', 3, 3);
INSERT INTO foul VALUES (4, 'defensive foul', 12, 1);
INSERT INTO foul VALUES (5, 'disqualifying foul', 10, 4);
INSERT INTO foul VALUES (6, 'double foul', 7, 2);
INSERT INTO foul VALUES (7, 'flagrant foul', 2, 4);
INSERT INTO foul VALUES (8, 'moving pick', 13, 3);
INSERT INTO foul VALUES (9, 'defensive foul', 3, 2);
INSERT INTO foul VALUES (10, 'flagrant foul', 11, 4);
INSERT INTO foul VALUES (11, 'technical foul', 15, 1);



CREATE TABLE referee(
rid INTEGER NOT NULL,
rname VARCHAR(20) NOT NULL,
rnationality VARCHAR(20) NOT NULL,
rdob DATE NOT NULL,
PRIMARY KEY(rid)
);

INSERT INTO referee VALUES (1, 'Derrick Collins', 'USA', '1965-7-15');
INSERT INTO referee VALUES (2, 'Greg Willard', 'USA', '1958-11-5');
INSERT INTO referee VALUES (3, 'Bennett Salvatore', 'USA', '1950-1-9');
INSERT INTO referee VALUES (4, 'Dan Crawford', 'USA', '1953-11-23');
INSERT INTO referee VALUES (5, 'David Guthrie', 'USA', '1974-5-21');
INSERT INTO referee VALUES (6, 'Ed Malloy', 'USA', '1971-3-17');
INSERT INTO referee VALUES (7, 'Eli Roe', 'USA', '1974-3-18');
INSERT INTO referee VALUES (8, 'Gary Zielinski', 'USA', '1965-8-31');
INSERT INTO referee VALUES (9, 'Joe DeRosa', 'USA', '1957-3-9');
INSERT INTO referee VALUES (10, 'Luis Grillo', 'USA', '1948-10-10');






CREATE TABLE coach(
coid INTEGER NOT NULL,
coname VARCHAR(20) NOT NULL,
cnationality VARCHAR(20) NOT NULL,
codob DATE NOT NULL,
PRIMARY KEY(coid)
);
INSERT INTO coach VALUES (1, 'Rick Carlisle', 'USA', '1959-10-27');
INSERT INTO coach VALUES (2, 'Byron Scott', 'USA', '1961-3-28');
INSERT INTO coach VALUES (3, 'Steve Kerr', 'USA', '1965-9-27');
INSERT INTO coach VALUES (4, 'J.B-Bigstuff', 'USA', '1979-3-10');
INSERT INTO coach VALUES (5, 'Jacque Vaughn', 'USA', '1975-2-11');
INSERT INTO coach VALUES (6, 'Dwane Casey', 'USA', '1957-4-17');









CREATE TABLE participatedInM(
clid INTEGER NOT NULL REFERENCES club(clid), 
mid INTEGER NOT NULL REFERENCES match(mid), 
ptype VARCHAR(10) NOT NULL,
iswinner boolean NOT NULL,
totalScores INTEGER NOT NULL,
PRIMARY KEY(clid, mid),
CHECK (ptype = 'home' OR ptype = 'away')
);
INSERT INTO participatedInM VALUES (1, 1, 'home', TRUE, 112);
INSERT INTO participatedInM VALUES (2, 1,  'away', FALSE, 95);
INSERT INTO participatedInM VALUES (1, 2,  'home', FALSE, 95);
INSERT INTO participatedInM VALUES (3, 2,  'away', TRUE, 112);
INSERT INTO participatedInM VALUES (1, 3,  'home', FALSE, 90);
INSERT INTO participatedInM VALUES (4, 3,  'away', TRUE, 92);
INSERT INTO participatedInM VALUES (1, 4,  'home', FALSE, 93);
INSERT INTO participatedInM VALUES (6, 4,  'away', TRUE, 102);
INSERT INTO participatedInM VALUES (1, 5,  'home', FALSE, 99);
INSERT INTO participatedInM VALUES (5, 5,  'away', TRUE, 101);




CREATE TABLE participatedInC(
clid INTEGER NOT NULL REFERENCES club(clid),
cpyear INTEGER NOT NULL REFERENCES competition(cpyear),
PRIMARY KEY(clid, cpyear)
);
INSERT INTO participatedInC VALUES (1, 2016);
INSERT INTO participatedInC VALUES (2, 2016);
INSERT INTO participatedInC VALUES (3, 2016);
INSERT INTO participatedInC VALUES (4, 2016);
INSERT INTO participatedInC VALUES (5, 2016);
INSERT INTO participatedInC VALUES (6, 2016);


CREATE TABLE performedIn(
pid INTEGER NOT NULL REFERENCES player(pid),
mid INTEGER NOT NULL REFERENCES match(mid),
totalScores INTEGER NOT NULL,
backboard INTEGER NOT NULL,
assist INTEGER NOT NULL,
steals INTEGER NOT NULL,
penaltyShoot INTEGER NOT NULL, 
twoPointShoot INTEGER NOT NULL,
threePointShoot INTEGER NOT NULL,
fieldGoalPercentage INTEGER NOT NULL,
PRIMARY KEY(pid, mid)
);
INSERT INTO performedIn VALUES (1, 1, 18, 5,3,4,7,6,2, 80);
INSERT INTO performedIn VALUES (8, 2, 32, 4,7,9,7,10,4, 76);
INSERT INTO performedIn VALUES (2, 1, 16, 3,4,5,3,5,2, 82);
INSERT INTO performedIn VALUES (9, 2, 10, 2,3,1,7,2,2, 50);
INSERT INTO performedIn VALUES (3, 1, 12, 5,3,6,2,3,2, 73);
INSERT INTO performedIn VALUES (10, 2, 13, 2,0,0,3,5,1, 70);
INSERT INTO performedIn VALUES (4, 5, 18, 6,9,3,2,3,4, 66);
INSERT INTO performedIn VALUES (11, 3, 23, 1,1,2,5,7,3, 79);
INSERT INTO performedIn VALUES (5, 4, 17, 8,10,3,2,7,1, 83);
INSERT INTO performedIn VALUES (12, 2, 33, 8,10,5,9,12,3, 79);
INSERT INTO performedIn VALUES (6, 3, 18, 5,4,7,8,6,2, 70);
INSERT INTO performedIn VALUES (7, 2, 21, 7,5,4,7,9,1, 87);
INSERT INTO performedIn VALUES (13, 3, 30, 4,6,2,7,0,10, 67);
INSERT INTO performedIn VALUES (14, 1, 13, 7,4,5,4,5,1, 65);
INSERT INTO performedIn VALUES (15, 2, 16, 4,7,8,5,5,2, 72);





CREATE TABLE refereeIn(
rid INTEGER NOT NULL REFERENCES referee(rid),
mid INTEGER NOT NULL REFERENCES match(mid),
PRIMARY KEY(rid, mid)
);
INSERT INTO refereeIn VALUES (3, 1);
INSERT INTO refereeIn VALUES (4, 2);
INSERT INTO refereeIn VALUES (9, 3);
INSERT INTO refereeIn VALUES (1, 4);
INSERT INTO refereeIn VALUES (7, 5);



CREATE TABLE matchIn(
mid INTEGER NOT NULL REFERENCES match(mid),
cpyear INTEGER NOT NULL REFERENCES competition(cpyear),
PRIMARY KEY(mid, cpyear)
);
INSERT INTO matchIn VALUES (1, 2016);
INSERT INTO matchIn VALUES (2, 2016);
INSERT INTO matchIn VALUES (3, 2016);
INSERT INTO matchIn VALUES (4, 2016);
INSERT INTO matchIn VALUES (5, 2016);



CREATE TABLE playsIn(
pid INTEGER NOT NULL REFERENCES player(pid), 
clid INTEGER NOT NULL REFERENCES club(clid),
salary INTEGER NOT NULL, 
contractStartYear INTEGER NOT NULL,
contractEndYear INTEGER NOT NULL,
PRIMARY KEY(pid, clid, contractStartYear, contractEndYear)
);


INSERT INTO playsIn VALUES (1, 1, 25000000, 2015, 2016);
INSERT INTO playsIn VALUES (2, 1, 700000, 2015, 2016);
INSERT INTO playsIn VALUES (3, 1, 500000, 2015, 2016);
INSERT INTO playsIn VALUES (4, 2, 11370786, 2015, 2016);
INSERT INTO playsIn VALUES (5, 2, 14300000, 2015, 2016);
INSERT INTO playsIn VALUES (6, 2, 12000000, 2014, 2016);
INSERT INTO playsIn VALUES (7, 3, 5400000, 2015, 2016);
INSERT INTO playsIn VALUES (8, 3, 22359364, 2013, 2016);
INSERT INTO playsIn VALUES (9, 3, 15756438, 2015, 2016);
INSERT INTO playsIn VALUES (10, 4, 15493680, 2015, 2016);
INSERT INTO playsIn VALUES (11, 4, 1490670, 2015, 2016);
INSERT INTO playsIn VALUES (12, 5, 4171680, 2014, 2016);
INSERT INTO playsIn VALUES (13, 5, 947278, 2014, 2016);

INSERT INTO playsIn VALUES (15, 6, 2500000, 2015, 2016);



CREATE TABLE startsIn(
pid INTEGER NOT NULL REFERENCES player(pid),
mid INTEGER NOT NULL REFERENCES match(mid),
PRIMARY KEY(pid, mid)
);
INSERT INTO startsIn VALUES (1, 1);
INSERT INTO startsIn VALUES (1, 2);
INSERT INTO startsIn VALUES (1, 3);
INSERT INTO startsIn VALUES (1, 4);
INSERT INTO startsIn VALUES (1, 5);
INSERT INTO startsIn VALUES (1, 6);


CREATE TABLE coachIn(
coid INTEGER NOT NULL REFERENCES coach(coid),
clid INTEGER NOT NULL REFERENCES club(clid),
startYear INTEGER NOT NULL,
endYear INTEGER NOT NULL,
PRIMARY KEY(coid, clid, startYear, endYear)
);


INSERT INTO coachin VALUES (1, 4, 2015, 2016);
INSERT INTO coachin VALUES (2, 1, 2015, 2016);
INSERT INTO coachin VALUES (3, 2, 2015, 2016);
INSERT INTO coachin VALUES (4, 3, 2015, 2016);
INSERT INTO coachin VALUES (5, 5, 2015, 2016);
INSERT INTO coachin VALUES (6, 6, 2015, 2016);



SELECT CL.clname, AVG(T.AGE), AVG(T.totalScores), AVG(T.salary),
       AVG( SELECT T.AGE
            FROM T
            WHERE T.AGE < AVG(T.AGE) AND T.totalScores >= AVG(T.totalScores)) AS RS_AVG_AGE,
       AVG( SELECT T.totalScores
            FROM T
            WHERE T.AGE < AVG(T.AGE) AND T.totalScores >= AVG(T.totalScores)) AS RS_AVG_totalScores,
       AVG( SELECT T.salary
            FROM T
            WHERE T.AGE < AVG(T.AGE) AND T.totalScores >= AVG(T.totalScores)) AS RS_AVG_salary
FROM club CL, (SELECT PI.salary, PI.pid, ("2016-03-07"-P.pdob) AS AGE, Per.totalScores
               FROM playsIn PI, player P, performedIn Per
               WHERE PI.clid = CL.clid AND PI.pid = P.pid AND Per.pid = P.pid) T
WHERE (SELECT count(SELECT M.mid
                    FROM match M, participatedInM PM
                    WHERE PM.clid = CL.clid AND M.mid = PM.mid AND M.mwinner = CL.clname)) >
      (SELECT AVG(SELECT count(SELECT M.mid
                               FROM match M, participatedInM PM
                               WHERE M.mid = PM.mid AND PM.clid = C.clid AND M.mwinner  = C.clname)
                  FROM club C))
GROUP BY CL.clname;





SELECT C.clname, M.mid, M.mwinner, M.mtime, M.mtype
FROM participatedInM PM, match M, club C
WHERE PM.mid = M.mid AND PM.clid = C.clid AND PM.ptype = 'away' AND PM.totalScores >= 110 AND
      PM.isWinner = TRUE AND
      (SELECT PIM.totalScores
       FROM participatedInM PIM, club C1
       WHERE PIM.mid = M.mid AND PIM.clid = C1.clid AND PM.ptype = 'home') >= 110 AND
       (PM.totalScores-(SELECT PIM.totalScores
                        FROM participatedInM PIM, club C1
                        WHERE PIM.mid = M.mid AND PIM.clid = C1.clid AND PM.ptype = 'home')) <= 10
GROUP BY M.mid;




select 
from 