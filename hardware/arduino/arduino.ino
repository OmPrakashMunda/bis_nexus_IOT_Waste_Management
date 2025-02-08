#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <time.h>

const char* ssid = "OPNETWORK";
const char* password = "123456789";
const char* serverUrl = "https://iotwm-api.teamitj.tech/api/bins";

const int TRIG_PIN_1 = 2;
const int ECHO_PIN_1 = 3;
const int TRIG_PIN_2 = 4;
const int ECHO_PIN_2 = 5;
const float BIN_HEIGHT = 8.5;

const char* ntpServer = "pool.ntp.org";
const long gmtOffset_sec = 19800;    // IST offset: 5.5 hours = 19800 seconds
const int daylightOffset_sec = 0;    // No daylight saving in India

void setup() {
  Serial.begin(9600);
  
  pinMode(TRIG_PIN_1, OUTPUT);
  pinMode(ECHO_PIN_1, INPUT);
  pinMode(TRIG_PIN_2, OUTPUT);
  pinMode(ECHO_PIN_2, INPUT);
  
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to WiFi");
  
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
}

float getMeasurement(int trigPin, int echoPin) {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  float duration = pulseIn(echoPin, HIGH);
  float distance = duration * 0.034 / 2;
  float fillLevel = 100.0 * (1.0 - (distance / BIN_HEIGHT));
  
  return constrain(fillLevel, 0, 100);
}

String getISTTime() {
  struct tm timeinfo;
  if(!getLocalTime(&timeinfo)){
    return String(millis());
  }
  char timeStringBuff[50];
  strftime(timeStringBuff, sizeof(timeStringBuff), "%Y-%m-%d %H:%M:%S", &timeinfo);
  return String(timeStringBuff);
}

void sendData(float fillLevel1, float fillLevel2) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");
    
    StaticJsonDocument<200> doc;
    
    JsonObject bin1 = doc.createNestedObject("bin1");
    bin1["id"] = 1;
    bin1["fillLevel"] = fillLevel1;
    bin1["timestamp"] = getISTTime();
    
    JsonObject bin2 = doc.createNestedObject("bin2");
    bin2["id"] = 2;
    bin2["fillLevel"] = fillLevel2;
    bin2["timestamp"] = getISTTime();
    
    String jsonString;
    serializeJson(doc, jsonString);
    
    int httpResponseCode = http.POST(jsonString);
    
    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println("HTTP Response: " + response);
    } else {
      Serial.println("Error sending data");
    }
    
    http.end();
  }
}

void loop() {
  float fillLevel1 = getMeasurement(TRIG_PIN_1, ECHO_PIN_1);
  float fillLevel2 = getMeasurement(TRIG_PIN_2, ECHO_PIN_2);
  
  Serial.printf("Bin 1: %.1f%%, Bin 2: %.1f%% at %s\n", fillLevel1, fillLevel2, getISTTime().c_str());
  
  sendData(fillLevel1, fillLevel2);
  
  delay(5000);
}