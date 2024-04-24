# Running the program
 - First download the docker image "socsguelph/cis2750" from "https://hub.docker.com/r/socsguelph/cis2750"
 - Start the image with the command ```docker run --name [container-name] -v [path-to-local-dir:remote-dir] -it socsguelph/cis2750```, with your container-name and paths to local and remote directories
 - Compile the C files with ```make```
 - Run the program using ```server.py [port-number]```, where port number is the port you would like the game to run on
 - Navigate to ```http://localhost:[port-number]/info.html``` and follow the on-screen instructions to play

<video controls src="Pool Example.mp4" title="Pool Game Example"></video>
 ![alt text](image.png)