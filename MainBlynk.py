import time
import RPi.GPIO as GPIO
from datetime import datetime
import threading
 
import BlynkLib
from UltrasonicSensor import read_distance
from Content import get_temperature, get_fact, get_trivia, get_trivia_answer, get_weather_details, increment_index
from Timer import Timer


BLYNK_AUTH = '1gQnZr7XwdOn23xe_n9YlNzUOPwX55GI'

blynk = BlynkLib.Blynk(BLYNK_AUTH)

# Defines used in content start/stop logic
CONTENT_START_TIME = 0
MAX_RUN_TIME = 3
#

#Variable used for temperature caching
TEMP = None
#

def log(msg):
  print('[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '] ' + msg)


# factory method for the content thread
def create_content_thread():
  return threading.Thread(target=get_content, daemon=True)


def get_time():
  blynk.run()
  time_formatted = datetime.now().strftime('%H:%M:%S')
  log("Writing to VP 1: " + str(time_formatted))
  blynk.virtual_write(1, str(time_formatted))


def get_distance():
  blynk.run()
  dist = read_distance()
  if dist != 'False': 
    log("Writing to VP 0: " + str(dist))
    blynk.virtual_write(0, dist)
    
    # determine if content display should start
    global content_thread
    global ev
    
    # sensor detected movement - start showing content
    if dist < 100:
      if not content_thread.is_alive():
	# restart thread
        content_thread = create_content_thread()
        content_thread.start()
	# reset event
        content_event.clear()
	
	# set start time
        global CONTENT_START_TIME
        CONTENT_START_TIME = time.time()
    
    # sensor stopped detecting movement - stop showing content
    elif time.time() - CONTENT_START_TIME > MAX_RUN_TIME and content_thread.is_alive():
      log("Content thread will shut down")
      content_event.set()
	

def get_temp():
  blynk.run()
  
  # cache temperature
  global TEMP
  if TEMP is None:
    TEMP = get_temperature()
  log("Writing to VP 2: " + str(TEMP))
  blynk.virtual_write(2, TEMP)
  
  
def get_content():
  pause_time = 2
  log("Content thread started")
  while True:
    blynk.run()
    
    fact = get_fact()
    log("Writing to VP 3: " + fact)
    blynk.virtual_write(3, fact)
    time.sleep(pause_time)
    
    trivia = get_trivia()
    log("Writing to VP 3: " + trivia)
    blynk.virtual_write(3, trivia)
    time.sleep(pause_time)
    
    answer = get_trivia_answer()
    log("Writing to VP 3: " + answer)
    blynk.virtual_write(3, "Answer: " + answer)
    time.sleep(pause_time)

    increment_index()

    weather_details = get_weather_details()
    log("Writing to VP 3: " + weather_details)
    blynk.virtual_write(3, weather_details)
    time.sleep(pause_time)
    
    global ev
    if content_event.is_set():
      break
  log("Content thread shutting down")
	
	
#----------#
#---MAIN---#
#----------#
content_thread = create_content_thread()
content_event = threading.Event()	

timer_dist = Timer(1, get_distance)
timer_dist.set_interval(1)

timer_time = Timer(2, get_time)
timer_time.set_interval(1)

timer_temp = Timer(3, get_temp)
timer_temp.set_interval(1800)

try:
  while True:
    timer_dist.run()
    timer_time.run()
    timer_temp.run()
except KeyboardInterrupt:
  log('\ninterrupted! - cleaning up GPIO')
  GPIO.cleanup()
