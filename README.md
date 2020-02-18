# Summer-Internship
Solar panel controller/UI

Summer internship for an agroenergy company working on solar panel installations for novel use cases.

This code written with Python and javascript, use the Flask framework, is a prototype and proof of concept for a ruggedized raspberry pi
controller that predictively tracks the sun, allows the user to connect to a webserver to move the solar panels via a UI.
Additionally, there is a prototype DHCP type protocol for allowing the controllers to be able to communicate with eachother, this feature
has not been fully implimented and is still untested.  

The solar tracking works based on field measurements of the movement speed of the motor, which has the excellent features of
moving very slowly (a short start up time to reach operating velocity) and while operating very little variablity in speed.

Python will poll the pysolar library's Azimuth method and when the azimuth has changed a full degree will fire off the motor. The motor
then moves one degree.  This method works on approximations, but very good approximations, and is able to be reset each night into the
starting position ensures that any drift that might have occured will be removed.  


Currently, there is an installation in Northern California testing the controller.  Testing is going quite well.

There are a number of folders in this project.  The most relevant is 'Motor Testing'.

Some of the other folders relate to our research and attempt to use Google's map API to programmatically set 
the map location to above the solar installation, and then using GPS devices on each controller, have them set their coordinates on
the UI.  This feature would have been a novel way to allow for a plug and play setup. However, we found that to get a GPS device
that could be accurate enough to relay the proper coordinate to the backend would have been prohibitively expensive.  

I have some other ideas for creating a user friendly and simple UI for connecting a controller to a location on the user's screen that
clearly corresponds to a specific rack.


Multithreading (or as close to it as you can get with high level python)
Pysolar - a python library for determining where the sun is (Azimuth) based on time and location.



