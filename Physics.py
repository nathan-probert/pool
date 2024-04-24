import os
import sqlite3
import time
import phylib;

import math

################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS;
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER;

HOLE_RADIUS = phylib.PHYLIB_HOLE_RADIUS
TABLE_LENGTH = phylib.PHYLIB_TABLE_LENGTH;
TABLE_WIDTH = phylib.PHYLIB_TABLE_WIDTH;

SIM_RATE = phylib.PHYLIB_SIM_RATE;
VEL_EPSILON = phylib.PHYLIB_VEL_EPSILON;

DRAG = phylib.PHYLIB_DRAG;
MAX_TIME = phylib.PHYLIB_MAX_TIME;

MAX_OBJECTS = phylib.PHYLIB_MAX_OBJECTS;

FRAME_INTERVAL = 0.01;

SCREEN_TABLE_WIDTH = 400
SCREEN_TABLE_HEIGHT = 785.71

# add more here

HEADER = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
                    "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg id="svgCon" class="svgCon" width="{SCREEN_TABLE_WIDTH}" height="{SCREEN_TABLE_HEIGHT}" viewBox="-25 -25 1400 2750";
    xmlns="http://www.w3.org/2000/svg"
    xmlns:xlink="http://www.w3.org/1999/xlink">""";

FOOTER = """</svg>\n""";

################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN 
    ];

def vectorLength( vel ):
    return math.sqrt(vel.x * vel.x + vel.y * vel.y);

################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass;


################################################################################
class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall;


    # add an svg method here
    def svg( self ):
        return """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (self.obj.still_ball.pos.x, self.obj.still_ball.pos.y, phylib.PHYLIB_BALL_RADIUS, BALL_COLOURS[self.obj.still_ball.number])


################################################################################
class RollingBall( phylib.phylib_object ):
    """
    Python RollingBall class.
    """

    def __init__( self, number, pos, vel, acc ):
        """
        Constructor function. Requires ball number, position (x,y), velocity (x,y), and accelleration (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_ROLLING_BALL, 
                                       number, 
                                       pos, vel, acc, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = RollingBall;


    # add an svg method here
    def svg( self ):
        return """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (self.obj.rolling_ball.pos.x, self.obj.rolling_ball.pos.y, phylib.PHYLIB_BALL_RADIUS, BALL_COLOURS[self.obj.rolling_ball.number])

################################################################################
class Hole( phylib.phylib_object ):
    """
    Python Hole class.
    """

    def __init__( self, pos  ):
        """
        Constructor function. Requires ball number, position (x,y), velocity (x,y), and accelleration (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HOLE, 
                                       None, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = Hole;


    # add an svg method here
    def svg( self ):
        return """ <circle cx="%d" cy="%d" r="%d" fill="black" />\n""" % (self.obj.hole.pos.x, self.obj.hole.pos.y, phylib.PHYLIB_HOLE_RADIUS)

################################################################################
class HCushion( phylib.phylib_object ):
    """
    Python RollingBall class.
    """

    def __init__( self, y ):
        """
        Constructor function. Requires ball number, position (x,y), velocity (x,y), and accelleration (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                    phylib.PHYLIB_HCUSHION, 
                                    None, 
                                    None, None, None, 
                                    None, y );
    
        # this converts the phylib_object into a StillBall class
        self.__class__ = HCushion;


    # add an svg method here
    def svg( self ):
        y = phylib.PHYLIB_TABLE_LENGTH
        if (self.obj.hcushion.y == 0.0):
            y = -25

        return """ <rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n""" % (y)

