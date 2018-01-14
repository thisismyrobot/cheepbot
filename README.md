# Cheepbot

![Bot](bot.jpg?raw=true "Bot")

## Design

A set of RESTful HTTP microservices running on a Raspberry Pi Zero, inside a
very cheap Roomba clone.

## Services

This will grow over time of course.

### Camera

GET to http://[ip]:10000 will return an image from the ceiling-facing camera
with embedded (when my hardware arrives) orientation information, stored in
the GPSImgDirection Exif tag.

### Map builder

POST of an image to http://[ip]:10001/map will add that image to a map based
on SIFT feature detection, returning a composite map image. The "Robot-Step-
Succeeded" header returned in the 302 response is the success flag of adding
the new image to the map. The 302 response points to the GET on /map.

GET to http://[ip]:10001/map will return the current map. The "Robot-Path"
header returned is the ordered list of pixel locations on the map for each
image that was uploaded allowing for path display.

DELETE to http://[ip]:10001/map will reset the map to a fresh start.

GET to http://[ip]:10001 will show a test page for exercising the builder with
manually uploaded images.

### Motor

Very WIP.

POST 'command' of 'forward' or 'stop' to http://[ip]:10002/motor/command

GET http://[ip]:10002/motor for a test page.

## Typo?

The spelling is not a typo, it's a nod to a joke about what sound a 30 foot
budgie makes, the budgie in question was being the mascot for a budget
shopping chain that formally existed in Tasmania. The robot chassis was bought
from a similar place. Sorry.
