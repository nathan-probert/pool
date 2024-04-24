import ctypes
import math
import os
import random
import sys; # used to get argv
import cgi
import time; # used to parse Mutlipart FormData 
            # this should be replace with multipart in the future

import Physics
from urllib.parse import parse_qs

from Physics import SCREEN_TABLE_WIDTH
from Physics import SCREEN_TABLE_HEIGHT

# web server parts
from http.server import HTTPServer, BaseHTTPRequestHandler;

# used to parse the URL and extract form data for GET requests
from urllib.parse import urlparse, parse_qsl;

def deleteTables():
    for filename in os.listdir("."):
        if filename.startswith('table-') and filename.endswith('.svg'):
            try:
                os.remove(filename)
            except OSError as e:
                pass

def vectorLength(vel):
    return math.sqrt(vel.x * vel.x + vel.y * vel.y);

def makeSvg(number, table):
    with open(f"./table-{number}.svg", "w") as fp:
        fp.write(f"{table.svg()}");

def makeBigSvg(tables):
    with open(f"./table-1.svg", "w") as fp:
        fp.write(f"{tables}");

def nudge():
    return random.uniform( -1.5, 1.5 );

from Physics import *
def compareTables( initial, final ):
    sunkBalls = []
    for i in range(10, 26):
        ball1 = initial[i]
        if ball1 is not None:
            found = False
            if isinstance( ball1, StillBall ):
                ball1Num = ball1.obj.still_ball.number
            if isinstance( ball1, RollingBall):
                ball1Num = ball1.obj.rolling_ball.number
            
            for j in range(10,26):
                ball2 = final[j]
                if ball2 is not None:
                    if isinstance( ball2, StillBall ):
                        ball2Num = ball2.obj.still_ball.number
                    if isinstance( ball2, RollingBall):
                        ball2Num = ball2.obj.rolling_ball.number

                    if ball1Num == ball2Num:
                        # found ball
                        found = True

            if (found == False):
                sunkBalls.append({"ball" : ball1, "num" : ball1Num})

    return sunkBalls

def respawn( table ):
    
    # make sure location is free?
    pos = Physics.Coordinate( Physics.TABLE_WIDTH/2.0 + 2,
                            Physics.TABLE_LENGTH - Physics.TABLE_WIDTH/2.0 );
    sb  = Physics.StillBall( 0, pos );
    table += sb;

    return table;

