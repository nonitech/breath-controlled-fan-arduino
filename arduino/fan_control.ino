// C++ code
/*Telematic Breath system. We use wind speed sensor(Potentiometer instead of a wind speed sensor) 
to make the fan(motor used instead) start spinning and control the speed base on the quantity of the 
breath(air flow) which the sensor receive. */

#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// Tinkercad uses address 32 (0x20), not 0x27
LiquidCrystal_I2C lcd(32, 16, 2); // Initialize I2C LCD (address 32 which is 0x20, 16 columns, 2 rows)

const int motorPin = 5;
const int sensorPin = A0;

const int minReading = 35;
const int maxReading = 1000;
const int motorStart = 100;

int analogValue = 0;
int motorSpeed = 0;

void setup() 
{
  Serial.begin(9600);
  pinMode(motorPin, OUTPUT);
  lcd.init();         // Initialize the LCD
  lcd.backlight();    // Turn on the backlight
}


void loop()
{
  analogValue = analogRead(sensorPin);
  analogValue = constrain(analogValue, minReading, maxReading);
  motorSpeed = map(analogValue, minReading, maxReading, 0, 255);

  if((analogValue > minReading) && (analogValue < motorStart))
  {
    analogWrite(motorPin, motorStart);    
  }
  else analogWrite(motorPin, motorSpeed);
  
  // LCD display
   // Set the cursor to column 0, row 0 (the first row)
  lcd.setCursor(0,0);
  lcd.print("Breath:");
  lcd.print(analogValue);
  lcd.print("   ");  // Print spaces to overwrite old digits (prevents ghosting from 1000 to 99)

   // Set the cursor to column 0, row 1 (the second row)
  lcd.setCursor(0,1);
  lcd.print("Motor:");
  lcd.print(motorSpeed);
  lcd.print("   ");  // clear extra characters
  
   // Send data to Python (format: breath,motorSpeed)
  Serial.print(analogValue);  // breath value
  Serial.print(",");          // separator
  Serial.println(motorSpeed); // motor speed
  
  delay(25);  // updates every 25ms for smooth plotting  
}
