# Summer-Internship
Solar panel controller/UI

SSummer Internship
Solar panel controller
Constructive Systems, Inc

Developed custom solar panel controller and data collector for agroenergy company. Controller automatically tracks the sun from sunup to sundown. It also allows the user to control the position of the panels through a web based client.

Controller used ruggedized Raspberry Pi running Linux. Controller code written in Python and used the Flask web framework and TCP/IP for communicating with the web client. Used Message Queue Telemetry Transport (MQTT) for configuration and data collection. Developed a DHCP style protocol to allow real time changes in configuration and maintenance with minimal or no down time.

Solar tracking was accomplished using Pysolar’s azimuth method to approximate the sun’s position, and field measurements of the time interval needed for the motor to move one degree. The motor is energized for that interval with each degree change in the sun’s position. The panels reset to the starting position each night, eliminating any drift.

Currently, there is an installation in Northern California testing the controller with excellent results.  There has been little or no down time, and solar tracking has proven to be very accurate.






