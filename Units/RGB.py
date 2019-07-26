#Author Elliott Tiver
#Raspbery PI3 RGB LED project
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17,GPIO.OUT) #RED
GPIO.setup(27,GPIO.OUT) #GREEN
GPIO.setup(22,GPIO.OUT) #BLUE

#RGB  COLOUR FUNCTIONS/COMBINATIONS
def redLED(state):
	if (state == "ON" or state == "on"):
		GPIO.output(17, True)
	elif (state == "OFF" or state == "off"):
		GPIO.output(17, False)

def greenLED(state):
	if (state == "ON" or state == "on"):
		GPIO.output(27, True)
	elif (state == "OFF" or state == "off"):
		GPIO.output(27,False)

def blueLED(state):
	if (state == "ON" or state == "on"):
		GPIO.output(22, True)
	elif (state == "OFF" or state == "off"):
		GPIO.output(22, False)

def yellowLED(state):
	if (state == "ON" or state ==  "on"):
		redLED("ON")
		greenLED("ON")
	elif (state == "OFF" or state == "off"):
		redLED("OFF")
		greenLED("OFF")

def cyanLED(state):
	if (state == "ON" or state == "on"):
		greenLED("on")
		blueLED("ON")
	elif (state == "OFF" or state == "off"):
		greenLED("off")
		blueLED("off")

def magLED(state):
	if (state == "ON" or state == "on"):
		redLED("ON")
		blueLED("ON")
	elif (state == "OFF" or state == "off"):
        	redLED("off")
                blueLED("off")

def whiteLED(state):
	if (state == "ON" or state == "on"):
		redLED("ON")
                blueLED("ON")
		greenLED("ON")
	elif (state == "OFF" or state == "off"):
                redLED("off")
                blueLED("off")
		greenLED("OFF")
def orangeLED(state):
	if (state == "ON" or state == "on"):
                redLED("ON")
                yellowLED("ON")
        elif (state == "OFF" or state == "off"):
                redLED("off")
                yellowLED("OFF")	
 


#unexplaned colour mixing before code runs simple fix
redLED("off")
greenLED("OFF")
blueLED("OFF")

for x in range (3):
	redLED("on")
	time.sleep(1)
	redLED("OFF")
	greenLED("ON")
	time.sleep(1)
	greenLED("OFF")
	blueLED("ON")
	time.sleep(1)
	blueLED("off")
	yellowLED("ON")
	time.sleep(1)
	yellowLED("OFF")
	cyanLED("ON")
	time.sleep(1)
	cyanLED("OFF")
	magLED("ON")
	time.sleep(1)
	magLED("off")
	whiteLED("ON")
	time.sleep(1)
	whiteLED("OFF")
	orangeLED("ON")
	time.sleep(1)
	orangeLED("OFF")
GPIO.cleanup()
       






	
	
	



