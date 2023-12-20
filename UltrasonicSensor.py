import RPi.GPIO as GPIO
import time

# setup GPIO pins
echoPIN = 15
triggerPIN = 14

GPIO.setmode(GPIO.BCM)
GPIO.setup(echoPIN,GPIO.IN)
GPIO.setup(triggerPIN,GPIO.OUT)

def read_distance():
  new_reading = False
  counter = 0
  distance = 0
  duration = 0

  # send trigger
  GPIO.output(triggerPIN, 0)
  time.sleep(0.000002)
  GPIO.output(triggerPIN, 1)
  time.sleep(0.000010) # wait 10 us (the duration of the trigger)
  GPIO.output(triggerPIN, 0)
  time.sleep(0.000002)

  # wait for echo reading
  while GPIO.input(echoPIN) == 0:
    pass
    # handle freeze
    counter += 1
    if counter == 5000:
      new_reading = True
      break

  # handle freeze
  if new_reading:
    return False
    
  # data receiving has started - set start time
  startT = time.time()

  # skip while data is being received
  while GPIO.input(echoPIN) == 1: pass
 
  # data receiving has ended - set end time
  feedbackT = time.time()

  # calculate distance
  if feedbackT == startT:
    distance = "N/A" # handle error
  else:
    duration = feedbackT - startT
    soundSpeed = 34300 # cm/s
    distance = duration * soundSpeed / 2
    distance = round(distance, 1)
  time.sleep(0.2)
  return distance


# print the distance to the console
def run():
  try:
    while True:
      print (" Distance: " + str(read_distance())+ "   ", end='\r')
  except KeyboardInterrupt:
    print('interrupted!')
    GPIO.cleanup()

#run()
