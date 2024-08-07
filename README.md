# Info
I've tried to keep as much dependencies as possible within this repo, in order to make it easier for me to transfer this project to another machine depending on how we decide to implement it.
This is why I've added the virtual environment even though you're usually not supposed to do that.
The project also depends on a "client_secret.json" file and a "sheets.googleapis.com-python.json" file, which I haven't added to this repo because they contain my google account api keys.
# Progress
## So Far
- system for reading in card data
- local file for keeping user profiles
- handling system for new and unknown users
- system for logging card scans to a google sheet

## To do
- testing to see whether remoher storage of valid ids and profiles will be fast enough, or whether local caching will be needed
- adding system for reading user profiles from remote --- either on-scan or continuously updating a cache

## Questions
What needs to be stored locally and what can be stored remotely on the google sheet?
The system should provide fast, almost instentanious feedback.  If your card is not detcted, it should tell you right away.  If you are now signed out / in, it should tell you right away
If the system has a screen, it should display your name and status (signed in/out).  It should make a unique noise regardless
The main question is: will the delay caused from a query to a remote google sheet be quick enough for the user to wait for?
The users will be scanning quickly as they rush through the door, so a delay of even a couple seconds could be too long
The things to determine are:
- Should a list of valid cards be maintained locally?
- Should a dictionary of card ids mapped to names be maintained locally?
- Should a list of user statuses (signed in or out) be maintained locally?
- Should a log of sign-in sign-out times be maintained locally (either as a backup, alternative, or debugging resource)
