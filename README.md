# Info
This system reads in input from a RFID card reader and signs a user in or out using a google sheet as a remote database.
The google sheet stores user ids mapped to names, records a log of all card inputs, takes in input from a google form as another login system, and compiles all that data into a dashboard showing each user's monthly and weekly hours.
This system notifies the user of their status, letting them know if their card was verified, calling them by name, and announcing whether they are now signed in or signed out.  It uses text-to-speech and sound effects to communicate with the user.
For now at least, the system is meant to be run on a laptop, through a terminal.  It may be modified to run on a Raspberry Pi in the future.  The screen does not need to be shown to the user---the system is meant to run with the laptop shut and hidden away on a shelf or somewhere.


## Progress
### So Far
- system for reading in card data
- interaction with remote google sheet
- system for logging cards, validating users, and signing users in
- generic sound queuing system with text-to-speech and sound effects

### To do
- abstract away google sheet interactions from main file
- catch and handle all possible exceptions
- test throughoutly
- document
