String readString;
String bpstring,bpval, bp1,bp2,outputbp;
String pstring,val, v1, v2, output;
String tstring,ninject_index1,ninject_index2,ninjectstring;
String pulsewidth_index1, pulsewidth_index2, pulsewidthstring;
int bpvolt,apv, ninject,pulsewidth,n; //backpressure volt,inject pressure volt,num inject,pulsewidth of inject, conuter


void setup() {
  Serial.begin(9600);
  pinMode(11, OUTPUT);
  pinMode(2, OUTPUT);
  
}

void loop() {
 //runs when no data is here
 
  while (!Serial.available()) {
    } 

  //when something is being sent... buffer is 30ms
  while (Serial.available()) {
    delay(30);

    //interprets serial info
    if (Serial.available() > 0) {
      char c = Serial.read();
      readString += c;
    }
  }

  // if information is sent, print recieved data
  if (readString.length() > 0) {
    Serial.println("Arduino recieved:");
    Serial.println(readString);

    
    //looks for descriptor strings there are three options:
    //backpressure (compensation pressure) voltage ex. "bc40C" means set 40mbar as backpressure to prevent clogging
    //if bpstring == "0" the backpressure will be set and will continue to run later on if no other string is being read
    
    // pstring for pressure voltage ex. "pressure!134!" means set 134 as voltage out 
    // if pstring == 0 then the pressure will be set to pressure value, but no triggering occurs 
    
    // tstring for trigger command means trigger
    // if tstring == "0", the number of injections and pulse duration will be found in string and 
    // injection is triggered ninject times for pulseduration miliseconds
    // the whole string will look like "triggern06Nw100W" for trigger 6 injections at 100ms pulse duration
    
    bpstring = readString.indexOf("b");
    pstring = readString.indexOf("p");
    tstring = readString.indexOf("t");
    Serial.println(bpstring);
   
    
    //pressure control
    if (bpstring == "0") {
      //compensation pressure 
      bp1 = readString.indexOf("c");
      bp2 = readString.indexOf("C");
      outputbp = readString.substring(bp1.toInt()+1,bp2.toInt());
      bpvolt = outputbp.toInt();
      analogWrite(11,bpvolt);

      //injection pressure 
      v1=readString.indexOf("!");
      v2=readString.lastIndexOf("!");
      val=readString.substring(v1.toInt()+1,v2.toInt());
      apv=val.toInt();
      output = apv;
      delay(50);
      Serial.print("Compensation pressure set to:");
      Serial.println(outputbp);
      Serial.print("Injection pressure set to:");
      Serial.println(output);
      delay(50);
    }

    
    digitalWrite(2,HIGH); // open valve 
    
    //trigger control
    if (tstring == "0") {
      n = 0;
      // ninject for number of injections ex. "n06N" means 6 injections
      // pulsewidth for pulse width time of triggering in ms ex. "w100W" means 100ms

      ninject_index1 = readString.indexOf("n");
      ninject_index2 = readString.indexOf("N");
      ninjectstring = readString.substring(ninject_index1.toInt()+1,ninject_index2.toInt());
      ninject = ninjectstring.toInt();
    
      pulsewidth_index1 = readString.indexOf("w");
      pulsewidth_index2 = readString.indexOf("W");
      pulsewidthstring = readString.substring(pulsewidth_index1.toInt()+1,pulsewidth_index2.toInt());
      pulsewidth = pulsewidthstring.toInt();

      Serial.print("(pulsewidth,ninject) = ");
      Serial.print("(");
      Serial.print(pulsewidth);
      Serial.print(",");
      Serial.print(ninject);
      Serial.println(")");
      
      while (n < ninject) {
        analogWrite(11, apv); // inject at full pressure
        delay(pulsewidth);
        analogWrite(11, bpvolt); // stop injection but still have compensation pressure to prevent backflow
        
        output = "trigger" +String(n);
        n = n + 1;
        Serial.print("injected ");
        Serial.println(n);
      }
      Serial.println("Injection Complete");
    }
    
  delay(100);
  //clear strings
  readString = ""; 
  ninject = 0;
  bpstring = "";
  pstring = "";
  tstring = "";
  }
}
