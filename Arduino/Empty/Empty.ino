void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  // Pensaba poner un dibujo de chica anime ASCII por aquí, pero mejor no me gasto el tiempo
}

long counter = 0;

void loop() {
  // put your main code here, to run repeatedly:
  Serial.print("[");
  Serial.print(counter);
  Serial.print("] ");
  Serial.println("CanSat-Chan: ¡Prográmame! No tengo nada en el EEPROM.");
  counter++;
  delay(1000);
}
