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
    "PINK",
    "MEDIUMPURPLE",
    "LIGHTSALMON",    
    "LIGHTGREEN",
    "SANDYBROWN",       
    ];
function genBall(num) {
    return `<svg><circle cx="28.5" cy="28.5" r="28.5" fill="${BALL_COLOURS[num]}" class="display"/></svg>`;
}
    

var svg = document.getElementById("svgCon");
var cueBalls = svg.querySelectorAll("[fill='WHITE']");
var cueBall = cueBalls[cueBalls.length - 1];
var cueBallX = parseFloat(cueBall.getAttribute("cx"));
var cueBallY = parseFloat(cueBall.getAttribute("cy"));

var lowUpdated = false

var onBall = false;

var bigSvg = document.getElementById("bigCon");
bigSvg.addEventListener("mousedown", ()=>print(event));
bigSvg.addEventListener("mouseup", ()=>shoot(event));

// Get the line element
var line = document.getElementById('dynamicLine');

// Function to update line coordinates
function updateLine(x1, y1, x2, y2) {
    line.setAttribute('x1', x1);
    line.setAttribute('y1', y1);
    line.setAttribute('x2', x2);
    line.setAttribute('y2', y2);
}

function closeEnough(x, y) {
    if (x <= 28.5 && x >= -28.5) {
        if (y <= 28.5 && y >= -28.5) {
            return true;
        }
    }
    return false;
}

function screenToSVG(screenX, screenY) {
    var p = svg.createSVGPoint()
    p.x = screenX
    p.y = screenY
    return p.matrixTransform(svg.getScreenCTM().inverse());
}

function screenToBigSVG(screenX, screenY) {
    var p = bigSvg.createSVGPoint()
    p.x = screenX
    p.y = screenY
    return p.matrixTransform(bigSvg.getScreenCTM().inverse());
}

function SVGToScreen(svgX, svgY) {
    var p = svg.createSVGPoint()
    p.x = svgX
    p.y = svgY
    return p.matrixTransform(svg.getScreenCTM());
}

function print(event) {
    var  pt = screenToSVG(event.pageX, event.pageY);

    var dX = pt.x - cueBallX;
    var dY = pt.y - cueBallY;
    if (closeEnough(dX, dY)) {
        onBall = true;
    } else {
        onBall = false;
    }
}

var svgContainers;
const nextShot = document.getElementById("svgCon");
function shoot(event) {
    if (onBall) {
        onBall = false;
        updateLine(0, 0, 0, 0);
        var vel = calcVel(event.pageX, event.pageY); // check this line

        $.post('/makeShot', vel, function(data, status) {
            if (status === 'success') {
                const end = performance.now();

                var url = "table-1.svg";

                var winner = data.winner
                var curPlayer = data.curPlayer
                var low = data.low
                var high = data.high

                var $targetElement = $(nextShot);
                
                const retries = 10

                // start of loop
                var i = 0
                loadSVG()
                function loadSVG() {
                    if (i < 10) {



                        $targetElement.load(url, function(response, status, xhr) {
                            if (status == "error") {
                                // If an error occurs, log the error
                                console.error("Failed to load SVG file: " + xhr.status);
                                i += 1
                                loadSVG()
                            } else {
                            
                                i = 10
                                svgContainers = document.querySelectorAll('.table'); // and this       
                                    
                                $(svgContainers).each(function(i, ele) {
                                    var delay = i * 10; // Delay in milliseconds
                                
                                    // Display current SVG
                                    setTimeout(() => {
                                        $(ele).addClass("active");
                                        $(svgContainers[i-1]).removeClass("active");
                                    }, delay);
                                
                                    // Remove active class for all except the very last SVG
                                    if (i == svgContainers.length - 1) {
                                        setTimeout(() => {
                                            $(svgContainers).not('.active').remove();
                                            cueBalls = document.querySelectorAll("[fill='WHITE']");
                                            // no cueBalls = game over

                                            // get scored balls, maybe pass from function

                                            cueBall = cueBalls[cueBalls.length - 1];
                                            cueBallX = parseFloat(cueBall.getAttribute("cx"));
                                            cueBallY = parseFloat(cueBall.getAttribute("cy"));
                                            svg = document.getElementsByClassName("svgCon")[1];

                                            // update high/low
                                            if (low == 1 && !lowUpdated) {
                                                document.getElementById('p1').textContent += ' - low';
                                                document.getElementById('p2').textContent += ' - high';
                                                lowUpdated = true
                                            } else if (low == 2 && !lowUpdated) {
                                                document.getElementById('p2').textContent += ' - low';
                                                document.getElementById('p1').textContent += ' - high';
                                                lowUpdated = true
                                            }

                                            // update cur player
                                            if (curPlayer == 1) {
                                                document.getElementById('p2').classList.remove('cur');
                                                document.getElementById('p1').classList.add('cur');
                                            } else if (curPlayer == 2) {
                                                document.getElementById('p1').classList.remove('cur');
                                                document.getElementById('p2').classList.add('cur');
                                            }

                                            // update remaining balls
                                            if (lowUpdated) {
                                                var allBalls = [];
                                                data.p1Remain.forEach(ballNum => {
                                                    allBalls.push(genBall(ballNum));
                                                });
                                                document.getElementById('p1Balls').innerHTML = allBalls.join("");

                                                var allBalls = [];
                                                data.p2Remain.forEach(ballNum => {
                                                    allBalls.push(genBall(ballNum));
                                                });
                                                document.getElementById('p2Balls').innerHTML = allBalls.join("");
                                            }

                                            handleWinner();
                                            function handleWinner() {
                                                if (winner) {
                                                    if (winner == 1) {
                                                        var words = document.getElementById('p1').textContent.trim().split(/\s+/);
                                                    } else if (winner == 2) {
                                                        var words = document.getElementById('p2').textContent.trim().split(/\s+/);
                                                    }
                                                    words.pop()
                                                    if (lowUpdated) {
                                                        words.pop();
                                                    }
                                                    var name = words.join(' ')
                                                    alert(`Game Over! ${name} won!`)

                                                    window.location.href = "http://localhost:56772/info.html"
                                                }
                                            }
                                        }, delay + 20); // Delay for removing the last SVG
                                    }
                                });                    
                            }
                        });
                    }
                
                }

            }
        });
        
    }

    function calcVel(x1, y1) {
        var cueB = SVGToScreen(cueBallX, cueBallY);
        var x2 = cueB.x;
        var y2 = cueB.y;
        var y = 10*(x1-x2);
        var x = -10*(y1-y2);
        return {'x' : x, 'y': y};
    }
}


function trackit( event ) {
    if (onBall) {
        var  pt = screenToBigSVG(event.pageX, event.pageY);

        // svg to screen
        var screen = SVGToScreen(cueBallX, cueBallY);
        // screen to big
        var big = screenToBigSVG(screen.x, screen.y);

        updateLine(big.x, big.y, pt.x, pt.y);
    }
}