################################################################################
class VCushion( phylib.phylib_object ):
    """
    Python RollingBall class.
    """

    def __init__( self, x ):
        """
        Constructor function. Requires ball number, position (x,y), velocity (x,y), and accelleration (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_VCUSHION, 
                                       None, 
                                       None, None, None, 
                                       x, None );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = VCushion;


    # add an svg method here
    def svg( self ):
        x = phylib.PHYLIB_TABLE_LENGTH / 2
        if (self.obj.vcushion.x == 0):
            x = -25

        return """ <rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n""" % (x)


################################################################################

class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self );
        self.current = -1;

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other );
        return self;

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self;

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1;  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ]; # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1;    # reset the index counter
        raise StopIteration;  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ); 
        if result==None:
            return None;
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall;
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall;
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole;
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion;
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion;
        return result;

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = "";    # create empty string
        result += "time = %6.1f;\n" % self.time;    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj);  # append object description
        return result;  # return the string

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to `make` it a Table object.
        """

        result = phylib.phylib_table.segment( self );
        if result:
            result.__class__ = Table;
            result.current = -1;
        return result;

    # add svg method here
    def svg(self, id, active=False) :
        # returnVal = HEADER
        returnVal = f'<g id="{id}" class="table">\n'
        if (active):
            returnVal = f'<g id="{id}" class="table active">\n'
        for object in self:
            if ((object) and (object.type == phylib.PHYLIB_ROLLING_BALL or object.type == phylib.PHYLIB_STILL_BALL)):
                returnVal += object.svg()
        returnVal += '</g>\n'

        # returnVal += FOOTER

        return returnVal
    
    def roll( self, t ):
        new = Table();
        for ball in self:
            if isinstance( ball, RollingBall ):
                # create4 a new ball with the same number as the old ball
                new_ball = RollingBall( ball.obj.rolling_ball.number,
                                        Coordinate(0,0),
                                        Coordinate(0,0),
                                        Coordinate(0,0) );
                # compute where it rolls to
                phylib.phylib_roll( new_ball, ball, t );
                # add ball to table
                new += new_ball;
            if isinstance( ball, StillBall ):
                # create a new ball with the same number and pos as the old ball
                new_ball = StillBall( ball.obj.still_ball.number,
                Coordinate( ball.obj.still_ball.pos.x,
                ball.obj.still_ball.pos.y ) );
                # add ball to table
                new += new_ball;
        # return table
        return new;

    # helper method
    def cueBall( self ):
        # get cue ball
        for ball in self:
            if isinstance( ball, StillBall ):
                if ball.obj.still_ball.number == 0:
                    temp = ball
        return temp                
    

