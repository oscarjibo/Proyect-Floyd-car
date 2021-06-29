

int IN3 = 4;    
int IN4 = 2;    
int ENB = 3;    
int IN1 = 7;    
int IN2 = 5;    
int ENA = 6;    
int persona = 8; 
int carro = 9;
int stops = 10;
int derecha=A2;
int izquierda=A1;
int recto=A0;
void setup()
{
 Serial.begin(9600);   // pongo puerto serie 
 pinMode (ENB, OUTPUT); 
 pinMode (IN3, OUTPUT);
 pinMode (IN4, OUTPUT);
 pinMode (ENA, OUTPUT); 
 pinMode (IN1, OUTPUT);
 pinMode (IN2, OUTPUT);
 pinMode (persona,INPUT); // llerga de la pi
 pinMode (carro,INPUT);
 pinMode (stops,INPUT);
 pinMode (derecha,INPUT);
 pinMode(izquierda,INPUT);
 pinMode(recto,INPUT);
}
void loop()
{
  digitalWrite (IN3, HIGH);
  digitalWrite (IN4, LOW);
  digitalWrite (IN1, LOW);
  digitalWrite (IN2, HIGH);
  analogWrite(ENB,75);
  analogWrite(ENA,75);
  // vamos a darle direccion
  derecha=analogRead(derecha);
  if (derecha==HIGH);{
    analogWrite(ENB,0);
    analogWrite(ENA,70);
  }
    izquierda=analogRead(izquierda);
  if (izquierda==HIGH);{
    analogWrite(ENB,70);
    analogWrite(ENA,0);
 
  }
      recto=analogRead(recto);
  if (recto==HIGH);{
    analogWrite(ENB,70);
    analogWrite(ENA,70);
 
  }
  
  
  
  
  
  
  persona=digitalRead(8); // para persona 
  if (persona ==HIGH){
    Serial.println("detectamos una persona");
  }
  else {
    Serial.println("");
  }
  carro=digitalRead(9);// para el carro
    if (carro ==HIGH){
    Serial.println("detectamos un carro");
  }
  else {
    Serial.println("");
  }
  stops=digitalRead(10);// para los stop
    if (stops ==HIGH){
        analogWrite(ENB,0);
        analogWrite(ENA,0);
      
    Serial.println("detectamos un STOP");
  }
  else {
    Serial.println("");
    analogWrite(ENB,60);
    analogWrite(ENA,60);
  }

  delay(200);
}
