# SmartBed
Distributed system that allows to track and collect sleeping user’s movements and implement a smart alarm functionality using Rasperry Pi and Arduino.
The systems is divided in four components:
1) Sensing (MMA 7455L sensor)
2) Data collection, packaging and delivery
3) Plotting
4) Dashboard management

<img align="center" width="80%" height="80%" src="https://github.com/FEDE9326/SmartBed/blob/master/img/Architecture.jpg">

The user's movement during sleeping is collected through an accelerometer placed under the matress.
Raspberry Pi and Arduino communicates through MQTT protocol and exchange the following messages:
1) Sensing is turned on/off by user command sent through MQTT message
2) During the sensing phase, the acceleration on the three axis is collected every second
Arduino and Raspberry Pi are connected to the same WLAN.
Raspberry Pi hosts the MQTT broker and runs a Python script that communicates with Freeboard and Thingspeak through REST services.

<img align="center" width="60%" height="60%" src="https://github.com/FEDE9326/SmartBed/blob/master/img/Architecture2.png">

The python script on Raspberry Pi relies on multithreading implementation and allows to manage multiple funcionalities:
1) MQTT publisher and subscriber
2) Continuous collection from Arduino and send on the web without lose data(a queue needed because Thingspeak has an update frequency of 15 seconds)
3) Alarm time
4) Smart alarm function: thread that sleeps until reaches the time to collect movements in that period. Here a lock variable is needed to avoid double ring if the user doesn’t move.

The Quality of sleep (QoS) function evaluates in an approximative way the quality of sleep based on:
1) sensor's datarate
2) number of samples of the queue
3) sensor’s MAXVAL possible
4) total movement and time of sleeping

<img align="center" width="80%" height="80%" src="https://github.com/FEDE9326/SmartBed/blob/master/img/formula.gif">

Freeboard is used as user interface:
1) Available from anywhere at https://freeboard.io/board/ZUART5
2) Show statistics and real time acceleration values from the sensor
3) Control panel in which the user can set the alarm time and activate/deactivate the system
4) Smart alarm function abilitation

<img align="center" width="80%" height="80%" src="https://github.com/FEDE9326/SmartBed/blob/master/img/Freeboard.png">

Thingspeak is used to:
1) Collect data into channels
2) Generate plots

<img align="center" width="80%" height="80%" src="https://github.com/FEDE9326/SmartBed/blob/master/img/Thingspeak.png">

Dweet.io is used as relay between RaspberryPi and Freeboard dashboard:
1) Very simple and intuitive service that permits to create online object
2) Objects can be updated through HTTP POST request with json/XML message format
3) Objects can be monitored through HTTP GET
4) Used to avoid to install in a local server both Freeboard and Thingspeak and to have problem of “open port” and static ip in our router

Smart WakeUp Functionality (Terrible for a lazy users, but useful if you don’t want waste time!): 
1) The user can select how many minutes before the alarm the system can wake him up
2) Realized calculating how much movement the user produces during this period of time
3) If the movement overcome a threshold, the system will ring













