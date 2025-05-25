# Info
This system reads in input from an RFID card reader and signs a user in or out using a Google sheet as a remote database.
The Google sheet stores user ids mapped to names, records a log of all card inputs, takes in input from a Google form as another login system, and compiles all that data into a dashboard showing each user's monthly and weekly hours.
This system notifies the user of their status, letting them know if their card was verified, calling them by name, and announcing whether they are now signed in or signed out.  It uses text-to-speech and sound effects to communicate with the user.
For now at least, the system is meant to be run on a laptop, through a terminal.  It may be modified to run on a Raspberry Pi in the future.  The screen does not need to be shown to the user---the system is meant to run with the laptop shut and hidden away on a shelf or somewhere.



### Authorizing Google Sheets
To install the python dependencies, run "pip install -r requirements.txt".
With the project's current configuration, all you need to do to authorize it is go to the google cloud project dashboard, go into IAM and Admin, and click on the email account.  Then go to "keys" and create a new key.  You can't download the file from an old key---if you lost the file just create a new key and use that file.  Downlaod it as a json, and save it to the root directory of this project "Signin-System/" and name it "service-account-key.json".  The system should then be authorized and work perfectly the next time you run it.



# Project Lifetime
This project was designed for the NEIA Robotics team, and intended to be used as a attendence tracking system, to give the team captains data about who was showing up the most.  It was used for about 4 months, but was then replaced by a full React webapp that used a Supabase backend (which worked much better than this hacked-together approach).  A few months later, we stopped using a sign-in system all together, so this project will no longer be updated.  However, it still contains some useful code for communicating with an Arduino, reading from an RFID peripheral, communicating with a Google Sheet, and Python asynchronous architecture.
