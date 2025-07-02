#define PWM1 9
#define PWM2 10

String call, CH, OUT;
char n;
int currentchan = 0, currentout = 0, oldchan = 0, oldout = 0, delimiter, out;

void setup() {
  //DO NOT CHANGE SETTINGS!!!
  TCCR1B = TCCR1B & B11111000 | B00000001; // Set Frequency to 31372.55 Hz for both PWM signals
  Serial.begin(9600);
  pinMode(PWM1, OUTPUT);
  pinMode(PWM2, OUTPUT);
  analogWrite(PWM1, 0);
  analogWrite(PWM2, 0);
}

void loop() {
  //Serial communication: CH,OUTPUT
  //Check if data received and filter errors
  if (Serial.available()) {
    oldchan = currentchan;
    oldout = currentout;
    Serialreadall();
    if (String(call) == "END"){
      analogWrite(PWM1,0);
      analogWrite(PWM2,0);
      //Serial.println("Pumps are off");
    } 
    delimiter = call.indexOf(',');
    if (delimiter > -1) {
      CH = call.substring(0, delimiter);
      OUT = call.substring(delimiter + 1);
      currentchan = CH.toInt();
      currentout = OUT.toInt();
      if ((currentchan != 1 && currentchan != 2) || (!isNumeric(OUT))) {
        currentchan = oldchan;
        currentout = oldout;
      }
      //Directing data to specific pump
      switch (currentchan) {
      case 1:
        analogWrite(PWM2, 0);
        out = constrain(currentout, 0, 100);
        //Serial.println("Analog Out to Channel 1 at " + String(out) + "%");
        out = map(out, 0, 100, 0, 255);
        analogWrite(PWM1, out);

        break;
      case 2:
        analogWrite(PWM1, 0);
        out = constrain(currentout, 0, 100);
        //Serial.println("Analog Out to Channel 2 at " + String(out) + "%");
        out = map(out, 0, 100, 0, 255);
        analogWrite(PWM2, out);
        break;
      default:
        break;
      }

    }
  }
  delay(10);
}


//IMPORTANT FUNCTIONS!!! DO NOT DELETE!!!
void Serialreadall() {
  while (Serial.available() > 0) {
    call = "";
    delay(1);
    while (Serial.available()) {
      n = Serial.read();
      call += n;
      delay(1);
    }
    Serial.flush();
  }
}
boolean isNumeric(String str) {
  unsigned int stringLength = str.length();

  if (stringLength == 0) {
    return false;
  }

  boolean seenDecimal = false;

  for (unsigned int i = 0; i < stringLength; ++i) {
    if (isDigit(str.charAt(i))) {
      continue;
    }

    if (str.charAt(i) == '.') {
      if (seenDecimal) {
        return false;
      }
      seenDecimal = true;
      continue;
    }
    return false;
  }
  return true;
}