def setupTable():
    table = Physics.Table();

    # ROW 1

    # 1 ball
    pos = Physics.Coordinate( 
                    Physics.TABLE_WIDTH / 2.0 + nudge(),
                    Physics.TABLE_WIDTH / 2.0 + nudge(),
                    );

    sb = Physics.StillBall( 1, pos );
    table += sb;

    # ROW 2

    # 2 ball
    pos = Physics.Coordinate(
                    Physics.TABLE_WIDTH/2.0 - (Physics.BALL_DIAMETER+4.0)/2.0 + nudge(),
                    Physics.TABLE_WIDTH/2.0 - 
                    math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0) + nudge()
                    );
    sb = Physics.StillBall( 2, pos );
    table += sb;

    # 9 ball
    pos = Physics.Coordinate(
                    Physics.TABLE_WIDTH/2.0 + (Physics.BALL_DIAMETER+4.0)/2.0 + nudge(),
                    Physics.TABLE_WIDTH/2.0 - 
                    math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0) + nudge()
                    );
    sb = Physics.StillBall( 9, pos );
    table += sb;

    # ROW 3

    # 3 ball
    pos = Physics.Coordinate(
                    Physics.TABLE_WIDTH/2.0 - 2*((Physics.BALL_DIAMETER+4.0)/2.0) + nudge(),
                    Physics.TABLE_WIDTH/2.0 - 
                    2*(math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0)) + nudge()
                    );
    sb = Physics.StillBall( 3, pos );
    table += sb;    

    # 8 ball
    pos = Physics.Coordinate(
                    Physics.TABLE_WIDTH / 2.0 + nudge(), 
                    Physics.TABLE_WIDTH/2.0 - 
                    2*math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0) + nudge()
                    );
    sb = Physics.StillBall( 8, pos );
    table += sb;

    # 10 ball
    pos = Physics.Coordinate(
                    Physics.TABLE_WIDTH/2.0 + 2*((Physics.BALL_DIAMETER+4.0)/2.0) + nudge(),
                    Physics.TABLE_WIDTH/2.0 - 
                    2*(math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0)) + nudge()
                    );
    sb = Physics.StillBall( 10, pos );
    table += sb;  

    # ROW 4

    # 4 ball
    pos = Physics.Coordinate(
                    Physics.TABLE_WIDTH/2.0 - 3*((Physics.BALL_DIAMETER+4.0)/2.0) + nudge(),
                    Physics.TABLE_WIDTH/2.0 - 
                    3*(math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0)) + nudge()
                    );
    sb = Physics.StillBall( 4, pos );
    table += sb;  

    # 14 ball
    pos = Physics.Coordinate(
                    Physics.TABLE_WIDTH/2.0 - (Physics.BALL_DIAMETER+4.0)/2.0 + nudge(),
                    Physics.TABLE_WIDTH/2.0 - 
                    3*(math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0)) + nudge()
                    );
    sb = Physics.StillBall( 14, pos );
    table += sb;

    # 7 ball
    pos = Physics.Coordinate(
                    Physics.TABLE_WIDTH/2.0 + (Physics.BALL_DIAMETER+4.0)/2.0 + nudge(),
                    Physics.TABLE_WIDTH/2.0 - 
                    3*(math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0)) + nudge()
                    );
    sb = Physics.StillBall( 7, pos );
    table += sb;

    # 11 ball
    pos = Physics.Coordinate(
                    Physics.TABLE_WIDTH/2.0 + 3*((Physics.BALL_DIAMETER+4.0)/2.0) + nudge(),
                    Physics.TABLE_WIDTH/2.0 - 
                    3*(math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0)) + nudge()
                    );
    sb = Physics.StillBall( 11, pos );
    table += sb; 

    # ROW 5

    # 12 ball
    pos = Physics.Coordinate(
                    Physics.TABLE_WIDTH/2.0 - 4*((Physics.BALL_DIAMETER+4.0)/2.0) + nudge(),
                    Physics.TABLE_WIDTH/2.0 - 
                    4*(math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0)) + nudge()
                    );
    sb = Physics.StillBall( 12, pos );
    table += sb;  

    # 6 ball
    pos = Physics.Coordinate(
                    Physics.TABLE_WIDTH/2.0 - 2*((Physics.BALL_DIAMETER+4.0)/2.0) + nudge(),
                    Physics.TABLE_WIDTH/2.0 - 
                    4*(math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0)) + nudge()
                    );
    sb = Physics.StillBall( 6, pos );
    table += sb; 

    # 15 ball
    pos = Physics.Coordinate(
                    Physics.TABLE_WIDTH / 2.0 + nudge(), 
                    Physics.TABLE_WIDTH/2.0 - 
                    4*math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0) + nudge()
                    );
    sb = Physics.StillBall( 15, pos );
    table += sb;

    # 13 ball
    pos = Physics.Coordinate(
                    Physics.TABLE_WIDTH/2.0 + 2*((Physics.BALL_DIAMETER+4.0)/2.0) + nudge(),
                    Physics.TABLE_WIDTH/2.0 - 
                    4*(math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0)) + nudge()
                    );
    sb = Physics.StillBall( 13, pos );
    table += sb; 

    # 5 ball
    pos = Physics.Coordinate(
                    Physics.TABLE_WIDTH/2.0 + 4*((Physics.BALL_DIAMETER+4.0)/2.0) + nudge(),
                    Physics.TABLE_WIDTH/2.0 - 
                    4*(math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0)) + nudge()
                    );
    sb = Physics.StillBall( 5, pos );
    table += sb;  

    # CUE BALL

    pos = Physics.Coordinate( Physics.TABLE_WIDTH/2.0 + 2,
                            Physics.TABLE_LENGTH - Physics.TABLE_WIDTH/2.0 );
    sb  = Physics.StillBall( 0, pos );
    table += sb;

    return table


