import cv2
import motor1
import RPi.GPIO as GPIO
import time
import threading
import mysql.connector

#Connect to MySQL database
mydb = mysql.connector.connect(
    host="18.236.87.185",
    user="haile",
    password="12345678",
    database="AKATHON2023"
)

#Initialize global variables
cx = None
cy = None
string = ""

#Define function to execute SQL queries
def execute_sql(sql, val):
    mycursor = mydb.cursor()
    mycursor.execute(sql, val)
    mydb.commit()

#Function to continuously insert data to database
def insert_data_to_db():
    while True:
        val = (cx, cy, string)
        sql = "INSERT INTO Log (cx, cy, status) VALUES (%s, %s, %s)"
        execute_sql(sql, val)
        time.sleep(1)

#Initialize motor1 object
m1 = motor1

#Set minimum distance for obstacle detection
min_distance = 20

#Configure GPIO pins
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#Function to continuously measure distance using ultrasonic sensor
trig = 23
echo = 24

GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)

def distance_thread():
    global distance
    while True:
        GPIO.output(trig, GPIO.LOW)
        time.sleep(0.02)
        GPIO.output(trig, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(trig, GPIO.LOW)

        pulse_start = time.time()
        timeout = pulse_start + 0.1
        while GPIO.input(echo) == GPIO.LOW and pulse_start < timeout:
            pulse_start = time.time()

        pulse_end = time.time()

        timeout = pulse_end + 0.1

        while GPIO.input(echo) == GPIO.HIGH and pulse_end < timeout:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start

        distance = pulse_duration * 17150

        time.sleep(0.02)

distance = None

#Start distance_thread as a daemon thread
distance_thread = threading.Thread(target=distance_thread)
distance_thread.daemon = True
distance_thread.start()

#Initialize video capture using OpenCV
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 360)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
cap.set(cv2.CAP_PROP_FPS, 30)

#Initialize variables for calculating FPS
fps_start = time.time()
fps_frames = 0

#Start insert_data_to_db thread as a daemon thread
db_thread = threading.Thread(target=insert_data_to_db)
db_thread.daemon = True
db_thread.start()

#Start main loop for image processing and motor control
while True:
    # Read a frame from the video capture
    ret, frame = cap.read()
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian Blur to reduce noise
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply thresholding to create a binary image
    _, thresh1 = cv2.threshold(blur, 50, 255, cv2.THRESH_BINARY_INV)

    # Perform morphological operations to remove small objects and fill gaps
    mask = cv2.erode(thresh1, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # Find contours in the binary image
    _, contours, hierarchy = cv2.findContours(
                    mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # If contours are found
    if len(contours) > 0:
        # Find the largest contour
        c = max(contours, key=cv2.contourArea)
        if len(c) > 0:
            # Draw a bounding box around the contour
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
            # Calculate the center of the contour
            cx = int(x + w / 2)
            cy = int(y + h / 2)
            
            # Draw lines to visualize the center of the contour
            cv2.line(frame, (cx, 0), (cx, 720),
                        (255, 0, 0), 1)
            cv2.line(frame, (0, cy),
                        (1280, cy), (255, 0, 0), 1)
            
            print("cx:", cx, "cy:", cy)
        # Control the motor based on the position of the center of the contour
        if cx >= 225:
            print("Turn right")
            m1.changeSpeedTurn()
            m1.turn_right()
            string = "Turn right"
        if cx <= 135:
            print("Turn left")
            m1.changeSpeedTurn()
            m1.turn_left()
            string = "Turn left"
        if cx < 225 and cx > 135:
            print("Forward")
            m1.setSpeedDefault()
            m1.forward()
            string = "Forward"

    else:
        # If no contours are found, move backward
        print("Don't see the line")
        m1.backward()
        string = "No line detected"

    # Check if an obstacle is detected# Cont'd: and stop the motor
    if distance is not None:
        print("Distance:", distance)
        if distance <= min_distance:
            print("Obstacle detected!")
            m1.stop()
            string = "Obstacle detected"

    # Calculate and display the FPS
    fps_frames += 1
    fps_end = time.time()
    fps = fps_frames / (fps_end - fps_start)
    cv2.putText(frame, "FPS: {:.2f}".format(fps),
                (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the frame
    cv2.imshow("frame", frame)

    # Check for key press to exit the program
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

#Release resources and clean up GPIO pins
cap.release()
cv2.destroyAllWindows()
GPIO.cleanup()