# Info
This system reads in input from an RFID card reader and signs a user in or out using a Google sheet as a remote database.
The Google sheet stores user ids mapped to names, records a log of all card inputs, takes in input from a Google form as another login system, and compiles all that data into a dashboard showing each user's monthly and weekly hours.
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
- test thoroughly 
- document


### Authorizing Google Sheets
With the project's current configuration, all you need to do to authorize it is go to the google cloud project dashboard, go into IAM and Admin, and click on the email account.  Then go to "keys" and create a new key.  Downlaod it as a json, and save it to the root directory of this project "Signin-System/" and name it "service-account-key.json".  The system should then be authorized and work perfectly the next time you run it.