# handler for our web-server - handles both GET and POST requests
class MyHandler( BaseHTTPRequestHandler ):
    game = None
    curPlayer = None
    table = None

    def genString( self, table, gameName, p1Name, p2Name, curPlayer ):
        header = f'''<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta http-equiv="X-UA-Compatible" content="ie=edge">
            <title>Display</title>
            <link rel="stylesheet" href="game.css">
            <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.3/jquery.min.js">
            </script>
        </head>
        <body>
        <h1>{gameName}</h1>'''
        
        if curPlayer == 1:
            header += f'''<div class=names><h2 id='p1' class="cur">{p1Name}</h2><h2 id='p2' class="">{p2Name}</h2></div>'''
        else:
            header += f'''<div class=names><h2 id='p1' class="">{p1Name}</h2><h2 id='p2' class="cur">{p2Name}</h2></div>'''
        
        # add remaining balls
        header += f'''
        <div class="remainingBalls">
            <div class="p1Balls" id="p1Balls"></div>
            <div class="p2Balls" id="p2Balls"></div>
        </div>
        <div class="center">
            <svg id="bigCon" class="bigCon" width="1000" height="1964.28" viewBox="-25 -25 1400 2750" onmousemove="trackit(event);">
                <line id="dynamicLine" x1="0" y1="0" x2="0" y2="0" stroke="black" stroke-width="3"/>
            </svg>
            <svg id="default" class="default svgCon" width="{SCREEN_TABLE_WIDTH}" height="{SCREEN_TABLE_HEIGHT}" viewBox="-25 -25 1400 2750";"
                xmlns="http://www.w3.org/2000/svg"
                xmlns:xlink="http://www.w3.org/1999/xlink">
                <rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" /> <rect width="1400" height="25" x="0" y="-25" fill="darkgreen" />
                <rect width="1400" height="25" x="0" y="2700.0" fill="darkgreen" />
                <rect width="25" height="2700" x="-25" y="0" fill="darkgreen" />
                <rect width="25" height="2700" x="1350.0" y="0" fill="darkgreen" />
                <circle cx="0.0" cy="0.0" r="114.0" fill="black" />
                <circle cx="0.0" cy="1350.0" r="114.0" fill="black" />
                <circle cx="0.0" cy="2700.0" r="114.0" fill="black" />
                <circle cx="1350.0" cy="0.0" r="114.0" fill="black" />
                <circle cx="1350.0" cy="1350.0" r="114.0" fill="black" />
                <circle cx="1350.0" cy="2700.0" r="114.0" fill="black" />
            </svg>
            <svg class="svgCon" id="svgCon" width="{SCREEN_TABLE_WIDTH}" height="{SCREEN_TABLE_HEIGHT}" viewBox="-25 -25 1400 2750"
                xmlns="http://www.w3.org/2000/svg"
                xmlns:xlink="http://www.w3.org/1999/xlink">
                
                
            '''

        body = f'''{table.svg(0, True)}'''

        footer = '''
                
            </svg>
        </div>
        </body>
            <script src="app.js"></script>
        </html>
        '''

        return header + body + footer

    def do_GET(self):
        # parse the URL to get the path and form data
        parsed  = urlparse( self.path );

        # check if the web-pages matches the list
        if parsed.path in [ '/info.html' ]:

            # clear database
            db = Physics.Database(  );
            db.createDB();

            # retreive the HTML file
            fp = open( '.'+self.path );
            content = fp.read();

            # generate the headers
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len( content ) );
            self.end_headers();

            # send it to the broswer
            self.wfile.write( bytes( content, "utf-8" ) );
            fp.close();

        # check if the web-pages matches the list
        elif self.path.startswith('/table-') and self.path.endswith('.svg'):

            # retreive the HTML file
            fp = open( '.'+self.path );
            content = fp.read();

            # generate the headers
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "image/svg+xml" );
            self.send_header( "Content-length", len( content ) );
            self.end_headers();

            # send it to the broswer
            self.wfile.write( bytes( content, "utf-8" ) );
            fp.close();
        
        elif self.path == '/game.css':
            try:
                with open('game.css', 'rb') as file:
                    content = file.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/css')
                self.send_header('Content-length', len(content))
                self.end_headers()
                self.wfile.write(content)
            except FileNotFoundError:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(bytes("404: CSS file not found", "utf-8"))
            
        elif self.path == '/app.js':
            try:
                with open('app.js', 'rb') as file:
                    content = file.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/javascript')
                self.send_header('Content-length', len(content))
                self.end_headers()
                self.wfile.write(content)
            except FileNotFoundError:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(bytes("404: Javascript file not found", "utf-8"))
        
        else:
            # generate 404 for GET requests with no valid repsonse
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: Path %s not found" % self.path, "utf-8" ) );

    def do_POST(self):
        # handle post request
        # parse the URL to get the path and form data
        parsed  = urlparse( self.path );

        if parsed.path in [ '/game.html' ]:

            # get data sent as Multipart FormData (MIME format)
            try:
                form = cgi.FieldStorage( fp=self.rfile,
                                        headers=self.headers,
                                        environ = { 'REQUEST_METHOD': 'POST',
                                                    'CONTENT_TYPE': 
                                                    self.headers['Content-Type'],
                                                } 
                                    );
                
                # delete all svg files
                deleteTables()

                gName = str(form['game_name'].value);
                p1Name = str(form['p1_name'].value);
                p2Name = str(form['p2_name'].value);

                MyHandler.game = Physics.Game( gameName=gName, player1Name=p1Name, player2Name=p2Name );
                MyHandler.curPlayer = random.randint(1, 2)

                MyHandler.player1 = {"name": p1Name, "type": None, "remainingBalls": None}
                MyHandler.player2 = {"name": p2Name, "type": None, "remainingBalls": None}

                MyHandler.table = setupTable();
            
                # show table
                content = self.genString(self.table, gName, p1Name, p2Name, MyHandler.curPlayer)

                # generate the headers
                self.send_response( 200 ); # OK
                self.send_header( "Content-type", "text/html" );
                self.send_header( "Content-length", len( content ) );
                self.end_headers();
            
                self.wfile.write( bytes( content, "utf-8" ) );
            except Exception as e:
                # not first shot
                print(e)

            # somehow show first table and then call game.shoot once we have the player's shot

        elif parsed.path in ['/makeShot']:
            if MyHandler.game is not None:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length).decode('utf-8')
                post_params = parse_qs(post_data)

                limit = 3000
                vel_x = float(post_params['x'][0])
                vel_y = float(post_params['y'][0])
                # vel_x = max(min(float(post_params['x'][0]), limit), -limit)
                # vel_y = max(min(float(post_params['y'][0]), limit), -limit)
                # Calculate the magnitude of the velocity vector
                magnitude = max(abs(vel_x), abs(vel_y))

                # Check if the magnitude exceeds the limit
                if magnitude > limit:
                    # Scale both velocity components proportionally to bring the magnitude down to the limit
                    scale_factor = limit / magnitude
                    vel_x *= scale_factor
                    vel_y *= scale_factor

                # basically instant up until here

                # get the player who made the shot
                if MyHandler.curPlayer == 1:
                    curPlayer = MyHandler.player1
                    otherPlayer = MyHandler.player2
                    other = 2
                else:
                    curPlayer = MyHandler.player2
                    otherPlayer = MyHandler.player1
                    other = 1

                ogTable = Physics.Table()
                for i in range(10, 26):
                    ogTable += MyHandler.table[i]

                allTables, tables = MyHandler.game.shootNoDB("", curPlayer['name'], MyHandler.table, vel_x, vel_y);

                if (len(allTables) >= 200000):
                    print(f"Too many tables - {len(allTables)}")
                    exit(1);

                
                MyHandler.table = allTables[-1]

                # compare first and last table, return sunk balls
                sunkBalls = compareTables(allTables[0], allTables[-1]);

                winner = None
                switch = True
                for ball in sunkBalls:
                    if ball['num'] == 0:
                        newTable = respawn(allTables[-1])
                        tables += newTable.svg(len(allTables))
                        MyHandler.table = newTable
                    elif ball['num'] == 8:
                        # check remaining balls
                        if curPlayer['remainingBalls'] and 8 in curPlayer['remainingBalls']:
                            winner = MyHandler.curPlayer
                        else:
                            winner = other
                    elif (curPlayer['type'] == None):
                        switch = False
                        if ball['num'] < 8:
                            curPlayer['type'] = 'low'
                            otherPlayer['type'] = 'high'
                        elif ball['num'] > 8:
                            curPlayer['type'] = 'high'
                            otherPlayer['type'] = 'low'
                    elif (curPlayer['type'] == 'low'):
                        if ball['num'] < 8:
                            switch = False
                    elif (curPlayer['type'] == 'high'):
                        if ball['num'] > 8:
                            switch = False

                if curPlayer['type'] is not None:
                    curPlayer['remainingBalls'] = []
                    for i in range(10, 26):
                        if allTables[-1][i] is not None:
                            num = allTables[-1][i].obj.still_ball.number
                            if curPlayer['type'] == 'high':
                                if num > 8:
                                    curPlayer['remainingBalls'].append(num);
                            elif curPlayer['type'] == 'low':
                                if num < 8 and num > 0:
                                    curPlayer['remainingBalls'].append(num);
                
                    # if empty, they must score 8 ball
                    if not curPlayer['remainingBalls']:
                        curPlayer['remainingBalls'].append(8)
            
                if otherPlayer['type'] is not None:
                    otherPlayer['remainingBalls'] = []
                    for i in range(10, 26):
                        if allTables[-1][i] is not None:
                            num = allTables[-1][i].obj.still_ball.number
                            if otherPlayer['type'] == 'high':
                                if num > 8:
                                    otherPlayer['remainingBalls'].append(num);
                            elif otherPlayer['type'] == 'low':
                                if num < 8 and num > 0:
                                    otherPlayer['remainingBalls'].append(num);
                
                    # if empty, they must score 8 ball
                    if not otherPlayer['remainingBalls']:
                        otherPlayer['remainingBalls'].append(8)


                if switch:
                    MyHandler.curPlayer = 2 if MyHandler.curPlayer == 1 else 1

                # write to SVG and then use .load to display in js
                makeBigSvg(tables)

                low = None
                high = None
                if (curPlayer['type'] == "low"):
                    low = MyHandler.curPlayer
                    high = other
                if (curPlayer['type'] == "high"):
                    high = MyHandler.curPlayer
                    low = other

                import json
                self.send_response(200)  # OK
                self.send_header("Content-type", "application/json")
                response = {'winner': winner, 
                            'curPlayer': MyHandler.curPlayer, 
                            'low': low, 
                            'high': high, 
                            'p1Remain': MyHandler.player1['remainingBalls'], 
                            'p2Remain': MyHandler.player2['remainingBalls']}
                response_bytes = json.dumps(response).encode("utf-8")
                self.send_header("Content-length", len(response_bytes))
                self.end_headers()

                self.wfile.write(response_bytes)
                MyHandler.game.shoot("", curPlayer['name'], ogTable, vel_x, vel_y);


            else:
                # Handle the case where the game object is not initialized
                self.send_response(400)
                self.end_headers()
                self.wfile.write(bytes("400: Game object not initialized", "utf-8"))
        
        else:
            # generate 404 for POST requests that aren't the file above
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) );

if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print("Please enter a port number.")
        exit()
    
    httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), MyHandler );
    print( "Server listing in port:  ", int(sys.argv[1]) );
    httpd.serve_forever();
