#define pin 2

void setup() {
  // put your setup code here, to run once:

  Serial.begin(115200);
  pinMode(pin, OUTPUT);
  
}

void loop() {
  // put your main code here, to run repeatedly:

  Serial.print("hi");
  digitalWrite(pin, HIGH);
  delay(1000);
  digitalWrite(pin,LOW);
  delay(1000);
}
