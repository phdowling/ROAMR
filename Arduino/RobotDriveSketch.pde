// This code creates a PWM signal that rotates a motor either left or right.
// PWM is used to control the voltage of the motor
//
// Simple schematic:
//
//                  +-------+                         VCC2=9V
//                  | L293D |                         VCC1=5V
//                  | |\    |
// MOTOR_DIR -------+-| >---+------[(M)]-----+
//                  | |/    |                |
//                  |       |                |
//                  | |\    |                |
// MOTOR_PWM -------+-| >---+----------------+
//                  | |/    |
//                  |       |
//                  +-------+

#include <avr/interrupt.h>
#include <avr/io.h>  


char index;
char serialbuff[7];
char ch;
int x=0;
int lSpeed;
int rSpeed;

int LMOTOR_DIR = 12;       // Non PWM pin for direction control
int LMOTOR_PWM = 11;       // PWM controlled pin.
int RMOTOR_DIR = 7;
int RMOTOR_PWM = 6;


void setup() {  
  Serial.begin(9600);

  // Set the pins to output.
  pinMode(LMOTOR_DIR, OUTPUT);
  pinMode(LMOTOR_PWM, OUTPUT);
  pinMode(RMOTOR_DIR, OUTPUT);
  pinMode(RMOTOR_PWM, OUTPUT);
  // And set them to a initial value to make sure.
  digitalWrite(LMOTOR_DIR, LOW);
  digitalWrite(LMOTOR_PWM, LOW);
  digitalWrite(RMOTOR_DIR, LOW);
  digitalWrite(RMOTOR_PWM, LOW);



void loop() {
  switch(x){
    case 0:{
      ch=(char)Serial.read();
      if(ch=='s'){
        x=1;
        serialbuff[0]=ch;
        index=1;
      }
    }
    break;
    
    case 1:{
      ch=(char)Serial.read();
      if(ch!=-1){
        serialbuff[index]=ch;
        index++;
        if(index==7){
         x=2;
        }
      }
    }
    break;
    
    case 2:{
      if(serialbuff[6]=='e'){
        x=3;
        /*int sum=0;
        for(index=1;index < 5; index++)
        {
          sum+=serialbuff[index];
        }
        if(sum==serialbuff[5]){
          x=3;
        }
        else{
          x=4;
        }*/
      }
      else{
      x=4;
    }
    }
    break;
      
    case 3:{
      if(serialbuff[1]=='+'){
        digitalWrite(LMOTOR_DIR, HIGH);
        lSpeed = 255-serialbuff[2];
      }
      else{
        digitalWrite(LMOTOR_DIR, LOW);
        lSpeed = serialbuff[2];
      }
       
      if(serialbuff[3]=='+'){
        digitalWrite(RMOTOR_DIR, HIGH);
        rSpeed = 255-serialbuff[4];
      }
      else{
        digitalWrite(RMOTOR_DIR, LOW);
        rSpeed = serialbuff[4];
      }
       
      analogWrite(LMOTOR_PWM, lSpeed);
      analogWrite(RMOTOR_PWM, rSpeed);
       
      x=4;
     }
    break;  
    
    case 4:{
      index=0;
      x=0;
    }
    break;
}
}