class Database():

    def __init__( self, reset=False ):
        path = "phylib.db"
        if reset:
            # delete file
            try:
                os.remove(path)
            except FileNotFoundError:
                # file is already deleted
                pass

        self.conn = sqlite3.connect(path)
        self.createDB()

    def Ball( self, cursor ):
        cursor.execute('''CREATE TABLE IF NOT EXISTS Ball(
                       BALLID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                       BALLNO INTEGER NOT NULL,
                       XPOS FLOAT NOT NULL,
                       YPOS FLOAT NOT NULL,
                       XVEL FLOAT,
                       YVEL FLOAT)''')

    def TTable( self, cursor ):
        cursor.execute('''CREATE TABLE IF NOT EXISTS TTABLE(
                       TABLEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                       TIME FLOAT NOT NULL)''')

    def BallTable( self, cursor ):
        cursor.execute('''CREATE TABLE IF NOT EXISTS BallTable(
                       BALLID INTEGER NOT NULL,
                       TABLEID INTEGER NOT NULL,
                       FOREIGN KEY (BALLID) REFERENCES Ball(BALLID),
                       FOREIGN KEY (TABLEID) REFERENCES TTable(TABLEID))''')

    def Shot( self, cursor ):
        cursor.execute('''CREATE TABLE IF NOT EXISTS Shot(
                       SHOTID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                       PLAYERID INTEGER NOT NULL,
                       GAMEID INTEGER NOT NULL,
                       FOREIGN KEY (PLAYERID) REFERENCES Player(PLAYERID),
                       FOREIGN KEY (GAMEID) REFERENCES Game(GAMEID))''')

    def TTable( self, cursor ):
        cursor.execute('''CREATE TABLE IF NOT EXISTS TTABLE(
                       TABLEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                       TIME FLOAT NOT NULL)''')

    def TableShot( self, cursor ):
        cursor.execute('''CREATE TABLE IF NOT EXISTS TableShot(
                       TABLEID INTEGER NOT NULL,
                       SHOTID INTEGER NOT NULL,
                       FOREIGN KEY (TABLEID) REFERENCES TTable(TABLEID),
                       FOREIGN KEY (SHOTID) REFERENCES Shot(SHOTID))''')

    def Game( self, cursor ):
        cursor.execute('''CREATE TABLE IF NOT EXISTS Game(
                    GAMEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    GAMENAME VARCHAR(64) NOT NULL)''')
        
    def Player( self, cursor ):
        cursor.execute('''CREATE TABLE IF NOT EXISTS Player(
                        PLAYERID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        GAMEID INTEGER NOT NULL,
                        PLAYERNAME VARCHAR(64) NOT NULL,
                        FOREIGN KEY (GAMEID) REFERENCES Game(GAMEID))''')

    def createDB( self ):
        cursor = self.conn.cursor()

        self.Ball(cursor)
        self.TTable(cursor)
        self.BallTable(cursor)
        self.Shot(cursor)
        self.TableShot(cursor)
        self.Game(cursor)
        self.Player(cursor)

        cursor.close()
        self.conn.commit()

    def readTable (self, tableID ):
        cursor = self.conn.cursor()

        cursor.execute('''SELECT Ball.BALLNO, Ball.XPOS, Ball.YPOS, Ball.XVEL, Ball.YVEL
                       FROM Ball
                       JOIN BallTable ON Ball.BALLID = BallTable.BALLID
                       WHERE BallTable.TABLEID = ?''', (tableID+1,))
        
        ballsData = cursor.fetchall()
        cursor.close()

        if not ballsData:
            return None

        table = Table()
        for ball in ballsData:
            if (ball[3] is None and ball[4] is None) :
                table += StillBall(ball[0], Coordinate(ball[1], ball[2]))
            else:
                vel = Coordinate(ball[3], ball[4])
                acc = Coordinate(0.0, 0.0)
                if (vectorLength(vel) > VEL_EPSILON):
                    acc.x = -(vel.x / vectorLength(vel)) * DRAG
                    acc.y = -(vel.y / vectorLength(vel)) * DRAG
                table += RollingBall(ball[0], Coordinate(ball[1], ball[2]), vel, acc)

        # get table time
        cursor = self.conn.cursor()

        cursor.execute('''SELECT TTable.TIME
                       FROM TTable
                       WHERE TTable.TABLEID = ?''', (tableID+1,))
        
        time = cursor.fetchall()
        
        table.time = time[0][0]
        cursor.close()
        
        return table

    def writeTable( self, table, commit=True ):
        
        cursor = self.conn.cursor()

        cursor.execute('''INSERT INTO TTable(TIME)
                       VALUES (?)''', (table.time,))
        
        tableID = cursor.lastrowid

        for item in table:

            # ignore cushions and holes cause they are always the same
            if type(item) == StillBall:

                # add to Ball

                cursor.execute('''INSERT INTO Ball(
                               BALLNO, XPOS, YPOS, XVEL, YVEL)
                               VALUES (?,?,?,NULL,NULL)''', 
                               (item.obj.still_ball.number, 
                               item.obj.still_ball.pos.x,
                               item.obj.still_ball.pos.y))

                ballID = cursor.lastrowid
                

                # add to BallTable

                cursor.execute('''INSERT INTO BallTable(BALLID, TABLEID)
                               VALUES (?, ?)''', (ballID, tableID))
                

            elif type(item) == RollingBall:

                cursor.execute('''INSERT INTO Ball(
                               BALLNO, XPOS, YPOS, XVEL, YVEL)
                               VALUES (?,?,?,?,?)''', 
                               (item.obj.rolling_ball.number, 
                               item.obj.rolling_ball.pos.x,
                               item.obj.rolling_ball.pos.y, 
                               item.obj.rolling_ball.vel.x, 
                               item.obj.rolling_ball.vel.y))
                
                ballID = cursor.lastrowid


                # add to BallTable

                cursor.execute('''INSERT INTO BallTable(BALLID, TABLEID)
                               VALUES (?, ?)''', (ballID, tableID))
                

        cursor.close()

        # This is unnecessary and slow, should be deleted but kept for requirement specs
        if commit:
            self.conn.commit()

        return tableID

    def close ( self ):
        self.conn.commit()
        self.conn.close() 

    def setGame( self, gameName, player1Name, player2Name ):
                
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO Game(GAMENAME)
                        VALUES(?)''', (gameName,))

        gameID = cursor.lastrowid

        # add to Player table
        cursor.execute('''INSERT INTO PLAYER(GAMEID, PLAYERNAME)
                            VALUES (?, ?)''', (gameID, player1Name,))
        cursor.execute('''INSERT INTO PLAYER(GAMEID, PLAYERNAME)
                            VALUES (?, ?)''', (gameID, player2Name,))

        self.conn.commit()
        cursor.close()

        return gameID


    def getGame( self, gameID ):
        cursor = self.conn.cursor()
        
        cursor.execute('''SELECT * FROM PLAYER INNER JOIN Game ON Player.GAMEID=Game.GAMEID WHERE Game.GAMEID=?''', (gameID, ))
        # Fetch all rows and save them into a variable
        result = cursor.fetchall()

        if result[0][0] < result[1][0]:
            # player1name
            p1Name = result[0][2]
            # player2name
            p2Name = result[1][2]
        else:
            # player1name
            p2Name = result[0][2]
            # player2name
            p1Name = result[1][2]

        # game name
        gameName = result[0][4]

        return gameName, p1Name, p2Name

class Game():

    def __init__( self, gameID=None, gameName=None, player1Name=None, player2Name=None ):
        self.db = Database()

        if (gameID is not None and gameName is None and player1Name is None and player2Name is None):
            self.gameID = gameID+1
            self.gameName, self.player1Name, self.player2Name = self.db.getGame( self.gameID )

        elif (gameID is None and gameName is not None and player1Name is not None and player2Name is not None):
            self.gameName = gameName
            self.player1Name = player1Name
            self.player2Name = player2Name
            self.gameID = self.db.setGame(self.gameName, self.player1Name, self.player2Name)

        else:
            raise TypeError()


    def newShot( self, playerName ):
        # get playerID using playerName
        # we have self.gameID

        cursor = self.db.conn.cursor()

        cursor.execute('''SELECT Player.PLAYERID
                        FROM Player
                        WHERE PLAYERNAME = ?''', (playerName,))

        playerID = cursor.fetchone()
        playerID = playerID[0]

        cursor.execute('''INSERT INTO Shot(PLAYERID, GAMEID)
                        VALUES (?, ?)''', (self.gameID, playerID))

        shotID = cursor.lastrowid

        self.db.conn.commit()
        cursor.close()

        return shotID

    def shoot( self, gameName, playerName, table, xvel, yvel ):
        shotID = self.newShot( playerName )

        acc = Coordinate(0.0, 0.0)
        vel = Coordinate(xvel, yvel)
        if (vectorLength(vel) > VEL_EPSILON):
            acc.x = -(vel.x / vectorLength(vel)) * DRAG
            acc.y = -(vel.y / vectorLength(vel)) * DRAG

        cueBall = table.cueBall()
        temp = cueBall.obj.still_ball.pos
        cueBall.type = phylib.PHYLIB_ROLLING_BALL

        cueBall.obj.rolling_ball.number = 0
        cueBall.obj.rolling_ball.pos = temp
        cueBall.obj.rolling_ball.vel = vel
        cueBall.obj.rolling_ball.acc = acc

        # call segement until it returns none
        allTables = []
        tableString = ""
        id = 0

        # intial time
        cursor = self.db.conn.cursor()
        copyTable = table
        while table:
            startTime = table.time
            table = table.segment();

            if table:
                elapsed = math.floor((table.time - startTime) / FRAME_INTERVAL)

                # loop over elapsed time
                for i in range(elapsed):
                    t = i * FRAME_INTERVAL
                    newTable = copyTable.roll(t)
                    newTable.time = (startTime + t)
                                        
                    allTables.append(newTable)
                    tableString += newTable.svg(id)
                    id += 1

                    tableID = self.db.writeTable(newTable, commit=False)

                    cursor.execute('''INSERT INTO TableShot(TABLEID, SHOTID)
                                    VALUES (?, ?)''', (tableID, shotID))

                copyTable = table
                allTables.append(table)
                tableString += table.svg(id)

        cursor.close()
        self.db.conn.commit()
        return allTables, tableString

    def shootNoDB( self, gameName, playerName, table, xvel, yvel ):
        allTables = []
        allTables.append(table)
        
        startTime = time.time()
        acc = Coordinate(0.0, 0.0)
        vel = Coordinate(xvel, yvel)
        if (vectorLength(vel) > VEL_EPSILON):
            acc.x = -(vel.x / vectorLength(vel)) * DRAG
            acc.y = -(vel.y / vectorLength(vel)) * DRAG

        cueBall = table.cueBall()
        cueBall.type = phylib.PHYLIB_ROLLING_BALL

        cueBall.obj.rolling_ball.number = 0
        cueBall.obj.rolling_ball.vel = vel
        cueBall.obj.rolling_ball.acc = acc

        # call segement until it returns none
        tableString = ""
        id = 0

        # intial time
        copyTable = table
        while table:
            startTime = table.time
            table = table.segment();

            if table:
                elapsed = math.floor((table.time - startTime) / FRAME_INTERVAL)

                # loop over elapsed time
                for i in range(elapsed):
                    t = i * FRAME_INTERVAL
                    newTable = copyTable.roll(t)
                    newTable.time = (startTime + t)
                    # tableID = self.db.writeTable(newTable, commit=False)
                    allTables.append(newTable)
                    tableString += newTable.svg(id)
                    id += 1
                    # cursor = self.db.conn.cursor()
                    # cursor.execute('''INSERT INTO TableShot(TABLEID, SHOTID)
                    #                 VALUES (?, ?)''', (tableID, shotID))
                    # cursor.close()
                copyTable = table

                allTables.append(table)
                tableString += table.svg(id)
            
        # self.db.close()
        return allTables, tableString
                
    


        



