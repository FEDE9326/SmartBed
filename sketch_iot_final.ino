#include "Time.h"  
#include "ArduinoJson.h"
#include "MMA_7455.h" //Include the MMA_7455 library
#include <BridgeClient.h>
#include <Bridge.h>
#include "PubSubClient.h"

/*Sensors */
MMA_7455 accelerometer = MMA_7455(); //Make an instance of MMA_7455
int xVal, yVal, zVal; //Variables for the values from the sensor
bool accReads=false;

/*JSON objects*/
StaticJsonBuffer<120> jsonBuffer;
JsonObject &root = jsonBuffer.createObject();
JsonObject &e = root.createNestedObject("e");
JsonObject &v = e.createNestedObject("v");
char message[127];

/*MQTT */
IPAddress server(192, 168, 1, 254); // MQTT server address
BridgeClient yun;
void callback(char* topic, byte* payload, unsigned int length);
PubSubClient client(server,1883, callback, yun);

/*
0  -> the subscription goes ok
-1 -> After 50 attemptes of subscriptions
*/
int checkSubscription(String topic);
void checkAndReconnect(char* id, char* topic);

void setup() {
  Serial.begin(9600);
  Bridge.begin();
  pinMode(13, OUTPUT);

  /*Sensing setup*/
  Serial.println("Serial connection established from Arduino.");
  accelerometer.initSensitivity(2); 
  accelerometer.calibrateOffset(-252,-240,-68); //Uncomment for first try: find offsets

  /*MQTT setup*/
  while(client.connect("arduino")!= true);
  checkSubscription("smart_bed/command");


   
}

void loop() {
  client.loop();
  
  chackAndReconnect("arduino","smart_bed/command");
    
  if (accReads == true)
  { 
        
    xVal = accelerometer.readAxis('x'); //Read out the 'x' Axis
    yVal = accelerometer.readAxis('y'); //Read out the 'y' Axis
    zVal = accelerometer.readAxis('z'); //Read out the 'z' Axis
    //package in a json message
    root["bn"] = "arduino"; //sensor ID
    root["bt"] = now();     //timestamp

    e["n"] = "Movment x,y,z";
    e["u"] = "g";
    v["x"] = xVal;
    v["y"] = yVal;
    v["z"] = zVal;
    
    root.printTo(message, sizeof(message)); 
    //Serial.println(message);
    
    if (client.publish("smart_bed/values",message)== false){
        if(client.publish("smart_bed/values",message) == false{
            digitalWrite(13, HIGH);
	    delay(1000);
	    digitalWrite(13, LOW);
        }
    }
            
    //stop sensing for 1000ms
    delay(1000);
    
  }
}//endLoop

void callback(char* topic, byte * payload, unsigned int length) {
  if (strcmp(topic,"smart_bed/command")==0){

    String inMessage = "";
    for (unsigned int i = 0; i < length; i++) {
      inMessage += (char)payload[i];
    }
    
    if (inMessage=="{\"status\": 1}")
      accReads=true;
    if (inMessage=="{\"status\": 0}")
      accReads=false;
  }
}

int checkSubscription(char* topic){
  int a=false;
  int countAttempt=0;
  while (a != true){
    a = client.subscribe(topic);
    if (a == true){
      //Serial.println("subscribe ok");
      return 0;
    }
    else{
      //Serial.println("subscribe fails");
      if(countAttempt++ >50);{
        return -1;
      }
    }
    delay(1500);
  }
  
}

void chackAndReconnect(char* id,char* topic){
  if (client.connected()==false) {
    while(client.connect(id)!=true);
    client.subscribe(topic);
  }
}
