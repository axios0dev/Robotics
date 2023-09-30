// This code contains the firmware and underlying functionality for the AxiosRoboticsRCv1 sensor module.
// This code is designed to run on a 3v3 logic Arduino pro mini.
// Constant pin definitions.
// Left sensor pins.
const int LeftSensorTrigPin = 3;
const int LeftSensorEchoPin = 5;
// Right sensor pins.
const int RightSensorTrigPin = 2;
const int RightSensorEchoPin = 4;
// Variables to store pulse duration and distance calculations.
long LeftSensorEchoPulseDuration;
int LeftSensorDistance;
long RightSensorEchoPulseDuration;
int RightSensorDistance;

// Initial pin and serial connection setup.
void setup() {
  // Left sensor pin configuration.
  pinMode(LeftSensorTrigPin, OUTPUT);
  pinMode(LeftSensorEchoPin, INPUT);
  // Right sensor pin configuration.
  pinMode(RightSensorTrigPin, OUTPUT);
  pinMode(RightSensorEchoPin, INPUT);
  // Begin the serial connection with a 9600 baudrate.
  Serial.begin(9600);

}

// This function triggers first the left sensor then the right sensor, after each sensor is triggered
// the pulse length received over the echo pin is measured then the distance of the object in front of
// the sensor is calculated. The result is then keyed and added to a string which is sent over the serial
// connection back to the AxiosRoboticsRCv1 unit every 100ms. 
void SensorReadingRoutine(){
 // Left sensor distance to closest object logic.
 // Pull the trigger pin low in preparation before triggering the sensor.
  digitalWrite(LeftSensorTrigPin, LOW);
  delayMicroseconds(2);
  // Trigger the left sensor, hold the trigger pin high for 10us.
  digitalWrite(LeftSensorTrigPin, HIGH); 
  delayMicroseconds(10);
  // Pull trigger pin low to end trigger sequence.
  digitalWrite(LeftSensorTrigPin, LOW);
  // Measure the duration of the pulse length received on the echo pin.
  LeftSensorEchoPulseDuration = pulseIn(LeftSensorEchoPin, HIGH);
  // Times the pulse length duration by the speed of sound per cm/ms to calculate the ultrasonic wave distance.
  // Then divide by 2 to get only the distance to the closet object and not the entire path to the object and 
  // back to the receiver.
  LeftSensorDistance = LeftSensorEchoPulseDuration * (0.034 / 2);

  // Right sensor distance to closest object logic.
  // Pull the trigger pin low in preparation before triggering the sensor.
  digitalWrite(RightSensorTrigPin, LOW);
  delayMicroseconds(2);
  // Trigger the right sensor, hold the trigger pin high for 10us.
  digitalWrite(RightSensorTrigPin, HIGH); 
  delayMicroseconds(10);
  digitalWrite(RightSensorTrigPin, LOW);
  // Pull trigger pin low to end trigger sequence.
  RightSensorEchoPulseDuration = pulseIn(RightSensorEchoPin, HIGH);
  // Times the pulse length duration by the speed of sound per cm/ms to calculate the ultrasonic wave distance.
  // Then divide by 2 to get only the distance to the closet object and not the entire path to the object and 
  // back to the receiver.
  RightSensorDistance = RightSensorEchoPulseDuration  * (0.034 / 2);

  // Create a string with a keyed L: and R: sensor value and write it out over the serial connection every 100ms
  // to the AxiosRoboticsRCv1 unit. 
  Serial.print("L:");
  Serial.print(LeftSensorDistance); 
  Serial.print(","); 
  Serial.print("R:");
  Serial.println(RightSensorDistance);
  // Rate limited to once every 100ms.
  delay(100);
}

// Constant string definitions to for toggling on/off the SensorReadingRoutine().
const String SensorOnState = "ON";
const String SensorOffState = "OFF";
// Variable to store data received over serial and the sensor monitoring state.
String ReceivedSerialData;
bool SensorReadingRoutineStarted = false;

// This main function checks if state requests have been received over serial from the AxiosRoboticsRCv1 unit
// and applies the requested state. Which proceeds to run/stop the SensorReadingRoutine(). 
void loop() {
  // First check for any requested state changes to the SensorReadingRoutine() state.
  if (Serial.available() > 0) {
    // Read the serial data into a string.
    ReceivedSerialData = Serial.readStringUntil('\n');
    // If a request to turn on the SensorReadingRoutine() has been received then set the state flag to true, which
    // will cause the routine to be run on every iteration until a request to change the state has been received.
    if(ReceivedSerialData == SensorOnState){
      SensorReadingRoutineStarted = true;
    }
    // Disable the SensorReadingRoutine() when a request to turn off sensor monitoring has been received.
    else if(ReceivedSerialData == SensorOffState){
      SensorReadingRoutineStarted = false;
    }
  }
  
  // Run the sensor monitoring routine when the state has been enabled.
  if(SensorReadingRoutineStarted){
    SensorReadingRoutine();
  }
}
