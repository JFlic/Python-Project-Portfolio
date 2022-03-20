int VRx = A0;
int VRy = A1;
int SW = 2;

//wheel 1 variables
int wheelSpeed = 6;
int dir1 = 4;
int dir2 = 3;
int mSpeed = 255;




int xPosition = 0;
int yPosition = 0;
int SW_state = 0;
int mapX = 0;
int mapY = 0;

void setup() {
  Serial.begin(9600); 
  
  pinMode(VRx, INPUT);
  pinMode(VRy, INPUT);
  pinMode(SW, INPUT_PULLUP);
  pinMode(wheelSpeed,OUTPUT);
   pinMode(dir1,OUTPUT);
    pinMode(dir2,OUTPUT);
}

void loop() {
  xPosition = analogRead(VRx);
  yPosition = analogRead(VRy);
  SW_state = digitalRead(SW);
  mapX = map(xPosition, 0, 1023, -255, 255);
  mapY = map(yPosition, 0, 1023, -255, 255);
  
  

  if (mapY< 0){
    Serial.print("X: ");
    Serial.print(mapX);
    Serial.print(" | Y: ");
    Serial.print(mapY);
    Serial.print(" | Button: ");
    Serial.println(SW_state);
    
    digitalWrite(dir1,HIGH);
    digitalWrite(dir2,LOW);
    analogWrite(wheelSpeed, -mapY);
  }if (mapY> 0){
    Serial.print("X: ");
    Serial.print(mapX);
    Serial.print(" | Y: ");
    Serial.print(mapY);
    Serial.print(" | Button: ");
    Serial.println(SW_state);
    
    digitalWrite(dir1,LOW);
    digitalWrite(dir2,HIGH);
    analogWrite(wheelSpeed, mapY);
  }
  

  delay(200);
  
}
