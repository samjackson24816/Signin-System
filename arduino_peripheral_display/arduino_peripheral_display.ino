// Define the buzzer pin
const int buzzerPin = 3;

// Define the notes and their frequencies
#define NOTE_C4 262
#define NOTE_D4 294
#define NOTE_E4 330
#define NOTE_F4 349
#define NOTE_G4 392
#define NOTE_A4 440
#define NOTE_B4 494
#define NOTE_C5 523

// Define the melody
int melody[] = {
  NOTE_C4, NOTE_D4, NOTE_E4, NOTE_F4, NOTE_G4, NOTE_A4, NOTE_B4, NOTE_C5
};

// Define the duration of each note (in milliseconds)
int noteDuration = 500;

// Define the Command enum first so it's recognized everywhere
enum Command {
  SIGNED_IN,
  SIGNED_OUT,
  NOT_REGESTERED,
  NONE
};


void setup() {
  // Set the buzzer pin as an output
  pinMode(buzzerPin, OUTPUT);
  Serial.begin(9600);
}

class OutputIO {
  public:
    virtual void createResources() = 0;
    virtual void startCommand(Command command) = 0;
    virtual void runCommand() = 0;
    virtual bool isCommandFinished() = 0;
    virtual void endCommand() = 0;
};

class OutputIOLED : public OutputIO {

  int rPin = 9;
  int gPin = 10;
  int bPin = 11;

  int inLength = 3;
  uint32_t inColors[3] = {0x00FF00, 0x000000, 0x00FF00};
  int inDurationsMillis[3] = {300, 300, 300};

  int outLength = 3;
  uint32_t outColors[3] = {0x0000FF, 0x000000, 0x0000FF};
  int outDurationsMillis[3] = {300, 300, 300};

  int nrLength = 5;
  uint32_t nrColors[5] = {0xFF0000, 0x000000, 0xFF0000, 0x000000, 0xFF0000};
  int nrDurationsMillis[5] = {500, 300, 500, 300, 500};

  int length = 0;
  uint32_t* colors = NULL;
  int* durationsMillis = NULL;

  unsigned long nextChangeTimeMillis = 0;

  int index = 0;

  Command commandType = Command::NONE;

  bool done = false;

  void setColor(int r, int g, int b) {
    analogWrite(rPin, r);
    analogWrite(gPin, g);
    analogWrite(bPin, b);
  }

  void setColor(uint32_t rgb) {
    int r = (rgb >> 16) & 0xFF;   // Extract red (bits 16-23)
    int g = (rgb >> 8) & 0xFF;  // Extract green (bits 8-15)
    int b = rgb & 0xFF;          // Extract blue (bits 0-7)

    Serial.print("R: ");
    Serial.print(r);
    Serial.print("  G: ");
    Serial.print(g);
    Serial.print("  B: ");
    Serial.print(b);

    analogWrite(rPin, r);
    analogWrite(gPin, g);
    analogWrite(bPin, b);

  }

  public:
    void createResources() {
      pinMode(rPin, OUTPUT);
      pinMode(gPin, OUTPUT);
      pinMode(bPin, OUTPUT);
    }

    void startCommand(Command command) override {
      commandType = command;
      
      index = 0;
      done = false;
      nextChangeTimeMillis = 0;
      Serial.print("Starting LED Command: ");
      Serial.println(commandType);

      switch (commandType) {
        case Command::SIGNED_IN:
          colors = inColors;
          durationsMillis = inDurationsMillis;
          length = inLength;
          break;
        case Command::SIGNED_OUT:
          colors = outColors;
          durationsMillis = outDurationsMillis;
          length = outLength;
          break;
        case Command::NOT_REGESTERED:
          colors = nrColors;
          durationsMillis = nrDurationsMillis;
          length = nrLength;
          break;
      }
      return true;
    }

    void runCommand() override {
      Serial.println("Running LED Command");

      if (millis() > nextChangeTimeMillis) {

        if (index >= length) {
          done = true;
        } else {
          setColor(colors[index]);
          nextChangeTimeMillis = millis() + durationsMillis[index];
          index++;
        }
        
      }

    }

    bool isCommandFinished() override {
        return done;
    }

    void endCommand() override {
      Serial.println("Ending LED Command");
      setColor(0, 0, 0);
    }
};

Command command = Command::NONE;
OutputIO* output = new OutputIOLED();  // Instantiate a derived class object



// Declare function prototypes so they can be called in loop() before being defined
Command update(OutputIO& output, Command command);
Command parseInput(String input);

void loop() {
  command = update(*output, command);  // Pass output by reference
}

// Define the update function
Command update(OutputIO& output, Command command) {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    command = parseInput(input);

    output.endCommand();

    if (command != Command::NONE) {
      output.startCommand(command);
    }
  }

  if (command != Command::NONE) {  // Fix the enum access
    output.runCommand();

    if (output.isCommandFinished()) {

      output.endCommand();
      command = Command::NONE;
    }
  }

  return command;
}

// Define the parseInput function
Command parseInput(String input) {
  // Process the serial input here
  Serial.print("Received: ");
  Serial.println(input);
  
  Command command = Command::NONE;

  if (input == "IN") {
    command = Command::SIGNED_IN;
  } else if (input == "OUT") {
    command = Command::SIGNED_OUT;
  } else if (input == "NR") {
    command = Command::NOT_REGESTERED;
  } else {
    command = Command::NONE;
  }
  return command;
}
