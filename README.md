# Opencv-smart-car

A car using an OpenCV module for camera tracking, also adding obstacle detection

## Description
The Internet of Things (or IoT) is a network consisting of physical objects or devices that
are connected to the Internet and can interact with each other. It is a major milestone in
technological advancements in that it opens up endless possibilities for innovative
applications of different devices and makes way for further development of existing
technologies. With that in mind, a car can be outfitted with various IoT-related
technologies, such as sensors, processors, …, to communicate with other cars or
infrastructures to optimize performance and improve road safety. This type of car is known
as Smart Car, which is what we will be doing for this assignment.<br>
<br>
Traditional cars, while serving their intended purpose of travel, are a volatile and error-prone piece of technology that contributes to many growing problems in modern society,
such as environmental or traffic concerns. Granted that modern cars have improved a lot
throughout history, as long as human input is involved, the risk of accidents is an
ever-looming threat hovering over drivers. Thus, the need for a safer, more efficient, and
possibly automatic means of traversal has been a top priority for many car manufacturers.<br>
<br>
The rising tide of IoT has led to new technologies being incorporated into car designs that
let them perform tasks previously impossible for traditional cars. With advanced
functionalities such as self-driving, object avoidance, and path optimization, Smart Cars are
both efficient and safe with what it does, being able to intelligently weave in and out of
traffic without human input.<br>
<br>
Our project aims to create a mini smart car that will be able to detect obstacles,
track, and automatically follow a line through a mounted camera. A full-fledged IoT
communication will be established between the IoT node (the car) and the edge device
through an MQTT broker. A cloud computing platform is also utilized through the use of an
AWS (Amazon Web Service) EC2 server.

## Hardware and software used
![image](https://github.com/Travis-Houston/Akathon2023-Opencv-smart-car/assets/131174749/65a55bab-d74e-423e-9db1-a2c79ed97b97)

## Conceptual designs
For a car to be considered smart, it needs to employ various IoT technologies such as
sensors, processors, actuators, and other communication devices. Smart cars should be
able to drive themselves automatically while avoiding obstacles on the road as well as being able
to connect to other IoT devices within the network. We implemented an ultrasonic sensor
on the front to detect obstacles and a camera to implement self-driving. The Raspberry Pi
will be the brain of the IoT node, receiving information from the sensors and sending
signals to the motor drivers to move the car.

* <b>Block diagram:</b><br>
![image](https://github.com/Travis-Houston/Akathon2023-Opencv-smart-car/assets/131174749/b5f7b726-df4f-4363-9b0e-0c81dccff960)

* <b>Operation flowchart:</b> <br>
![image](https://github.com/Travis-Houston/Akathon2023-Opencv-smart-car/assets/131174749/0015ef42-1533-4635-90dd-8d75e80f1502)


## Dependencies

Install the following dependencies to create a camera stream and database.

```
sudo apt-get update 
sudo apt-get upgrade

sudo apt-get install libatlas-base-dev
sudo apt-get install libjasper-dev
sudo apt-get install libqtgui4 
sudo apt-get install libqt4-test
sudo apt-get install libhdf5-dev

sudo pip3 install numpy
sudo pip3 install opencv-contrib-python
sudo pip3 install opencv-python
sudo apt install mariadb-server
sudo mysql_secure_installation
```

### Installing

If you want to try, just clone this repository through:
```
git clone https://github.com/Travis-Houston/Akathon2023-Opencv-smart-car.git
```

## Authors

### Huynh Nguyen Quoc Bao (Travis-Houston):
* Phone: 0707191380
* Email: baohnq2003@gmail.com
### Le Hoang Hai (HaileInnoTech)
* Phone: 
* Email:
### Nguyen Nhat Huy
* Phone: 
* Email: 
