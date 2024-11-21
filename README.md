## Intelligent Auto - Transcending the driving hassle free.

To convert the convert the conventional vechicle to into a SDV we used sensors and measurements from the vehicle published over eCAL network and built apps that help estimate
1. Vehicle Stability
2. Traffic rules violation Check
3. Collison Detection
4. Vehicle health monitoring
5. Know Your Breaks

### Vehicle Stability
Vehicle stability measure how stable the vehicle is in the road, this is estiamted using Vehicle Yaw rate, Steering angle and lateral acceleration. This in turn denotes if the driver is awake.

### Traffic rules violation check: 
This app checks for the Traffic speed limitations and Traffic warning and alert the user on the warnings. This app uses YOLO object dectection data to detect the traffic signals. 

### Collision detection
This app checks for collison detection of vehicles such as car, trucks etc and pedestrians. A Safety region of interest is defined using the Camera's FOV and if any object comes in the roi user will get warnings. 

### Vehicle health monitoring
This app measures the Vehicle health based on the Vehicle acceleration, deceleration and speed to check for Jerks, Quick acceleration/deceleration etc. This app is built with the idea that we can monitor various sensors in the vechile and predict a score as vehicle health - so that user would get to know about the vehicle better. 

For the hackathon purpose we used existing signals and predicted a score based on user driving pattern. 

### Know your breaks
This app is enable by a click of a button denoting user is going for a long drive. In the long drive, this app finds out whether the user had taken break it between the ride for a safer journey. For example: In a 2 hour ride, Driver should take rest for atleast 10 minutes for refreshments. 

The apps are built into as a docker images and is orchestrated by AnkaiOS. 

