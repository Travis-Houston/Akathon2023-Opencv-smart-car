import cv2
import motor1
import RPi.GPIO as GPIO
import time
import threading

m1 = motor1

# Set minimum distance threshold
min_distance = 20

# Set up GPIO mode
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Set GPIO pin of HC-SR04 to Raspberry 4
trig = 23
echo = 24

# Initialize GPIO Pin as outputs
GPIO.setup(trig, GPIO.OUT)

# Initialize GPIO Pin as input
GPIO.setup(echo, GPIO.IN)

# Function to measure distance
def distance_thread():
    global distance
    while True:
        # Send a trigger pulse to the HC-SR04
        GPIO.output(trig, GPIO.LOW)
        time.sleep(0.02)
        GPIO.output(trig, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(trig, GPIO.LOW)

        # Measure the duration of the echo pulse
        pulse_start = time.time()
        timeout = pulse_start + 0.1
        while GPIO.input(echo) == GPIO.LOW and pulse_start < timeout:
            pulse_start = time.time()

        pulse_end = time.time()
        timeout = pulse_end + 0.1
        while GPIO.input(echo) == GPIO.HIGH and pulse_end < timeout:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start

        # Calculate the distance to the object
        distance = pulse_duration * 17150

        # Wait for some time before taking the next measurement
        time.sleep(0.02)

# Start the distance measurement thread
distance = None
distance_thread = threading.Thread(target=distance_thread)
distance_thread.daemon = True
distance_thread.start()

# Initialize the video capture object
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 360)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
cap.set(cv2.CAP_PROP_FPS, 30)

# Initialize fps calculation variables
fps_start = time.time()
fps_frames = 0

while True:
    # Read the frame from the webcam
    ret, frame = cap.read()
    crop_img = frame[60:120, 0:160]
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Line tracking code
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh1 = cv2.threshold(blur, 50, 255, cv2.THRESH_BINARY_INV)
    mask = cv2.erode(thresh1, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    _, contours, hierarchy = cv2.findContours(
                    mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        if len(c) > 0:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
            cx = int(x + w / 2)
            cy = int(y + h / 2)
            cv2.line(frame, (cx, 0), (cx, 720),
                        (255, 0, 0), 1)  # draw cx
            cv2.line(frame, (0, cy),
                        (1280, cy), (255, 0, 0), 1)
            # print cordidate cx and cy
            print("cx:", cx, "cy:", cy)
        if cx >= 225:
            print("Turn right")
            m1.changeSpeedTurn()
            m1.turn_right()
        if cx <= 135:
            print("Turn left")
            m1.changeSpeedTurn()
            m1.turn_left()
        if cx < 225 and cx >135:
            print("Forward")
            m1.setSpeedDefault()
            m1.forward()

    else:
        print("Don't see the line")
        m1.backward()

    # Obstacle detection code
    if distance is not None:
        print("Distance:", distance)
        if distance <= min_distance:
            print("Obstacle detected!")
            # Stop the motor or take evasive action here
            m1.stop()

    # Display the frame
    fps_frames += 1
    fps_end = time.time()
    fps = fps_frames / (fps_end - fps_start)
    cv2.putText(frame, "FPS: {:.2f}".format(fps),
                (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    cv2.imshow("frame", frame)

    # Check for key presses
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# Clean up
cap.release()
cv2.destroyAllWindows()
GPIO.cleanup()