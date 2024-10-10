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
    virtual void startCommand(Command command) = 0;
    virtual void runCommand() = 0;
    virtual bool isCommandFinished() = 0;
    virtual void endCommand() = 0;
};

class OutputIOLED : public OutputIO {

  unsigned long startTimeMillis = 0;
  unsigned long durationMillis = 1000;

  Command commandType = Command::NONE;

  public:
    void startCommand(Command command) override {
      commandType = command;
      Serial.print("Starting LED Command: ");
      Serial.println(commandType);

      startTimeMillis = millis();
      return true;
    }

    void runCommand() override {
      Serial.println("Running LED Command");
    }

    bool isCommandFinished() override {
        return startTimeMillis + durationMillis < millis();
    }

    void endCommand() override {
      Serial.println("Ending LED Command");
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

    if (command != Command::NONE) {
      output.endCommand();
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
